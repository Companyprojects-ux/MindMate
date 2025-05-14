"""
AI API endpoints.
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from backend.services import ai_service, recommendation_service, mood_service, journal_service
from backend.core.dependencies import get_current_user

router = APIRouter()

class ChatMessage(BaseModel):
    """Chat message schema."""
    message: str

class ChatResponse(BaseModel):
    """Chat response schema."""
    response: str

class ChatHistoryItem(BaseModel):
    """Chat history item schema."""
    message_id: str
    message: str
    is_user: bool
    timestamp: str

class JournalPrompt(BaseModel):
    """Journal prompt schema."""
    title: str
    prompt: str

class CopingStrategy(BaseModel):
    """Coping strategy schema."""
    title: str
    description: str

class RecommendationResponse(BaseModel):
    """Recommendation response schema."""
    journal_prompts: List[JournalPrompt]
    coping_strategies: List[CopingStrategy]
    timestamp: str
    user_id: str

class Recommendations(BaseModel):
    """Legacy recommendations schema."""
    coping_strategies: List[str]
    resources: List[Dict[str, str]]
    activities: List[str]

class WeeklyReport(BaseModel):
    """Weekly report schema."""
    report: str

@router.post("/chat", response_model=ChatResponse)
async def chat_with_ai(
    message_data: ChatMessage,
    current_user: dict = Depends(get_current_user)
):
    """Send a message to the chatbot."""
    response = await ai_service.generate_chatbot_response(
        current_user["user_id"],
        message_data.message
    )
    return {"response": response}

@router.get("/chat/history", response_model=List[ChatHistoryItem])
async def get_chat_history(
    limit: int = Query(20, ge=1, le=100),
    current_user: dict = Depends(get_current_user)
):
    """Get chat history for the current user."""
    chat_history = await ai_service.get_chat_history(current_user["user_id"], limit)

    # Format response
    history_items = [
        {
            "message_id": message["message_id"],
            "message": message["message"],
            "is_user": message["is_user"],
            "timestamp": message["timestamp"]
        }
        for message in chat_history
    ]

    return history_items

@router.get("/legacy-recommendations", response_model=Recommendations)
async def get_legacy_recommendations(
    current_user: dict = Depends(get_current_user)
):
    """Get personalized recommendations for the current user (legacy endpoint)."""
    recommendations = await ai_service.get_personalized_recommendations(current_user["user_id"])
    return recommendations

@router.get("/weekly-report", response_model=WeeklyReport)
async def get_weekly_report(
    current_user: dict = Depends(get_current_user)
):
    """Get weekly report for the current user."""
    report = await ai_service.generate_weekly_report(current_user["user_id"])
    return {"report": report}

@router.get("/recommendations", response_model=RecommendationResponse)
async def get_ai_recommendations(
    current_user: dict = Depends(get_current_user)
):
    """Get AI-generated recommendations based on user data."""
    try:
        # Get user data
        mood_data = await mood_service.list_mood_entries(current_user["user_id"])
        journal_data = await journal_service.list_journal_entries(current_user["user_id"])

        # Generate personalized recommendations
        recommendations = await recommendation_service.generate_recommendations(
            current_user["user_id"], mood_data, journal_data
        )

        return recommendations
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/suggestions")
async def get_ai_suggestions(
    current_user: dict = Depends(get_current_user)
):
    """Get AI suggestions based on user context (legacy endpoint)."""
    suggestions = await ai_service.generate_ai_suggestions(current_user["user_id"])
    return suggestions

@router.get("/visualization_data")
async def get_visualization_data(
    current_user: dict = Depends(get_current_user),
    data_type: str = Query(..., description="Type of data to retrieve (mood, medication, journal)")
):
    """Get data for visualizations."""
    data = await ai_service.get_visualization_data(current_user["user_id"], data_type)
    return data

@router.post("/feedback")
async def submit_feedback(
    feedback: str = Query(..., description="User feedback on AI suggestions"),
    current_user: dict = Depends(get_current_user)
):
    """Submit feedback on AI suggestions."""
    await ai_service.submit_feedback(current_user["user_id"], feedback)
    return {"message": "Feedback submitted successfully"}
