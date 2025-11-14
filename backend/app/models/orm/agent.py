from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String

class Base(DeclarativeBase):
    pass

class Agent(Base):
    __tablename__ = "agents"

    agent_name: Mapped[str] = mapped_column(String(100), primary_key=True)
    agent_id: Mapped[str] = mapped_column(String(200), nullable=False)
