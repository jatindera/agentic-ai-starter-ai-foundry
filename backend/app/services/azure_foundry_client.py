import os
from azure.ai.projects.aio import AIProjectClient
from azure.identity.aio import DefaultAzureCredential
from dotenv import load_dotenv

load_dotenv()

PROJECT_ENDPOINT = os.getenv("AZURE_AI_PROJECT_ENDPOINT")
MODEL = os.getenv("AZURE_AI_MODEL_DEPLOYMENT_NAME")


class AzureFoundryClient:
    _client = None
    _credential = None

    @classmethod
    async def get_client(cls) -> AIProjectClient:
        if cls._client:
            return cls._client

        cls._credential = DefaultAzureCredential()
        cls._client = AIProjectClient(
            endpoint=PROJECT_ENDPOINT,
            credential=cls._credential
        )
        return cls._client

    @classmethod
    async def create_agent(cls, name: str, instructions: str):
        client = await cls.get_client()

        return await client.agents.create_agent(
            model=MODEL,
            name=name,
            instructions=instructions
        )
