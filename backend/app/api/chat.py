from fastapi import APIRouter
from app.models.schemas import ChatRequest, ChatResponse
from app.services.llm_service import LLMService
import uuid

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):

    session_id = request.session_id or str(uuid.uuid4())

    reply = LLMService.generate_response(request.message, session_id)

    return ChatResponse(
        response=reply,
        session_id=session_id
    )
