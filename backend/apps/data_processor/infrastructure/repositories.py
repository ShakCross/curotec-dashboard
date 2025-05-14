from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from shared.db.base_repository import BaseRepository
from apps.data_processor.domain.models import DataItem, DataSet
from .models import DataEntry

class DataEntryRepository(BaseRepository[DataEntry]):
    """Repository for data entries"""
    
    def __init__(self, session: Session):
        super().__init__(DataEntry, session)
    
    def create_many(self, data_items: List[DataItem]) -> List[DataEntry]:
        """Create multiple data entries"""
        entries = [DataEntry.from_domain(item) for item in data_items]
        self.session.add_all(entries)
        self.session.commit()
        for entry in entries:
            self.session.refresh(entry)
        return entries
    
    def get_all_as_domain(self) -> DataSet:
        """Get all entries as domain objects"""
        entries = self.get_all()
        return DataSet(items=[entry.to_domain() for entry in entries])
    
    def filter_by_field(self, field: str, value: Any) -> DataSet:
        """
        Filter entries by field value
        Note: This is a simplified implementation as filtering JSON fields
        would be more complex in real SQL queries
        """
        entries = self.get_all()
        domain_items = [entry.to_domain() for entry in entries]
        dataset = DataSet(items=domain_items)
        return dataset.filter(field, value) 