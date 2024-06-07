from sqlalchemy import Column, Integer, ForeignKey

from app.database import Base


class ResourceAssignment(Base):
    __tablename__ = 'resources_assignment'

    id = Column(Integer, primary_key=True)
    task_id = Column(Integer, ForeignKey('tasks.id'), nullable=False)
    resource_id = Column(Integer, ForeignKey('resources.id'), nullable=False)
    assigned_quantity = Column(Integer, nullable=False)
