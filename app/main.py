from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
from app.utils import get_answer_and_links
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="TDS Virtual TA",
    description="API for answering Tools in Data Science questions",
    version="1.0"
)

# Optional: Allow frontend apps to access this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to specific origin in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request model
class Query(BaseModel):
    question: str
    image: Optional[str] = None

# Link object in the response
class Link(BaseModel):
    url: str
    text: str

# Full response model
class Response(BaseModel):
    answer: str
    links: List[Link]

# Main endpoint
@app.post("/api/", response_model=Response)
async def get_response(query: Query):
    logger.info(f"Received question: {query.question}")
    answer, links = get_answer_and_links(query.question, query.image)
    logger.info("Sending response")
    return Response(answer=answer, links=links)
