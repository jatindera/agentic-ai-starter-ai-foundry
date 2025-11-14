from app.services.maf_agent_service import MAF_AgentService
from app.services.model_service import ModelService

class AgentService:
    def __init__(self):
        self.model_service = ModelService()
        self.agent = MAF_AgentService()

    async def process_message(self, message: str) -> str:
        # Here you can add: logging, preprocessing, user session context, etc.
        response = await self.agent.get_response(message)
        return response
