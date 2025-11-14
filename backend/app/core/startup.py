from fastapi import FastAPI
from starlette.concurrency import run_in_threadpool

from app.db.session import sync_engine
from app.models.orm.agent import Base


def init_db_sync():
    """Initialize database schema (sync SQLAlchemy)."""
    Base.metadata.create_all(bind=sync_engine)


async def startup_event(app: FastAPI):
    """FastAPI startup hook."""
    print("🚀 Initializing database...")
    await run_in_threadpool(init_db_sync)   # run sync DB setup without blocking
    print("✅ Database ready.")


async def shutdown_event(app: FastAPI):
    """FastAPI shutdown hook."""
    print("🛑 Shutting down database engine...")
    await run_in_threadpool(sync_engine.dispose)
    print("👌 Engine closed.")
