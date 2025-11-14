import json
import os
from pathlib import Path

REGISTRY_FILE = Path("backend/app_data/agent_registry.json")
REGISTRY_FILE.parent.mkdir(parents=True, exist_ok=True)

class AgentRegistry:
    """Handles persistent storage of Azure AI Foundry agent IDs locally."""

    @staticmethod
    def load_agent_id(agent_name: str) -> str | None:
        if not REGISTRY_FILE.exists():
            return None

        try:
            data = json.loads(REGISTRY_FILE.read_text())
            return data.get(agent_name)
        except Exception:
            return None

    @staticmethod
    def save_agent_id(agent_name: str, agent_id: str):
        data = {}

        if REGISTRY_FILE.exists():
            try:
                data = json.loads(REGISTRY_FILE.read_text())
            except Exception:
                pass

        data[agent_name] = agent_id
        REGISTRY_FILE.write_text(json.dumps(data, indent=4))
