"""
Response Transformer
Transforms API responses into standardized format
"""

import logging
from typing import List, Dict, Any, Optional, Callable
import pandas as pd

logger = logging.getLogger(__name__)


class ResponseTransformer:
    """Transform API responses"""
    
    def __init__(self):
        """Initialize transformer"""
        self.transformations = []
    
    def add_transformation(self, transformation: Callable):
        """
        Add a transformation function
        
        Args:
            transformation: Function that takes a record and returns transformed record
        """
        self.transformations.append(transformation)
    
    def transform(
        self,
        data: List[Dict[str, Any]],
        field_mapping: Optional[Dict[str, str]] = None,
        custom_transforms: Optional[List[Callable]] = None
    ) -> List[Dict[str, Any]]:
        """
        Transform API response data
        
        Args:
            data: List of records from API
            field_mapping: Dictionary mapping API fields to target fields
            custom_transforms: List of custom transformation functions
            
        Returns:
            Transformed list of records
        """
        try:
            transformed_data = []
            
            for record in data:
                # Apply field mapping
                if field_mapping:
                    transformed_record = {}
                    for api_field, target_field in field_mapping.items():
                        if api_field in record:
                            transformed_record[target_field] = record[api_field]
                        else:
                            transformed_record[target_field] = None
                    record = transformed_record
                
                # Apply built-in transformations
                for transform_func in self.transformations:
                    record = transform_func(record)
                
                # Apply custom transformations
                if custom_transforms:
                    for transform_func in custom_transforms:
                        record = transform_func(record)
                
                transformed_data.append(record)
            
            logger.info(f"Transformed {len(transformed_data)} records")
            return transformed_data
            
        except Exception as e:
            logger.error(f"Error transforming data: {str(e)}")
            raise
    
    def normalize_dates(
        self,
        data: List[Dict[str, Any]],
        date_fields: List[str]
    ) -> List[Dict[str, Any]]:
        """
        Normalize date fields to ISO format
        
        Args:
            data: List of records
            date_fields: List of field names containing dates
            
        Returns:
            Data with normalized dates
        """
        for record in data:
            for field in date_fields:
                if field in record and record[field]:
                    try:
                        # Try to parse and normalize date
                        if isinstance(record[field], str):
                            # Handle common date formats
                            from dateutil import parser
                            dt = parser.parse(record[field])
                            record[field] = dt.isoformat()
                    except Exception:
                        pass  # Keep original if parsing fails
        
        return data
    
    def flatten_nested(
        self,
        data: List[Dict[str, Any]],
        prefix: str = ""
    ) -> List[Dict[str, Any]]:
        """
        Flatten nested dictionaries
        
        Args:
            data: List of records with nested structures
            prefix: Prefix for flattened field names
            
        Returns:
            Flattened records
        """
        flattened = []
        
        for record in data:
            flat_record = {}
            for key, value in record.items():
                if isinstance(value, dict):
                    # Recursively flatten nested dicts
                    for nested_key, nested_value in value.items():
                        flat_key = f"{prefix}{key}_{nested_key}" if prefix else f"{key}_{nested_key}"
                        flat_record[flat_key] = nested_value
                else:
                    flat_record[key] = value
            flattened.append(flat_record)
        
        return flattened

