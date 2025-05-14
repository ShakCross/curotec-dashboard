from typing import Dict, List, Any, Optional, Union
from pydantic import BaseModel as PydanticBaseModel, Field, validator, root_validator
from enum import Enum


class BaseModel(PydanticBaseModel):
    """Base model with config for all Pydantic models"""
    class Config:
        validate_assignment = True
        arbitrary_types_allowed = True


class TransformationTypeEnum(str, Enum):
    """Types of transformations that can be performed on data"""
    FILTER = "filter"
    SORT = "sort"
    AGGREGATE = "aggregate"


class OperatorEnum(str, Enum):
    """Valid operators for filtering data"""
    EQ = "eq"
    NEQ = "neq"
    GT = "gt"
    LT = "lt"
    CONTAINS = "contains"


class AggregationOperationEnum(str, Enum):
    """Valid operations for data aggregation"""
    SUM = "sum"
    AVG = "avg"
    MIN = "min"
    MAX = "max"
    COUNT = "count"


class DataItemSchema(BaseModel):
    """Pydantic schema for data item validation"""
    id: Optional[int] = None
    name: Optional[str] = None
    price: Optional[float] = None
    quantity: Optional[int] = None
    category: Optional[str] = None
    numeric_fields: Dict[str, float] = Field(default_factory=dict)
    string_fields: Dict[str, str] = Field(default_factory=dict)
    
    class Config:
        extra = "allow"  # Allow extra fields which will be sorted into numeric/string fields
    
    @validator("numeric_fields", "string_fields", pre=True)
    def ensure_dict(cls, v):
        if v is None:
            return {}
        return v
    
    @root_validator(pre=True)
    def process_frontend_fields(cls, values):
        """Process frontend fields and map them to numeric_fields and string_fields"""
        # Start with empty dictionaries
        numeric_fields = dict(values.get('numeric_fields', {}))
        string_fields = dict(values.get('string_fields', {}))
        
        # Process name field
        if 'name' in values and values['name']:
            string_fields['name'] = str(values['name'])
        
        # Process price field
        if 'price' in values and values['price'] is not None:
            try:
                numeric_fields['price'] = float(values['price'])
            except (TypeError, ValueError):
                pass
        
        # Process quantity field
        if 'quantity' in values and values['quantity'] is not None:
            try:
                numeric_fields['quantity'] = int(values['quantity'])
            except (TypeError, ValueError):
                pass
        
        # Process category field
        if 'category' in values and values['category']:
            string_fields['category'] = str(values['category'])
        
        # Update the values
        updated_values = dict(values)
        updated_values['numeric_fields'] = numeric_fields
        updated_values['string_fields'] = string_fields
        
        return updated_values
    
    def to_domain(self):
        """Convert to domain model"""
        from apps.data_processor.domain.models import DataItem
        return DataItem(
            id=self.id,
            numeric_fields=self.numeric_fields,
            string_fields=self.string_fields
        )
    
    @classmethod
    def from_domain(cls, domain_model):
        """Create from domain model"""
        # Extract named fields from numeric and string fields
        numeric_fields = domain_model.numeric_fields or {}
        string_fields = domain_model.string_fields or {}
        
        return cls(
            id=domain_model.id,
            name=string_fields.get('name'),
            price=numeric_fields.get('price'),
            quantity=numeric_fields.get('quantity'),
            category=string_fields.get('category'),
            numeric_fields=numeric_fields,
            string_fields=string_fields
        )


class DataSetSchema(BaseModel):
    """Pydantic schema for data set validation"""
    items: List[DataItemSchema] = Field(default_factory=list)
    
    def to_domain(self):
        """Convert to domain model"""
        from apps.data_processor.domain.models import DataSet, DataItem
        return DataSet(
            items=[item.to_domain() for item in self.items]
        )
    
    @classmethod
    def from_domain(cls, domain_model):
        """Create from domain model"""
        return cls(
            items=[DataItemSchema.from_domain(item) for item in domain_model.items]
        )


class FilterParamsSchema(BaseModel):
    """Pydantic schema for filter parameters validation"""
    field: str
    value: Union[str, int, float, bool]
    operator: OperatorEnum = OperatorEnum.EQ
    
    @validator('value')
    def convert_value_type(cls, v, values):
        """Convert value to appropriate type based on field"""
        field = values.get('field')
        if field == 'id' and not isinstance(v, int):
            try:
                return int(v)
            except (ValueError, TypeError):
                raise ValueError(f"ID must be an integer, got {v}")
        return v


class SortParamsSchema(BaseModel):
    """Pydantic schema for sort parameters validation"""
    field: str
    ascending: bool = True


class AggregateParamsSchema(BaseModel):
    """Pydantic schema for aggregate parameters validation"""
    field: str
    operation: AggregationOperationEnum = AggregationOperationEnum.SUM 