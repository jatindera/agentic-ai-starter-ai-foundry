import os
from dotenv import load_dotenv

from app.services.agent_provision_service import AgentProvisionService
from app.services.azure_foundry_client import AzureFoundryClient

load_dotenv()


class MAF_AgentService:
    """
    Production-ready, lazy-agent Azure Foundry wrapper.
    - Creates agent only once (stored in DB)
    - Creates a thread per conversation
    - Sends message → runs agent → reads response
    """

    def __init__(self):
        self.provision_service = AgentProvisionService()
        self.agent_name = "chat-agent"
        self.instructions = "You are a helpful AI assistant."

    async def get_agent(self) -> str:
        """
        Lazy-creates agent if not existing.
        Always returns Foundry agent ID.
        """
        return await self.provision_service.get_or_create_agent(
            name=self.agent_name,
            instructions=self.instructions
        )

    async def get_response(self, message: str) -> str:
        """
        Sends a user message to Foundry agent and returns reply.
        """
        # 1. Ensure agent exists
        agent_id = await self.get_agent()

        # 2. Get Foundry project client (centralized)
        client = await AzureFoundryClient.get_client()

        # 3. Create thread
        thread = await client.agents.threads.create()

        # 4. Add user message
        await client.agents.messages.create(
            thread_id=thread.id,
            role="user",
            content=message,
        )

        # 5. Execute agent
        run = await client.agents.runs.create_and_process(
            thread_id=thread.id,
            agent_id=agent_id
        )

        if run.status == "failed":
            return f"Agent failed: {run.last_error}"

        # 6. Retrieve messages (ASC → last message is agent reply)
        messages = client.agents.messages.list(
            thread_id=thread.id,
            order="asc"
        )

        final_text = ""

        async for m in messages:
            if getattr(m, "text_messages", None):
                final_text = m.text_messages[-1].text.value

        return final_text
