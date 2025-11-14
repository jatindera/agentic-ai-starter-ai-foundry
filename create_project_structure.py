import os

BASE_DIR = "."

# Folders to create (backend now enterprise-ready)
FOLDERS = [
    # Frontend
    # "frontend/app/chat",
    # "frontend/app/api",
    # "frontend/components",
    # "frontend/lib",
    # "frontend/styles",
    # "frontend/public",

    # Backend
    "backend/app/api/routes",
    "backend/app/core",
    "backend/app/models/schemas",
    "backend/app/models/orm",
    "backend/app/db",
    "backend/app/repositories",
    "backend/app/services",
    "backend/app/agents/maf_agent",
    "backend/app/mcp/schemas",
    "backend/app/utils",
    "backend/app",
    "backend/tests",

    # Docs & Scripts
    "docs",
    "scripts",
]

# Files to create
FILES = [
    # Frontend
    # "frontend/app/layout.tsx",
    # "frontend/app/page.tsx",
    # "frontend/lib/axios.ts",
    # "frontend/lib/auth.ts",
    # "frontend/components/ChatWindow.tsx",
    # "frontend/components/MessageBubble.tsx",
    # "frontend/components/Loader.tsx",
    # "frontend/package.json",
    # "frontend/next.config.js",

    # Backend API routes
    "backend/app/api/routes/chat.py",
    "backend/app/api/routes/health.py",

    # Backend Core
    "backend/app/core/config.py",
    "backend/app/core/logging_config.py",
    "backend/app/core/security.py",

    # Backend Models
    "backend/app/models/schemas/user.py",
    "backend/app/models/schemas/chat.py",
    "backend/app/models/orm/user.py",
    "backend/app/models/orm/chat.py",

    # DB Layer
    "backend/app/db/session.py",
    "backend/app/db/config.py",

    # Repository Layer
    "backend/app/repositories/base_repository.py",
    "backend/app/repositories/user_repository.py",

    # Services
    "backend/app/services/agent_service.py",
    "backend/app/services/maf_agent_service.py",
    "backend/app/services/foundry_agent_service.py",
    "backend/app/services/mcp_client_service.py",
    "backend/app/services/model_service.py",

    # MAF Agent
    "backend/app/agents/maf_agent/agent.py",
    "backend/app/agents/maf_agent/tools.py",
    "backend/app/agents/maf_agent/planner.py",
    "backend/app/agents/maf_agent/memory.py",

    # MCP
    "backend/app/mcp/client.py",
    "backend/app/mcp/schemas/mcp_request.py",
    "backend/app/mcp/schemas/mcp_response.py",

    # Utils
    "backend/app/utils/http_client.py",
    "backend/app/utils/cache.py",
    "backend/app/utils/telemetry.py",

    # Tests
    "backend/tests/test_chat.py",
    "backend/tests/test_mcp_client.py",

    # Main
    "backend/app/main.py",

    # Docs
    "docs/architecture-overview.md",
    "docs/maf-agent-design.md",
    "docs/mcp-integration.md",
    "docs/foundry-agent.md",
    "docs/sequence-diagram.md",
    "docs/api-spec.md",

    # Scripts
    "scripts/start-backend.sh",
    "scripts/start-frontend.sh",
    "scripts/setup-env.sh",

    # Root files
    ".env.example",
    "README.md",
]

def create_structure():
    print(f"📁 Creating project at: {BASE_DIR}\n")

    # Create folders
    for folder in FOLDERS:
        path = os.path.join(BASE_DIR, folder)
        os.makedirs(path, exist_ok=True)
        print(f"📂 Created folder: {path}")

        # Add __init__.py to every folder (Python package)
        init_file = os.path.join(path, "__init__.py")
        with open(init_file, "w") as f:
            f.write("")
        print(f"📄 Added __init__.py in: {path}")

    # Create files
    for file in FILES:
        path = os.path.join(BASE_DIR, file)
        with open(path, "w", encoding="utf-8") as f:
            f.write("")
        print(f"📄 Created file: {path}")

    print("\n🎉 SUCCESS! Production-ready folder structure created.")
    print("👉 Next step: `cd backend && uv init`\n")

if __name__ == "__main__":
    create_structure()
