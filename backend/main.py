from fastapi import FastAPI, Request, status, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from backend.api import auth, medications, reminders, moods, journal, ai
from backend.config import settings
from backend.core.exceptions import AppException
from backend.llm import get_llm_response, get_personalized_coping_strategies

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Mental Health Support Application with Medicine Reminder Functionality",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development, restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Exception handlers
@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": exc.errors()},
    )

# Health check endpoint
@app.get("/api/health", tags=["Health"])
async def health_check():
    return {"status": "healthy"}

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(medications.router, prefix="/api/medications", tags=["Medications"])
app.include_router(reminders.router, prefix="/api/reminders", tags=["Reminders"])
app.include_router(moods.router, prefix="/api/moods", tags=["Mood Tracking"])
app.include_router(journal.router, prefix="/api/journal", tags=["Journal"])
app.include_router(ai.router, prefix="/api/ai", tags=["AI Support"])

# Legacy endpoints
@app.get("/mental_health_support", tags=["Mental Health"])
async def mental_health_support(prompt: str = Query(..., description="The prompt for the LLM")):
    """
    This endpoint takes a prompt and returns a response from the LLM.
    """
    response = get_llm_response(prompt)
    return {"response": response}

@app.get("/coping_strategies", tags=["Mental Health"])
async def coping_strategies(user_input: str = Query(..., description="The user's input")):
    """
    This endpoint takes user input and returns a list of personalized coping strategies.
    """
    strategies = get_personalized_coping_strategies(user_input)
    return {"strategies": strategies}
