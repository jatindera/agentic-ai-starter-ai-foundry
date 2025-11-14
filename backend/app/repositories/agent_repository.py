from app.models.orm.agent import Agent
from sqlalchemy.orm import Session

class AgentRepository:

    def get_agent(self, db: Session, name: str):
        return db.query(Agent).filter(Agent.agent_name == name).first()

    def save_agent(self, db: Session, name: str, agent_id: str):
        record = Agent(agent_name=name, agent_id=agent_id)
        db.add(record)
        db.commit()
        return record
