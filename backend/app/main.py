from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.chat import router as chat_router
from app.api.routes.health import router as health_router
from app.core.config import settings
from app.core.startup import startup_event, shutdown_event

app = FastAPI(
    title="Agentic AI Starter – AI Foundry",
    version="1.0.0",
    description="Base backend service using FastAPI with Azure SQL + MAF"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(health_router, prefix="/health", tags=["Health"])
app.include_router(chat_router, prefix="/chat", tags=["Chat"])
app.include_router(chat_router, prefix="/chat", tags=["Chat"])

# Startup / Shutdown
@app.on_event("startup")
async def on_startup():
    await startup_event(app)

@app.on_event("shutdown")
async def on_shutdown():
    await shutdown_event(app)

@app.get("/")
async def root():
    return {"message": "Backend is running"}


