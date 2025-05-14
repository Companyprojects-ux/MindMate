from langchain_google_genai import ChatGoogleGenerativeAI
from backend.config import settings

def get_llm_response(prompt: str):
    """
    This function takes a prompt and returns a response from the Gemini LLM.
    """
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-001", google_api_key=settings.GEMINI_API_KEY)
    response = llm.invoke(prompt)
    return response.content

def get_personalized_coping_strategies(user_input: str):
    """
    This function takes user input and returns a list of personalized coping strategies.
    """
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-001", google_api_key=settings.GEMINI_API_KEY)
    prompt = f"Provide a list of personalized coping strategies for the following situation: {user_input}"
    response = llm.invoke(prompt)
    return response.content
