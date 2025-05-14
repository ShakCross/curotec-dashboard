from typing import Generic, TypeVar, Type, List, Optional, Any, Dict, Union
from sqlalchemy.orm import Session
from .base_model import BaseModel

T = TypeVar('T', bound=BaseModel)

class BaseRepository(Generic[T]):
    """Base repository for database operations"""
    
    def __init__(self, model: Type[T], session: Session):
        self.model = model
        self.session = session
    
    def get_by_id(self, id: int) -> Optional[T]:
        """Get a record by ID"""
        return self.session.query(self.model).filter(self.model.id == id).first()
    
    def get_all(self) -> List[T]:
        """Get all records"""
        return self.session.query(self.model).all()
    
    def create(self, data: Dict[str, Any]) -> T:
        """Create a new record"""
        instance = self.model(**data)
        self.session.add(instance)
        self.session.commit()
        self.session.refresh(instance)
        return instance
    
    def update(self, id: int, data: Dict[str, Any]) -> Optional[T]:
        """Update an existing record"""
        instance = self.get_by_id(id)
        if instance:
            for key, value in data.items():
                setattr(instance, key, value)
            self.session.commit()
            self.session.refresh(instance)
        return instance
    
    def delete(self, id: int) -> bool:
        """Delete a record"""
        instance = self.get_by_id(id)
        if instance:
            self.session.delete(instance)
            self.session.commit()
            return True
        return False
    
    def filter(self, **kwargs) -> List[T]:
        """Filter records by attributes"""
        return self.session.query(self.model).filter_by(**kwargs).all() 