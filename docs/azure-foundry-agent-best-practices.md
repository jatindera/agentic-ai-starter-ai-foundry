# 📘 Azure AI Foundry Agent – Backend Integration Best Practices

### *FastAPI + Azure AI Project Client (AI Foundry) – Recommended Architecture & Implementation Guide*

This document describes the **best practices** for integrating **Azure AI Foundry (AIProjectClient)** into a FastAPI backend. It includes:

* Architecture overview
* Why the AI client should be a singleton
* Common pitfalls
* Correct implementation
* Annotated code examples
* Security & performance considerations

---

## 1. 🧩 Introduction

Microsoft’s **Azure AI Project Client** (`AIProjectClient`) provides programmatic access to Agents, Threads, Messages, and Runs inside Azure AI Foundry.

When integrating this client into a backend application (like FastAPI), proper lifecycle management is critical for:

* Performance
* Stability
* Token handling
* Reliability
* Cost optimization

This document defines the **recommended enterprise pattern**.

---

## 2. 🚫 What Azure AI Client Is *Not*

It is important to understand that `AIProjectClient` is **not a database connection**.

❌ It does **not** maintain a persistent TCP socket
❌ It does **not** hold long-lived sessions
❌ It does **not** require manual `.close()`
❌ It does **not** get “stale”
❌ It does **not** overload with reuse

It behaves like:

👉 **A stateless HTTP client wrapper that internally uses pooled HTTP connections.**

---

## 3. 🟢 What Azure AI Client *Is*

✔ Lightweight
✔ Thread-safe
✔ Designed to be **long-lived**
✔ Automatically refreshes tokens
✔ Automatically manages HTTP session pools

From Microsoft SDK guidelines:

> **“Azure SDK clients are thread-safe, long-lived objects. Reuse a single client instance rather than instantiating per API call.”**

---

## 4. 🎯 Why You Should Reuse a Singleton Client

### ✅ 4.1. Client creation is expensive

Creating a new client requires:

* Building identity via `DefaultAzureCredential`
* Performing environment detection
* Initializing token provider
* Creating HTTP session pools

Doing this per request severely impacts performance.

---

### ✅ 4.2. Reuse gives better performance

One shared client provides:

* Persistent HTTP connection pool
* Zero unnecessary authentication calls
* Zero TLS negotiation per request
* Faster response times
* Lower CPU and memory usage

---

### ✅ 4.3. Avoids rate-limiting & 429 errors

Spamming Azure with tens of client creations per second can cause:

* Token acquisition throttling
* Too many HTTP connection attempts
* Azure 429: "Rate limit exceeded"

---

### ✅ 4.4. Automatic token refresh

A long-lived client automatically:

* Detects expired tokens
* Obtains new tokens
* Retries operations

No manual code needed.

---

## 5. 🏗 Recommended Architecture

```
               ┌──────────────────────────┐
               │        FastAPI App        │
               └──────────────────────────┘
                          │
                          ▼
             ┌──────────────────────────────┐
             │     MAF_AgentService          │
             │  (one instance per request)   │
             └──────────────────────────────┘
                          │
                          ▼
             ┌──────────────────────────────┐
             │  AIProjectClient Singleton    │
             │  - Created once               │
             │  - Reused across requests     │
             └──────────────────────────────┘
                          │
                          ▼
                Azure AI Foundry API
```

---

## 6. 🧱 Recommended Implementation

### ✔ Singleton per-process

```python
class MAF_AgentService:
    _client = None  # shared instance
```

### ✔ Lazily initialized

```python
async def get_client(self):
    if not MAF_AgentService._client:
        MAF_AgentService._client = AIProjectClient(...)
    return MAF_AgentService._client
```

### ✔ Auto-managed credential

```python
credential = DefaultAzureCredential()
```

### ✔ Agent creation only once

```python
await self.provision_service.get_or_create_agent(...)
```

---

## 7. ⭐ Full Production-Ready Example

```python
import os
from azure.ai.projects.aio import AIProjectClient
from azure.identity.aio import DefaultAzureCredential
from app.services.agent_provision_service import AgentProvisionService

PROJECT_ENDPOINT = os.getenv("AZURE_AI_PROJECT_ENDPOINT")

class MAF_AgentService:
    """Production-ready Azure Foundry Agent wrapper."""

    _client = None  # Singleton

    def __init__(self):
        self.provision_service = AgentProvisionService()
        self.agent_name = "chat-agent"
        self.instructions = "You are a helpful AI assistant."

    async def get_client(self) -> AIProjectClient:
        """Create once, reuse always."""
        if not MAF_AgentService._client:
            credential = DefaultAzureCredential()
            MAF_AgentService._client = AIProjectClient(
                endpoint=PROJECT_ENDPOINT,
                credential=credential
            )
        return MAF_AgentService._client

    async def get_agent(self):
        """Get or create the Azure Foundry agent."""
        return await self.provision_service.get_or_create_agent(
            name=self.agent_name,
            instructions=self.instructions
        )

    async def get_response(self, message: str) -> str:
        agent_id = await self.get_agent()
        client = await self.get_client()

        # Create new thread for each conversation
        thread = await client.agents.threads.create()

        await client.agents.messages.create(
            thread_id=thread.id,
            role="user",
            content=message,
        )

        run = await client.agents.runs.create_and_process(
            thread_id=thread.id,
            agent_id=agent_id
        )

        # Fetch messages
        messages = client.agents.messages.list(thread_id=thread.id, order="ascending")

        last_text = ""
        async for m in messages:
            if getattr(m, "text_messages", None):
                last_text = m.text_messages[-1].text.value

        return last_text
```

---

## 8. 🔒 Security Best Practices

### ✔ Use `DefaultAzureCredential`

Enables local dev + Managed Identity in Azure automatically.

### ✔ Do NOT store secrets in code

Use:

* `.env`
* Azure Key Vault
* App Service settings

### ✔ Assign minimum permissions

Your Managed Identity needs only:

```
Azure AI Developer Role
```

---

## 9. 🧪 Performance Best Practices

| Pattern                   | Status         | Notes                       |
| ------------------------- | -------------- | --------------------------- |
| Singleton client          | ⭐ Recommended  | Azure guideline             |
| Create client per request | ❌ Avoid        | Causes latency, rate limits |
| Lazy initialization       | ✔ Good         | Simple and safe             |
| Dispose client            | ❌ Not required | Managed by SDK              |
| Multiple clients          | ❌ Avoid        | No benefit, more cost       |

---

## 10. 📝 Summary (Copy/Paste Ready)

* Azure AIProjectClient is **stateless**, **thread-safe**, and **designed for reuse**
* Create the client **once** and reuse it across all requests
* Never create a new client inside a request handler
* Threads & runs should be created per user conversation
* Token management is handled by Azure automatically
* This pattern reduces latency, failures, rate limits, and CPU overhead