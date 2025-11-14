import os
from azure.identity.aio import AzureCliCredential
from azure.ai.projects.aio import AIProjectClient
from dotenv import load_dotenv

load_dotenv()

PROJECT_ENDPOINT = os.getenv("AZURE_AI_PROJECT_ENDPOINT")
MODEL_DEPLOYMENT = os.getenv("AZURE_AI_MODEL_DEPLOYMENT_NAME")

class AzureFoundryClient:
    """Client wrapper for Azure AI Foundry."""

    @staticmethod
    async def list_agents():
        async with AzureCliCredential() as credential:
            async with AIProjectClient(
                endpoint=PROJECT_ENDPOINT,
                credential=credential
            ) as project_client:
                agents = await project_client.agents.list_agents()
                return agents, project_client

    @staticmethod
    async def create_agent(agent_name: str, instructions: str):
        async with AzureCliCredential() as credential:
            async with AIProjectClient(
                endpoint=PROJECT_ENDPOINT,
                credential=credential
            ) as project_client:

                created_agent = await project_client.agents.create_agent(
                    model=MODEL_DEPLOYMENT,
                    name=agent_name,
                    instructions=instructions,
                )

                return created_agent, project_client
