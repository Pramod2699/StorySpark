from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Add the project root to the path to ensure 'src' can be found
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

# Import all necessary components from your project structure
from src.handlers.AnswerGenerator import AnswerGenerator
from src.utils.Logger import Logger
from src.config.ConfigHelper import ConfigHelper

# --- 1. Application and Dependency Initialization ---
app = FastAPI(
    title="AI Essay Brainstormer API",
    description="API for handling essay brainstorming sessions.",
    version="1.0.0"
)

# These dependencies are created once when the server starts up.
logger = Logger()
config = ConfigHelper().config
# NOTE: This creates a single, global instance of AnswerGenerator.
# For a production app with multiple simultaneous users, you would need to
# manage a separate instance for each user's session (e.g., using a dictionary
# mapping session IDs to generator instances). For this prototype, this is fine.
answer_generator = AnswerGenerator()

# --- 2. CORS (Cross-Origin Resource Sharing) Middleware ---
# This is a security feature that is essential for web apps. It tells the
# server that it's okay to accept requests from a different "origin"
# (in this case, your local index.html file).
origins = [
    "null",  # Allows requests from local `file:///` URLs
    "http://127.0.0.1:5500", # A common port for live server extensions
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], # Allow all HTTP methods (POST, GET, etc.)
    allow_headers=["*"], # Allow all request headers
)

# --- 3. Pydantic Models for API Data Validation ---
# These classes define the expected structure of JSON data for requests and responses.
# FastAPI uses them to automatically validate incoming data and serialize outgoing data.
class StartSessionRequest(BaseModel):
    name: str
    stream: str
    major: str
    college: str

class ChatRequest(BaseModel):
    message: str

class ApiResponse(BaseModel):
    response: str
    is_complete: bool

# --- 4. API Endpoints ---
# These are the functions that handle incoming HTTP requests.
@app.post("/start-session", response_model=ApiResponse)
async def start_session(request: StartSessionRequest):
    """
    Endpoint to start a new brainstorming session.
    Receives user details and returns the first personalized question.
    """
    logger.info(f"Received request to start a new session for user: {request.name}")
    
    first_question = answer_generator.start_session(
        name=request.name,
        stream=request.stream,
        major=request.major,
        college=request.college
    )
    
    return ApiResponse(response=first_question, is_complete=False)

@app.post("/chat", response_model=ApiResponse)
async def chat(request: ChatRequest):
    """
    Endpoint to handle a message during an ongoing conversation.
    Receives the user's answer and returns the AI's next response.
    """
    logger.info(f"Received chat message: '{request.message[:50]}...'")
    
    ai_response = answer_generator.chat(request.message)
    is_complete = answer_generator.conversation_stage == "COMPLETED"
    
    return ApiResponse(response=ai_response, is_complete=is_complete)

