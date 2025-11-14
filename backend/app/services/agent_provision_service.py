from app.repositories.agent_repository import AgentRepository
from app.services.azure_foundry_client import AzureFoundryClient
from app.db.session import SessionLocal


class AgentProvisionService:

    def __init__(self):
        self.repo = AgentRepository()

    def get_db(self):
        """Local DB session for sync SQLAlchemy."""
        return SessionLocal()

    async def get_or_create_agent(self, agent_name: str, instructions: str) -> str:
        """
        Get agent from DB → Azure AI Foundry → Create if needed.
        This remains async because Azure Foundry calls are async.
        """

        # 1. Check SQL DB (sync)
        db = self.get_db()
        try:
            existing = self.repo.get_agent(db, agent_name)
        finally:
            db.close()

        if existing:
            return existing.agent_id

        # 2. Check Azure AI Foundry (async)
        agents, project_client = await AzureFoundryClient.list_agents()
        for agent in agents:
            if agent.name.lower() == agent_name.lower():

                # Save to DB
                db = self.get_db()
                try:
                    self.repo.save_agent(db, agent_name, agent.id)
                finally:
                    db.close()

                return agent.id

        # 3. Create agent in Azure Foundry (async)
        created_agent, project_client = await AzureFoundryClient.create_agent(
            agent_name=agent_name,
            instructions=instructions,
        )

        # Store in DB
        db = self.get_db()
        try:
            self.repo.save_agent(db, agent_name, created_agent.id)
        finally:
            db.close()

        return created_agent.id
