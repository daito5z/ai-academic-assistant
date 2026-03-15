from pydantic import BaseModel  # type: ignore


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    response: str
