from datetime import datetime
from uuid import uuid4

from sqlalchemy import Column, String, DateTime, UUID

from app.database import Base


class Ecosystem(Base):
    __tablename__ = 'ecosystems'

    id = Column(UUID, primary_key=True, default=uuid4)
    name = Column(String, nullable=False)
    description = Column(String)
    creation_date = Column(DateTime, default=datetime.now)
