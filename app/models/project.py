from datetime import datetime

from sqlalchemy import Column, Integer, DateTime, ForeignKey

from app.database import Base


class Project(Base):
    __tablename__ = 'projects'

    id = Column(Integer, primary_key=True)
    ecosystem_id = Column(Integer, ForeignKey('ecosystems.id'), nullable=False)
    creation_date = Column(DateTime, default=datetime.now)
    modification_date = Column(DateTime, default=datetime.now)
