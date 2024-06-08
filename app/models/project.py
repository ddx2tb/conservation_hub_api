from datetime import datetime

from sqlalchemy import Column, Integer, DateTime, ForeignKey, String

from app.database import Base


class Project(Base):
    __tablename__ = 'projects'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    ecosystem_id = Column(Integer, ForeignKey('ecosystems.id'), nullable=False)
    creation_date = Column(DateTime, default=datetime.now)
    modification_date = Column(DateTime, default=datetime.now)
