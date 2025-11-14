from fastapi import APIRouter
from pydantic import BaseModel
from app.services.agent_service import AgentService

router = APIRouter()
agent_service = AgentService()

class ChatRequest(BaseModel):
    message: str

@router.post("/")
async def chat(request: ChatRequest):
    response = await agent_service.process_message(request.message)
    return {"reply": response}
