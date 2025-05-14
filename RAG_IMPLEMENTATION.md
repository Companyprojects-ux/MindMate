# RAG Implementation Details

This document provides technical details about the Retrieval-Augmented Generation (RAG) implementation in the Mental Health Support application.

## Overview

The RAG system enhances the AI chatbot by providing evidence-based responses from trusted mental health resources. It combines the power of large language models with information retrieval to generate more accurate and reliable responses.

## Components

### 1. Document Processing

The system processes PDF documents from trusted mental health sources:

```python
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Load PDF documents
knowledge_base_dir = "knowledge_base"
pdf_files = [f for f in os.listdir(knowledge_base_dir) if f.endswith('.pdf')]

documents = []
for pdf_file in pdf_files:
    loader = PyPDFLoader(os.path.join(knowledge_base_dir, pdf_file))
    documents.extend(loader.load())
```

### 2. Text Chunking

Documents are split into manageable chunks for better retrieval:

```python
# Split documents into chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    length_function=len
)
chunks = text_splitter.split_documents(documents)
```

### 3. Embedding Generation

Text chunks are converted into vector embeddings:

```python
from langchain_community.embeddings import HuggingFaceEmbeddings

# Generate embeddings
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
```

### 4. Vector Storage

Embeddings are stored in a FAISS vector database:

```python
from langchain_community.vectorstores import FAISS

# Create vector store
vector_store = FAISS.from_documents(chunks, embeddings)
```

### 5. Similarity Search

When a user asks a question, the system retrieves the most relevant information:

```python
# Retrieve relevant documents
relevant_docs = vector_store.similarity_search(query, k=3)
```

### 6. Response Generation

The LLM generates a response based on the retrieved information and user context:

```python
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import RetrievalQA

# Initialize LLM
llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=settings.GOOGLE_API_KEY)

# Create RAG chain
rag_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=vector_store.as_retriever(),
    return_source_documents=True
)

# Generate response
response = rag_chain.invoke({"query": query})
```

## Integration with User Context

The RAG system is enhanced with user-specific context to provide personalized responses:

```python
def get_rag_response(prompt: str, chat_history: List[Dict[str, Any]]) -> str:
    # Format chat history
    formatted_history = format_chat_history(chat_history)
    
    # Combine prompt with chat history
    full_prompt = f"{formatted_history}\n\n{prompt}"
    
    # Get response from RAG
    response = rag_chain.invoke({"query": full_prompt})
    
    return response["result"]
```

## Crisis Detection

The system includes crisis detection to identify potential mental health emergencies:

```python
CRISIS_KEYWORDS = [
    "suicide", "kill myself", "end my life", "want to die", "don't want to live",
    "self-harm", "hurt myself", "cutting myself", "harming myself",
    "hopeless", "worthless", "can't go on", "no reason to live",
    "everyone would be better off without me", "no way out"
]

def detect_crisis(message: str) -> bool:
    message_lower = message.lower()
    for keyword in CRISIS_KEYWORDS:
        if keyword in message_lower:
            return True
    return False
```

## Performance Considerations

- **Caching**: Embeddings are cached to improve performance
- **Chunking Strategy**: Chunk size and overlap are optimized for mental health content
- **Model Selection**: Using smaller embedding models for faster retrieval
- **Asynchronous Processing**: Using async functions for better responsiveness

## Future Improvements

1. **Incremental Updates**: Add capability to update the knowledge base without reprocessing all documents
2. **Multi-modal Support**: Extend to handle images and diagrams from mental health resources
3. **Hybrid Search**: Combine semantic search with keyword-based search for better results
4. **User Feedback Loop**: Incorporate user feedback to improve retrieval quality
5. **Cross-lingual Support**: Add support for multiple languages
