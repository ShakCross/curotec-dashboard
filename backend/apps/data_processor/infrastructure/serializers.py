from typing import List, Dict, Any
from rest_framework import serializers
from apps.data_processor.domain.models import DataItem, DataSet
from apps.data_processor.domain.schemas import DataItemSchema, DataSetSchema

class DataItemSerializer(serializers.Serializer):
    """Serializer for data items"""
    id = serializers.IntegerField(required=False)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # DRF doesn't natively support dynamic fields,
        # so we'll handle additional fields in the to_representation and to_internal_value methods
    
    def to_representation(self, instance):
        """Convert DataItem to dictionary"""
        if isinstance(instance, DataItem):
            return instance.to_dict()
        return instance
    
    def to_internal_value(self, data):
        """Convert dictionary to DataItem using Pydantic validation"""
        try:
            # Use Pydantic for validation
            schema = DataItemSchema.parse_obj(data)
            # Convert to domain model
            return schema.to_domain()
        except Exception as e:
            raise serializers.ValidationError(str(e))
    
    def create(self, validated_data):
        """Return the validated data as is"""
        return validated_data
    
    def update(self, instance, validated_data):
        """Update instance with validated data"""
        instance.id = validated_data.get('id', instance.id)
        instance.numeric_fields.update(validated_data.get('numeric_fields', {}))
        instance.string_fields.update(validated_data.get('string_fields', {}))
        return instance

class DataSetSerializer(serializers.Serializer):
    """Serializer for data sets"""
    items = DataItemSerializer(many=True)
    
    def to_representation(self, instance):
        """Convert DataSet to list of dictionaries"""
        if isinstance(instance, DataSet):
            return instance.to_dict()
        return instance
    
    def to_internal_value(self, data):
        """Convert list of dictionaries to DataSet using Pydantic validation"""
        try:
            # Use Pydantic for validation
            schema = DataSetSchema(items=data)
            # Convert to domain model
            return schema.to_domain()
        except Exception as e:
            raise serializers.ValidationError(str(e))
    
    def create(self, validated_data):
        """Return the validated data as is"""
        return validated_data
    
    def update(self, instance, validated_data):
        """Update is not supported for DataSet"""
        raise NotImplementedError("Update is not supported for DataSet") 