from uuid import uuid4

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, UUID

from app.database import Base


class Task(Base):
    __tablename__ = 'tasks'

    id = Column(UUID, primary_key=True, default=uuid4)
    project_id = Column(Integer, ForeignKey('projects.id'), nullable=False)
    name = Column(String, nullable=False)
    description = Column(String)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    status = Column(String, nullable=False)
