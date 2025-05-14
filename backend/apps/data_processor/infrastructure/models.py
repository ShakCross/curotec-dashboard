from sqlalchemy import Column, Integer, String, Float, JSON, ForeignKey
from sqlalchemy.orm import relationship
from shared.db.base_model import BaseModel
import logging

# Configure logging
logger = logging.getLogger(__name__)

class DataEntry(BaseModel):
    """SQLAlchemy model for storing data entries"""
    __tablename__ = "data_entries"
    
    # Store numeric and string fields in JSON format
    numeric_fields = Column(JSON, nullable=False, default=dict)
    string_fields = Column(JSON, nullable=False, default=dict)
    
    def to_domain(self):
        """Convert to domain model"""
        from apps.data_processor.domain.models import DataItem
        
        # Log the conversion for debugging
        logger.debug(f"Converting DB model to domain: id={self.id}, " +
                    f"numeric_fields={self.numeric_fields}, " +
                    f"string_fields={self.string_fields}")
        
        # Ensure fields are dicts, not None
        numeric_fields = self.numeric_fields if self.numeric_fields is not None else {}
        string_fields = self.string_fields if self.string_fields is not None else {}
        
        return DataItem(
            id=self.id,
            numeric_fields=numeric_fields,
            string_fields=string_fields
        )
    
    @classmethod
    def from_domain(cls, data_item):
        """Create from domain model"""
        # Log the conversion for debugging
        logger.debug(f"Converting domain to DB model: id={data_item.id}, " +
                    f"numeric_fields={data_item.numeric_fields}, " +
                    f"string_fields={data_item.string_fields}")
        
        # Ensure fields are dicts, not None
        numeric_fields = data_item.numeric_fields if data_item.numeric_fields is not None else {}
        string_fields = data_item.string_fields if data_item.string_fields is not None else {}
        
        return cls(
            id=data_item.id,
            numeric_fields=numeric_fields,
            string_fields=string_fields
        ) 