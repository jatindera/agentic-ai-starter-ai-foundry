import os
from agent_framework.azure import AzureOpenAIChatClient
from agent_framework import ChatMessage, TextContent, Role
from azure.identity.aio import AzureCliCredential
from app.services.agent_provision_service import AgentProvisionService

PROJECT_ENDPOINT = os.getenv("AZURE_AI_PROJECT_ENDPOINT")


class MAF_AgentService:
    """Production-ready MAF agent wrapper (latest agent-framework)."""

    def __init__(self):
        self.provision_service = AgentProvisionService()
        self.agent_name = "chat-agent"
        self.instructions = "You are a helpful AI assistant."

    async def get_agent(self):
        """Return the Azure Foundry agent ID, creating the agent if needed."""
        agent_id = await self.provision_service.get_or_create_agent(
            agent_name=self.agent_name,
            instructions=self.instructions
        )
        return agent_id

    async def get_response(self, message: str) -> str:
        agent_id = await self.get_agent()

        async with AzureCliCredential() as credential:

            # Create Chat Client (this replaces ChatAgent)
            chat_client = AzureOpenAIChatClient(
                credential=credential,
                project_endpoint=PROJECT_ENDPOINT,
                agent_id=agent_id
            )

            # Build message
            chat_message = ChatMessage(
                role=Role.USER,
                contents=[TextContent(text=message)],
            )

            # Invoke agent
            result = await chat_client.run(chat_message)

            # Return final text
            return result.text if hasattr(result, "text") else ""
