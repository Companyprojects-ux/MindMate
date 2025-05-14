"""
RAG (Retrieval-Augmented Generation) pipeline for the knowledge base.
"""
import os
from typing import List, Dict, Any, Optional
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from backend.config import settings

# Path to the knowledge base directory
KNOWLEDGE_BASE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "knowledge_base")

# Global variable to store the vector store
_vector_store = None

def get_vector_store():
    """Get the vector store, creating it if it doesn't exist."""
    global _vector_store
    if _vector_store is None:
        _vector_store = create_vector_store()
    return _vector_store

def create_vector_store():
    """Create a vector store from the knowledge base documents."""
    # Load all PDF documents from the knowledge base directory
    documents = []
    for filename in os.listdir(KNOWLEDGE_BASE_DIR):
        if filename.endswith(".pdf"):
            file_path = os.path.join(KNOWLEDGE_BASE_DIR, filename)
            loader = PyPDFLoader(file_path)
            documents.extend(loader.load())
    
    # Split the documents into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
    )
    chunks = text_splitter.split_documents(documents)
    
    # Create embeddings and store them in a vector store
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=settings.GEMINI_API_KEY)
    vector_store = FAISS.from_documents(chunks, embeddings)
    
    return vector_store

def get_relevant_context(query: str, k: int = 5) -> str:
    """Get relevant context for a query from the knowledge base."""
    vector_store = get_vector_store()
    docs = vector_store.similarity_search(query, k=k)
    
    # Combine the content of the retrieved documents
    context = "\n\n".join([doc.page_content for doc in docs])
    
    return context

def get_rag_response(query: str, chat_history: List[Dict[str, Any]] = None) -> str:
    """Get a response using RAG."""
    # Get relevant context from the knowledge base
    context = get_relevant_context(query)
    
    # Create a prompt that includes the context
    prompt = f"""You are a mental health support assistant. Use the following information from trusted sources to provide an evidence-based response to the user's query.

Context from trusted sources:
{context}

"""
    
    # Add chat history if provided
    if chat_history:
        prompt += "Chat history:\n"
        for message in chat_history:
            role = "User" if message["is_user"] else "Assistant"
            prompt += f"{role}: {message['message']}\n"
    
    # Add the user's query
    prompt += f"\nUser: {query}\nAssistant:"
    
    # Get response from LLM
    from backend.llm import get_llm_response
    response = get_llm_response(prompt)
    
    return response
