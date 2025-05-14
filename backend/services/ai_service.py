"""
AI service for mental health support.
"""
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from backend.db.dynamodb import feedback_table, chat_history_table, create_item, get_item, update_item, delete_item, query_items
from backend.db.dynamodb import chat_history_table, create_item, get_item, update_item, delete_item, query_items
from backend.core.exceptions import NotFoundException
from backend.core.utils import generate_uuid, get_current_timestamp
from backend.config import settings
from backend.rag import get_rag_response
from backend.services import nlp_service
from backend.services import mood_service, journal_service, medication_service, reminder_service

# Crisis keywords and phrases
CRISIS_KEYWORDS = [
    "suicide", "kill myself", "end my life", "want to die", "don't want to live",
    "self-harm", "hurt myself", "cutting myself", "harming myself",
    "hopeless", "worthless", "can't go on", "no reason to live",
    "everyone would be better off without me", "no way out"
]

async def create_chat_message(user_id: str, message: str, is_user: bool = True) -> Dict[str, Any]:
    """Create a new chat message."""
    message_data = {
        "user_id": user_id,
        "message": message,
        "is_user": is_user,
        "timestamp": datetime.utcnow().isoformat()
    }

    chat_message = await create_item(chat_history_table, message_data, "message_id", "user_id")
    return chat_message

async def get_chat_history(user_id: str, limit: int = 20) -> List[Dict[str, Any]]:
    """Get chat history for a user."""
    # Get all chat messages for the user
    chat_messages = await query_items(
        chat_history_table,
        "user_id = :user_id",
        {":user_id": user_id},
        "UserIdIndex"
    )

    # Sort by timestamp (oldest first)
    chat_messages.sort(key=lambda x: x["timestamp"])

    # Apply limit (get the most recent messages)
    return chat_messages[-limit:]

async def get_user_context(user_id: str) -> Dict[str, Any]:
    """Get context about the user for personalized responses."""
    context = {}

    # Get user data
    try:
        from backend.db.dynamodb import get_user_by_id
        user = await get_user_by_id(user_id)
        if user:
            context["user_preferences"] = user.get("preferences", {})
    except Exception as e:
        print(f"Error getting user data: {e}")
        pass

    # Get recent mood entries
    try:
        mood_entries = await mood_service.list_mood_entries(user_id, limit=5)
        if mood_entries:
            context["recent_moods"] = mood_entries

            # Get mood statistics
            mood_stats = await mood_service.get_mood_statistics(user_id)
            context["mood_stats"] = mood_stats
    except Exception:
        # Continue even if mood data is not available
        pass

    # Get recent journal entries
    try:
        journal_entries = await journal_service.list_journal_entries(user_id, limit=3)
        if journal_entries:
            context["recent_journal_entries"] = journal_entries
            # Analyze journal entries for sentiment and keywords
            for entry in journal_entries:
                entry["sentiment"] = nlp_service.analyze_sentiment(entry["text"])
                entry["keywords"] = nlp_service.extract_keywords(entry["text"])
    except Exception:
        # Continue even if journal data is not available
        pass

    # Get medications
    try:
        medications = await medication_service.list_medications(user_id)
        if medications:
            context["medications"] = medications
    except Exception:
        # Continue even if medication data is not available
        pass

    # Get upcoming reminders
    try:
        reminders = await reminder_service.get_upcoming_reminders(user_id)
        if reminders:
            context["upcoming_reminders"] = reminders
    except Exception:
        # Continue even if reminder data is not available
        pass

    # Get recent assessment results - temporarily disabled until assessment_service is implemented
    # try:
    #     assessment_results = await assessment_service.get_assessment_history(user_id)
    #     if assessment_results:
    #         context["recent_assessments"] = assessment_results[:3]
    # except Exception:
    #     # Continue even if assessment data is not available
    #     pass

    return context

def detect_crisis(message: str) -> bool:
    """Detect if a message indicates a crisis situation."""
    message_lower = message.lower()
    for keyword in CRISIS_KEYWORDS:
        if keyword in message_lower:
            return True
    return False

def get_crisis_response() -> str:
    """Get a response for a crisis situation."""
    return """I'm concerned about what you've shared. If you're having thoughts of harming yourself or ending your life, please reach out for immediate help:

1. Call a crisis hotline:
   - National Suicide Prevention Lifeline: 1-800-273-8255
   - Crisis Text Line: Text HOME to 741741

2. Go to your nearest emergency room or call 911

3. Talk to a trusted friend, family member, or mental health professional

Your life matters, and help is available. Would you like me to provide more resources or support options?"""

async def generate_chatbot_response(user_id: str, user_message: str) -> str:
    """Generate a response from the chatbot."""
    # Check for crisis indicators
    if detect_crisis(user_message):
        response = get_crisis_response()

        # Save user message and bot response
        await create_chat_message(user_id, user_message, is_user=True)
        await create_chat_message(user_id, response, is_user=False)

        return response

    # Save user message
    await create_chat_message(user_id, user_message, is_user=True)

    # Get chat history
    chat_history = await get_chat_history(user_id)

    # Get user context
    user_context = await get_user_context(user_id)

    # Create prompt for the LLM
    prompt = _create_prompt(user_message, chat_history, user_context)

    # Get response from RAG
    response = get_rag_response(prompt, chat_history)

    # Save bot response
    await create_chat_message(user_id, response, is_user=False)

    return response

def _create_prompt(user_message: str, chat_history: List[Dict[str, Any]], user_context: Dict[str, Any]) -> str:
    """Create a prompt for the LLM based on user message, chat history, and context."""
    # Create a formatted user context
    formatted_context = "User Context:\n"

    # Add mood information
    if "recent_moods" in user_context and user_context["recent_moods"]:
        recent_mood = user_context["recent_moods"][0]
        formatted_context += f"- Recent mood: {recent_mood['mood_rating']}/10"
        if recent_mood.get("tags"):
            formatted_context += f" (Tags: {', '.join(recent_mood['tags'])})"
        formatted_context += "\n"

    if "mood_stats" in user_context:
        mood_stats = user_context["mood_stats"]
        formatted_context += f"- Average mood: {mood_stats['average_rating']:.1f}/10\n"

    # Add medication information
    if "medications" in user_context and user_context["medications"]:
        formatted_context += "- Medications:\n"
        for medication in user_context["medications"][:3]:  # Limit to 3 medications
            formatted_context += f"  * {medication['name']} ({medication['dosage']}, {medication['frequency']})\n"

    # Add reminder information
    if "upcoming_reminders" in user_context and user_context["upcoming_reminders"]:
        formatted_context += "- Upcoming medication reminders:\n"
        for reminder in user_context["upcoming_reminders"][:3]:  # Limit to 3 reminders
            formatted_context += f"  * {reminder['medication']['name']} at {reminder['scheduled_time']}\n"

    # Add assessment information - temporarily disabled until assessment_service is implemented
    # if "recent_assessments" in user_context and user_context["recent_assessments"]:
    #     recent_assessment = user_context["recent_assessments"][0]
    #     formatted_context += f"- Recent assessment: {recent_assessment['assessment_type']} - Score: {recent_assessment['score']} ({recent_assessment['interpretation']['label']})\n"

    # Create the final prompt
    prompt = f"""You are a supportive mental health assistant. Your goal is to provide empathetic, helpful responses to users who may be dealing with mental health challenges. Always be supportive, non-judgmental, and encouraging. Never provide medical advice or diagnoses, and always suggest professional help for serious concerns.

{formatted_context}

User message: {user_message}"""

    return prompt

async def get_personalized_recommendations(user_id: str) -> Dict[str, Any]:
    """Get personalized recommendations based on user data."""
    # Get user context
    user_context = await get_user_context(user_id)

    # Create recommendations based on context
    recommendations = {
        "coping_strategies": [],
        "resources": [],
        "activities": []
    }

    # Add coping strategies based on mood and assessments
    if "mood_stats" in user_context:
        mood_stats = user_context["mood_stats"]
        avg_mood = mood_stats["average_rating"]

        if avg_mood < 4:
            # Low mood recommendations
            recommendations["coping_strategies"].extend([
                "Practice deep breathing exercises",
                "Try a short mindfulness meditation",
                "Reach out to a friend or family member",
                "Consider speaking with a mental health professional"
            ])
            recommendations["activities"].extend([
                "Take a short walk outside",
                "Listen to uplifting music",
                "Write down three things you're grateful for"
            ])
        elif avg_mood < 7:
            # Moderate mood recommendations
            recommendations["coping_strategies"].extend([
                "Practice self-care activities",
                "Try journaling about your feelings",
                "Engage in light physical activity"
            ])
            recommendations["activities"].extend([
                "Do a hobby you enjoy",
                "Connect with a friend",
                "Try a new relaxation technique"
            ])
        else:
            # Good mood recommendations
            recommendations["coping_strategies"].extend([
                "Continue your positive habits",
                "Share your positive energy with others",
                "Reflect on what's working well for you"
            ])
            recommendations["activities"].extend([
                "Challenge yourself with a new activity",
                "Help someone else who might be struggling",
                "Set goals for maintaining your well-being"
            ])

    # Add resources based on assessments - temporarily disabled until assessment_service is implemented
    # if "recent_assessments" in user_context and user_context["recent_assessments"]:
    #     for assessment in user_context["recent_assessments"]:
    #         if assessment["assessment_type"] == "phq9" and assessment["score"] > 10:
    #             recommendations["resources"].extend([
    #                 {
    #                     "title": "Depression - National Institute of Mental Health",
    #                     "url": "https://www.nimh.nih.gov/health/topics/depression"
    #                 },
    #                 {
    #                     "title": "Depression Management Techniques",
    #                     "url": "https://www.helpguide.org/articles/depression/coping-with-depression.htm"
    #                 }
    #             ])
    #         elif assessment["assessment_type"] == "gad7" and assessment["score"] > 10:
    #             recommendations["resources"].extend([
    #                 {
    #                     "title": "Anxiety Disorders - National Institute of Mental Health",
    #                     "url": "https://www.nimh.nih.gov/health/topics/anxiety-disorders"
    #                 },
    #                 {
    #                     "title": "Anxiety Management Techniques",
    #                     "url": "https://www.helpguide.org/articles/anxiety/how-to-stop-worrying.htm"
    #                 }
    #             ])

    return recommendations

async def generate_weekly_report(user_id: str) -> str:
    """Generate a weekly report for a user."""
    # Get user context
    user_context = await get_user_context(user_id)

    # Get data for the past week
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=7)

    # Get mood entries for the past week
    mood_entries = await mood_service.list_mood_entries(
        user_id,
        limit=100,
        start_date=start_date.isoformat(),
        end_date=end_date.isoformat()
    )

    # Get journal entries for the past week
    journal_entries = await journal_service.list_journal_entries(
        user_id,
        limit=100,
        start_date=start_date.isoformat(),
        end_date=end_date.isoformat()
    )

    # Get medication adherence for the past week
    reminders = await reminder_service.list_reminders(
        user_id
    )

    # Calculate medication adherence
    total_reminders = len(reminders)
    completed_reminders = len([r for r in reminders if r["status"] == "completed"])
    adherence_rate = (completed_reminders / total_reminders) * 100 if total_reminders > 0 else 0

    # Create a prompt for the weekly report
    prompt = f"""Generate a weekly mental health report for a user based on the following data:

Mood Entries (past week):
{len(mood_entries)} entries
Average mood rating: {sum([entry["mood_rating"] for entry in mood_entries]) / len(mood_entries) if mood_entries else 0:.1f}/10

Journal Entries (past week):
{len(journal_entries)} entries

Medication Adherence (past week):
{adherence_rate:.1f}% ({completed_reminders}/{total_reminders} reminders completed)

Create a supportive, encouraging weekly report that summarizes this data and provides personalized recommendations for the coming week. Include:
1. A summary of the user's mood and journaling patterns
2. Recognition of their medication adherence
3. Specific, actionable suggestions for the coming week
4. Encouragement and positive reinforcement

Format the report with clear sections and bullet points where appropriate."""

    # Get response from LLM
    from backend.llm import get_llm_response
    report = get_llm_response(prompt)
    return report

async def generate_ai_suggestions(user_id: str) -> Dict[str, Any]:
    """Generate AI suggestions based on user context."""
    # Get user context
    user_context = await get_user_context(user_id)

    # Create suggestions based on context
    suggestions = {}

    # Add suggestions based on mood
    if "recent_moods" in user_context and user_context["recent_moods"]:
        recent_mood = user_context["recent_moods"][0]
        if recent_mood["mood_rating"] < 4:
            suggestions["journal_prompt"] = "What is causing you to feel this way?"
            suggestions["coping_tip"] = "Try a short mindfulness meditation."
            suggestions["motivational_content"] = "Remember that it's okay to have bad days."
        elif recent_mood["mood_rating"] > 7:
            suggestions["journal_prompt"] = "What is making you feel so good today?"
            suggestions["coping_tip"] = "Continue your positive habits."
            suggestions["motivational_content"] = "Share your positive energy with others."
        else:
            suggestions["journal_prompt"] = "Reflect on your day and identify any positive or negative experiences."
            suggestions["coping_tip"] = "Practice self-care activities."
            suggestions["motivational_content"] = "Focus on the present moment."

    # Add suggestions based on medication adherence
    if "medications" in user_context and user_context["medications"]:
        medications = user_context["medications"]
        for medication in medications:
            # Check if medication has a name
            if "name" in medication:
                suggestions["medication_tip"] = f"Remember to take your {medication['name']} as prescribed."
                break

    return suggestions


async def get_visualization_data(user_id: str, data_type: str) -> List[Dict[str, Any]]:
    """Get data for visualizations."""
    if data_type == "mood":
        data = await mood_service.list_mood_entries(user_id)
    elif data_type == "medication":
        data = await reminder_service.list_reminders(user_id)
    elif data_type == "journal":
        data = await journal_service.list_journal_entries(user_id)
    else:
        raise ValueError("Invalid data type")

    return data


async def submit_feedback(user_id: str, feedback: str) -> None:
    """Submit feedback on AI suggestions."""
    # Store feedback in DynamoDB
    feedback_data = {
        "user_id": user_id,
        "feedback": feedback,
        "timestamp": datetime.utcnow().isoformat()
    }
    await create_item(feedback_table, feedback_data, "feedback_id", "user_id")
