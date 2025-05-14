from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum

class TransformationType(str, Enum):
    """Types of transformations that can be performed on data"""
    FILTER = "filter"
    SORT = "sort"
    AGGREGATE = "aggregate"
    
    @classmethod
    def has_value(cls, value):
        """Check if value is a valid TransformationType"""
        return value in [item.value for item in cls]

@dataclass
class DataItem:
    """Domain model for a single data item"""
    id: Optional[int] = None
    numeric_fields: Dict[str, float] = None
    string_fields: Dict[str, str] = None
    
    def __post_init__(self):
        if self.numeric_fields is None:
            self.numeric_fields = {}
        if self.string_fields is None:
            self.string_fields = {}
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation"""
        result = {}
        if self.id is not None:
            result["id"] = self.id
        
        result.update(self.numeric_fields)
        result.update(self.string_fields)
        
        return result

@dataclass
class DataSet:
    """Domain model for a collection of data items"""
    items: List[DataItem]
    
    def filter(self, field: str, value: Any, operator: str = "eq") -> "DataSet":
        """Filter items based on field, value and operator"""
        filtered_items = []
        
        for item in self.items:
            # Special case for ID field
            if field == 'id':
                item_value = item.id
                if item_value is None:
                    continue
                
                # Ensure both values are integers for comparison
                try:
                    item_value = int(item_value)
                    compare_value = int(value) if not isinstance(value, int) else value
                except (ValueError, TypeError):
                    continue
                    
                # Apply operator
                if operator == "eq" and item_value == compare_value:
                    filtered_items.append(item)
                elif operator == "neq" and item_value != compare_value:
                    filtered_items.append(item)
                elif operator == "gt" and item_value > compare_value:
                    filtered_items.append(item)
                elif operator == "lt" and item_value < compare_value:
                    filtered_items.append(item)
                continue
                
            # Handle numeric fields (price, quantity, etc.)
            if field in item.numeric_fields:
                item_value = item.numeric_fields[field]
                
                # Ensure both values are numeric for comparison
                try:
                    item_value = float(item_value)
                    compare_value = float(value) if not isinstance(value, (int, float)) else value
                except (ValueError, TypeError):
                    continue
                
                # Apply the filter based on operator
                if operator == "eq" and item_value == compare_value:
                    filtered_items.append(item)
                elif operator == "neq" and item_value != compare_value:
                    filtered_items.append(item)
                elif operator == "gt" and item_value > compare_value:
                    filtered_items.append(item)
                elif operator == "lt" and item_value < compare_value:
                    filtered_items.append(item)
                continue
                
            # Handle string fields    
            elif field in item.string_fields:
                item_value = item.string_fields[field]
                
                # Apply string comparison operators
                if operator == "eq" and item_value == value:
                    filtered_items.append(item)
                elif operator == "neq" and item_value != value:
                    filtered_items.append(item)
                elif operator == "contains" and isinstance(value, str):
                    # Case-insensitive contains check
                    if value.upper() in item_value.upper():
                        filtered_items.append(item)
        
        return DataSet(items=filtered_items)
    
    def sort(self, field: str, ascending: bool = True) -> "DataSet":
        """Sort items based on field"""
        
        def get_value(item: DataItem) -> Any:
            # Special case for ID field
            if field == 'id':
                return item.id
            elif field in item.numeric_fields:
                return item.numeric_fields[field]
            elif field in item.string_fields:
                return item.string_fields[field]
            return None
        
        # Create a sorted copy
        sorted_items = sorted(
            [item for item in self.items if get_value(item) is not None],
            key=get_value,
            reverse=not ascending
        )
        
        return DataSet(items=sorted_items)
    
    def aggregate(self, field: str, operation: str = "sum") -> Dict[str, Any]:
        """Aggregate numeric values using specified operation"""
        values = []
        
        for item in self.items:
            if field in item.numeric_fields:
                values.append(item.numeric_fields[field])
        
        if not values:
            return {"result": None}
            
        if operation == "sum":
            return {"result": sum(values)}
        elif operation == "avg":
            return {"result": sum(values) / len(values)}
        elif operation == "min":
            return {"result": min(values)}
        elif operation == "max":
            return {"result": max(values)}
        elif operation == "count":
            return {"result": len(values)}
        
        return {"result": None}
    
    def to_dict(self) -> List[Dict[str, Any]]:
        """Convert to list of dictionaries"""
        return [item.to_dict() for item in self.items] 