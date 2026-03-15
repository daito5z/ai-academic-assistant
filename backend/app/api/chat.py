from fastapi import APIRouter  # type: ignore
from app.services.llm_service import LLMService
from app.models.schemas import ChatRequest, ChatResponse

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):

    reply = LLMService.generate_response(request.message)

    return ChatResponse(response=reply)
