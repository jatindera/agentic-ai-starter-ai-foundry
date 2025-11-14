from app.db.session import SessionLocal

def get_db_sync():
    """FastAPI dependency for SQLAlchemy sync session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
