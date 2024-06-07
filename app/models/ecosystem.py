from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime

from app.database import Base


class Ecosystem(Base):
    __tablename__ = 'ecosystems'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    creation_date = Column(DateTime, default=datetime.now)
