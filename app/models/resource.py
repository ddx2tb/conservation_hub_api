from uuid import uuid4

from sqlalchemy import Column, Integer, String, UUID

from app.database import Base


class Resource(Base):
    __tablename__ = 'resources'

    id = Column(UUID, primary_key=True, default=uuid4)
    name = Column(String, nullable=False)
    description = Column(String)
    quantity = Column(Integer, nullable=False)
