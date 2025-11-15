from app.repositories.agent_repository import AgentRepository
from app.services.azure_foundry_client import AzureFoundryClient
from app.db.session import SessionLocal

class AgentProvisionService:
    def __init__(self):
        self.repo = AgentRepository()

    async def get_or_create_agent(self, name: str, instructions: str) -> str:
        db = SessionLocal()
        try:
            existing = self.repo.get_agent(db, name)
        finally:
            db.close()

        if existing:
            return existing.agent_id

        # Create agent in Foundry
        created_agent = await AzureFoundryClient.create_agent(
            name=name,
            instructions=instructions
        )

        # Save agent to DB
        db = SessionLocal()
        try:
            self.repo.save_agent(db, name, created_agent.id)
        finally:
            db.close()

        return created_agent.id
