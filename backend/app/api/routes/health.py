from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.concurrency import run_in_threadpool
from app.dependencies.db import get_db_sync

router = APIRouter()


@router.get("/", tags=["Health"])
async def health_root():
    return {"status": "ok"}


@router.get("/db-check")
async def db_check(db: Session = Depends(get_db_sync)):
    """
    Executes SELECT 1 using Azure SQL RBAC sync connection
    inside an async FastAPI route.
    """

    def query():
        result = db.execute("SELECT 1 AS value")
        return result.scalar()

    value = await run_in_threadpool(query)

    return {
        "database_status": "connected" if value == 1 else "failed",
        "value": value
    }