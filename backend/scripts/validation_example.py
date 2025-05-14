#!/usr/bin/env python
"""
Example script showing how to use Pydantic models for validation in the backend.
This demonstrates the validation capabilities added to improve data integrity.
"""

import sys
import os
import json
from typing import Dict, List, Any

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import Pydantic schemas
from apps.data_processor.domain.schemas import (
    DataItemSchema, DataSetSchema, FilterParamsSchema, 
    SortParamsSchema, AggregateParamsSchema
)

def validate_data_item(data: Dict[str, Any]) -> None:
    """Validate a single data item using Pydantic"""
    try:
        # Validate with Pydantic schema
        schema = DataItemSchema.parse_obj(data)
        print(f"✅ Valid data item: {schema.dict()}")
        
        # Show the numeric and string fields separation
        print(f"  - Numeric fields: {schema.numeric_fields}")
        print(f"  - String fields: {schema.string_fields}")
        
        # Convert to domain model
        domain_model = schema.to_domain()
        print(f"  - Domain model: {domain_model}")
        
        return schema
    except Exception as e:
        print(f"❌ Invalid data item: {e}")
        return None

def validate_data_set(data_items: List[Dict[str, Any]]) -> None:
    """Validate a dataset using Pydantic"""
    try:
        # Validate with Pydantic schema
        schema = DataSetSchema(items=data_items)
        print(f"✅ Valid dataset with {len(schema.items)} items")
        
        # Convert to domain model
        domain_model = schema.to_domain()
        print(f"  - Domain model items count: {len(domain_model.items)}")
        
        return schema
    except Exception as e:
        print(f"❌ Invalid dataset: {e}")
        return None

def validate_filter_params(params: Dict[str, Any]) -> None:
    """Validate filter parameters using Pydantic"""
    try:
        # Validate with Pydantic schema
        schema = FilterParamsSchema(**params)
        print(f"✅ Valid filter parameters: {schema.dict()}")
        return schema
    except Exception as e:
        print(f"❌ Invalid filter parameters: {e}")
        return None

def validate_sort_params(params: Dict[str, Any]) -> None:
    """Validate sort parameters using Pydantic"""
    try:
        # Validate with Pydantic schema
        schema = SortParamsSchema(**params)
        print(f"✅ Valid sort parameters: {schema.dict()}")
        return schema
    except Exception as e:
        print(f"❌ Invalid sort parameters: {e}")
        return None

def validate_aggregate_params(params: Dict[str, Any]) -> None:
    """Validate aggregate parameters using Pydantic"""
    try:
        # Validate with Pydantic schema
        schema = AggregateParamsSchema(**params)
        print(f"✅ Valid aggregate parameters: {schema.dict()}")
        return schema
    except Exception as e:
        print(f"❌ Invalid aggregate parameters: {e}")
        return None


if __name__ == "__main__":
    print("\n=== Pydantic Validation Examples ===\n")
    
    # Valid data item example
    print("\n-- Valid Data Item --")
    valid_item = {
        "id": 1,
        "name": "Product 1",
        "price": 19.99,
        "quantity": 10,
        "category": "Electronics"
    }
    validate_data_item(valid_item)
    
    # Invalid data item example
    print("\n-- Invalid Data Item --")
    invalid_item = {
        "id": "not-a-number",  # Should be an integer
        "price": "19.99",      # Should be a number
        "quantity": "10"       # Should be a number
    }
    validate_data_item(invalid_item)
    
    # Valid dataset example
    print("\n-- Valid Dataset --")
    valid_dataset = [
        {
            "name": "Product 1",
            "price": 19.99,
            "quantity": 10
        },
        {
            "name": "Product 2",
            "price": 29.99,
            "quantity": 5
        }
    ]
    validate_data_set(valid_dataset)
    
    # Valid filter parameters
    print("\n-- Valid Filter Parameters --")
    valid_filter = {
        "field": "price",
        "value": 19.99,
        "operator": "gt"
    }
    validate_filter_params(valid_filter)
    
    # Invalid filter parameters
    print("\n-- Invalid Filter Parameters --")
    invalid_filter = {
        "field": "price",
        "value": 19.99,
        "operator": "invalid"  # Not a valid operator
    }
    validate_filter_params(invalid_filter)
    
    # Valid sort parameters
    print("\n-- Valid Sort Parameters --")
    valid_sort = {
        "field": "price",
        "ascending": False
    }
    validate_sort_params(valid_sort)
    
    # Valid aggregate parameters
    print("\n-- Valid Aggregate Parameters --")
    valid_aggregate = {
        "field": "price",
        "operation": "avg"
    }
    validate_aggregate_params(valid_aggregate)
    
    # Invalid aggregate parameters
    print("\n-- Invalid Aggregate Parameters --")
    invalid_aggregate = {
        "field": "price",
        "operation": "invalid"  # Not a valid operation
    }
    validate_aggregate_params(invalid_aggregate) 