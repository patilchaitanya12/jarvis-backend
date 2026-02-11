# app/routers/chat.py
from fastapi import APIRouter
from app.schemas.chat import ChatRequest, ChatResponse
from app.brain import get_response

router = APIRouter(prefix="/chat", tags=["Chat"])

@router.post("", response_model=ChatResponse)
def chat(payload: ChatRequest):
    response, confidence, source = get_response(payload.message)

    return ChatResponse(
        response=response,
        confidence=round(confidence, 2),
        source=source
    )
