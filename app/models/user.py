from uuid import uuid4

from sqlalchemy import Column, String, UUID

from app.database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(UUID, primary_key=True, default=uuid4)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
