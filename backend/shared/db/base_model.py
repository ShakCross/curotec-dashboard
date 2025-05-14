from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.sql import func
import uuid
from datetime import datetime

Base = declarative_base()

class BaseModel(Base):
    """Base model for all database entities"""
    __abstract__ = True
    
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    def to_dict(self):
        """Convert model instance to a dictionary"""
        return {c.name: getattr(self, c.name) for c in self.__table__.columns} 