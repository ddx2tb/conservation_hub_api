from uuid import uuid4

from sqlalchemy import Column, Integer, ForeignKey, UUID

from app.database import Base


class ResourceAssignment(Base):
    __tablename__ = 'resources_assignment'

    id = Column(UUID, primary_key=True, default=uuid4)
    task_id = Column(Integer, ForeignKey('tasks.id'), nullable=False)
    resource_id = Column(Integer, ForeignKey('resources.id'), nullable=False)
    assigned_quantity = Column(Integer, nullable=False)
