from rest_framework import status, views
from rest_framework.response import Response
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from django.conf import settings
import logging
import json
from apps.data_processor.application.services import DataProcessingService
from apps.data_processor.infrastructure.serializers import DataItemSerializer, DataSetSerializer
from apps.data_processor.domain.models import TransformationType
from apps.data_processor.domain.schemas import (
    DataSetSchema, FilterParamsSchema, SortParamsSchema, 
    AggregateParamsSchema, TransformationTypeEnum
)
from pydantic import ValidationError

# Configure logging
logger = logging.getLogger(__name__)

# Configure SQLAlchemy
engine = create_engine(settings.SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class DataProcessorView(views.APIView):
    """View for processing and transforming data"""
    
    def get_session(self):
        """Get SQLAlchemy session"""
        session = SessionLocal()
        try:
            return session
        finally:
            session.close()
    
    def post(self, request, *args, **kwargs):
        """Process data"""
        try:
            # Log received data for debugging
            logger.info(f"Received data for processing: {json.dumps(request.data)}")
            
            # Check if request data is empty
            if not request.data:
                return Response(
                    {"error": "No data provided"},
                    status=status.HTTP_400_BAD_REQUEST
                )
                
            # Validate input data with Pydantic
            if isinstance(request.data, list):
                data_items = request.data
            else:
                data_items = [request.data]
                
            # Ensure each item has required fields
            for item in data_items:
                # Extract required fields if missing
                if not item.get('name'):
                    return Response(
                        {"error": "Product name is required"}, 
                        status=status.HTTP_400_BAD_REQUEST
                    )
                    
                # Log the processed item
                logger.debug(f"Processing product: {item.get('name')}")
                
            data_set_schema = DataSetSchema(items=data_items)
            
            # Convert validated data to domain model
            domain_data_set = data_set_schema.to_domain()
            
            # Create session and service
            session = SessionLocal()
            try:
                service = DataProcessingService(session)
                
                # Process data
                result = service.process_data(domain_data_set.to_dict())
                
                # Log the result
                logger.info(f"Successfully processed {len(result)} products")
                
                return Response(result, status=status.HTTP_201_CREATED)
            except Exception as e:
                session.rollback()
                logger.error(f"Error processing data: {str(e)}")
                return Response(
                    {"error": str(e)},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            finally:
                session.close()
        except ValidationError as e:
            logger.error(f"Validation error: {e.errors()}")
            return Response(
                {"error": "Invalid data format", "details": e.errors()},
                status=status.HTTP_400_BAD_REQUEST
            )

class AllProductsView(views.APIView):
    """View for retrieving all products"""
    
    def get(self, request, *args, **kwargs):
        """Get all products without transformation"""
        # Create session and service
        session = SessionLocal()
        try:
            service = DataProcessingService(session)
            
            # Get all data as domain objects
            dataset = service.repository.get_all_as_domain()
            
            # Convert to dictionary representation
            result = {"data": dataset.to_dict()}
            
            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error getting all products: {str(e)}")
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        finally:
            session.close()

class TransformDataView(views.APIView):
    """View for transforming data"""
    
    def get(self, request, transformation_type, *args, **kwargs):
        """Transform data based on transformation type and parameters"""
        # Validate transformation type
        try:
            # Use Pydantic enum for validation
            transformation = TransformationTypeEnum(transformation_type)
        except ValueError:
            return Response(
                {"error": f"Invalid transformation type: {transformation_type}. Valid types are: {', '.join([t.value for t in TransformationTypeEnum])}"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Extract parameters from query string
        params = {}
        for key, value in request.query_params.items():
            # Process special fields with proper type conversion
            if key == 'field' and value in ('id', 'price', 'quantity'):
                params[key] = value
            # Convert string values to appropriate types
            elif key == 'value':
                field = request.query_params.get('field', '')
                # Handle ID field specifically to ensure it's an integer
                if field == 'id':
                    try:
                        params[key] = int(value)
                    except (ValueError, TypeError):
                        return Response(
                            {"error": "ID values must be valid integers"},
                            status=status.HTTP_400_BAD_REQUEST
                        )
                # Handle price and quantity fields to ensure they're floats
                elif field in ('price', 'quantity'):
                    try:
                        params[key] = float(value)
                    except (ValueError, TypeError):
                        return Response(
                            {"error": f"{field.capitalize()} values must be valid numbers"},
                            status=status.HTTP_400_BAD_REQUEST
                        )
                else:
                    # Default handling for other fields
                    if value.isdigit():
                        params[key] = int(value)
                    elif value.replace('.', '', 1).isdigit() and value.count('.') < 2:
                        params[key] = float(value)
                    elif value.lower() in ('true', 'false'):
                        params[key] = value.lower() == 'true'
                    else:
                        params[key] = value
            else:
                # Default handling for other parameters
                if value.isdigit():
                    params[key] = int(value)
                elif value.replace('.', '', 1).isdigit() and value.count('.') < 2:
                    params[key] = float(value)
                elif value.lower() in ('true', 'false'):
                    params[key] = value.lower() == 'true'
                else:
                    params[key] = value
        
        try:
            # Validate parameters based on transformation type
            validated_params = {}
            if transformation == TransformationTypeEnum.FILTER:
                filter_schema = FilterParamsSchema(**params)
                validated_params = filter_schema.dict()
            elif transformation == TransformationTypeEnum.SORT:
                validated_params = SortParamsSchema(**params).dict()
            elif transformation == TransformationTypeEnum.AGGREGATE:
                validated_params = AggregateParamsSchema(**params).dict()
            
            # Create session and service
            session = SessionLocal()
            try:
                service = DataProcessingService(session)
                
                # Transform data
                result = service.transform_data(transformation.value, **validated_params)
                
                # Add empty data response if no products found for better frontend handling
                if "data" in result and (not result["data"] or len(result["data"]) == 0):
                    return Response({"data": [], "message": "No products found matching your criteria."}, status=status.HTTP_200_OK)
                
                return Response(result, status=status.HTTP_200_OK)
            except Exception as e:
                logger.error(f"Error transforming data: {str(e)}")
                return Response(
                    {"error": str(e)},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            finally:
                session.close()
        except ValidationError as e:
            logger.error(f"Validation error: {e.errors()}")
            return Response(
                {"error": "Invalid parameters", "details": e.errors()},
                status=status.HTTP_400_BAD_REQUEST
            ) 