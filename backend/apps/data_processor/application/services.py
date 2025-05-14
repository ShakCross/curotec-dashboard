from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
import logging
from apps.data_processor.domain.models import DataItem, DataSet, TransformationType
from apps.data_processor.domain.schemas import (
    DataItemSchema, DataSetSchema, FilterParamsSchema, 
    SortParamsSchema, AggregateParamsSchema, TransformationTypeEnum
)
from apps.data_processor.infrastructure.repositories import DataEntryRepository

# Configure logging
logger = logging.getLogger(__name__)

class DataProcessingService:
    """Service for processing and transforming data"""
    
    def __init__(self, session: Session):
        self.session = session
        self.repository = DataEntryRepository(session)
    
    def process_data(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Process raw input data and store in database"""
        # Convert input data to domain models using Pydantic schemas
        data_items = []
        
        for item_data in data:
            try:
                # Log the raw item
                logger.debug(f"Processing raw item: {item_data}")
                
                # Ensure required fields exist (name, price, quantity, category)
                if 'name' not in item_data or not item_data['name']:
                    logger.warning(f"Skipping item with missing name: {item_data}")
                    continue
                    
                # Validate with Pydantic schema
                schema = DataItemSchema.parse_obj(item_data)
                
                # Log validated schema
                logger.debug(f"Validated schema: id={schema.id}, name={schema.name}, " +
                            f"price={schema.price}, quantity={schema.quantity}, " +
                            f"category={schema.category}")
                logger.debug(f"Numeric fields: {schema.numeric_fields}")
                logger.debug(f"String fields: {schema.string_fields}")
                
                # Convert to domain model
                domain_item = schema.to_domain()
                data_items.append(domain_item)
                
                # Log domain item
                logger.debug(f"Domain item: id={domain_item.id}, " +
                            f"numeric_fields={domain_item.numeric_fields}, " +
                            f"string_fields={domain_item.string_fields}")
            except Exception as e:
                logger.error(f"Error processing item {item_data}: {str(e)}")
                raise
        
        # Skip processing if no valid items
        if not data_items:
            logger.warning("No valid items to process")
            return []
            
        # Store data items
        created_entries = self.repository.create_many(data_items)
        
        # Return stored data
        result = [entry.to_domain().to_dict() for entry in created_entries]
        logger.info(f"Created {len(result)} entries")
        return result
    
    def transform_data(self, transformation_type: str, **params) -> Dict[str, Any]:
        """Transform data based on transformation type and parameters"""
        try:
            # Log transformation request
            logger.info(f"Transforming data with type: {transformation_type}, params: {params}")
            
            # Get all data as domain objects
            dataset = self.repository.get_all_as_domain()
            
            # Apply transformation
            if transformation_type == TransformationTypeEnum.FILTER:
                # Parameters already validated by Pydantic in the view
                field = params.get('field')
                value = params.get('value')
                operator = params.get('operator')
                
                logger.debug(f"Filtering by field: {field}, value: {value} ({type(value)}), operator: {operator}")
                
                # Handle ID field specially
                if field == 'id' and not isinstance(value, int):
                    try:
                        value = int(value)
                    except (ValueError, TypeError):
                        logger.error(f"Invalid ID value: {value}")
                        raise ValueError(f"ID must be an integer, got {value}")
                
                # Handle numeric fields
                if field in ('price', 'quantity') and not isinstance(value, (int, float)):
                    try:
                        value = float(value)
                    except (ValueError, TypeError):
                        logger.error(f"Invalid numeric value for {field}: {value}")
                        raise ValueError(f"{field.capitalize()} must be a number, got {value}")
                
                result = dataset.filter(field, value, operator)
                if not result.items:
                    logger.info(f"No results found for filter: {field}={value} with operator {operator}")
                return {"data": result.to_dict()}
                
            elif transformation_type == TransformationTypeEnum.SORT:
                # Parameters already validated by Pydantic in the view
                field = params.get('field')
                ascending = params.get('ascending')
                
                logger.debug(f"Sorting by field: {field}, ascending: {ascending}")
                
                result = dataset.sort(field, ascending)
                return {"data": result.to_dict()}
                
            elif transformation_type == TransformationTypeEnum.AGGREGATE:
                # Parameters already validated by Pydantic in the view
                field = params.get('field')
                operation = params.get('operation')
                
                logger.debug(f"Aggregating field: {field}, operation: {operation}")
                
                result = dataset.aggregate(field, operation)
                return result
            
            logger.error(f"Unsupported transformation type: {transformation_type}")
            raise ValueError(f"Unsupported transformation type: {transformation_type}")
            
        except Exception as e:
            logger.error(f"Error in transform_data: {str(e)}")
            raise 