"""
API Extractor
Extracts data from REST APIs
"""

import logging
from typing import List, Dict, Any, Optional
from ..clients.base_client import BaseClient

logger = logging.getLogger(__name__)


class APIExtractor:
    """Extract data from APIs"""
    
    def __init__(self, client: BaseClient):
        """
        Initialize API extractor
        
        Args:
            client: API client instance
        """
        self.client = client
    
    def extract(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        pagination: bool = False,
        page_size: int = 100
    ) -> List[Dict[str, Any]]:
        """
        Extract data from API endpoint
        
        Args:
            endpoint: API endpoint
            params: Query parameters
            pagination: Enable pagination
            page_size: Items per page
            
        Returns:
            List of records
        """
        try:
            all_data = []
            
            if pagination:
                page = 1
                while True:
                    paginated_params = {
                        **(params or {}),
                        'page': page,
                        'per_page': page_size
                    }
                    
                    response = self.client.get(endpoint, params=paginated_params)
                    data = response.json()
                    
                    # Handle different pagination formats
                    if isinstance(data, list):
                        records = data
                    elif isinstance(data, dict):
                        records = data.get('data', data.get('results', data.get('items', [])))
                    else:
                        records = []
                    
                    if not records:
                        break
                    
                    all_data.extend(records)
                    logger.info(f"Extracted page {page}: {len(records)} records")
                    
                    # Check if there are more pages
                    if isinstance(data, dict):
                        if not data.get('has_more', True) or page >= data.get('total_pages', page):
                            break
                    
                    page += 1
            else:
                response = self.client.get(endpoint, params=params)
                data = response.json()
                
                if isinstance(data, list):
                    all_data = data
                elif isinstance(data, dict):
                    all_data = data.get('data', data.get('results', data.get('items', [data])))
                else:
                    all_data = [data]
            
            logger.info(f"Total records extracted: {len(all_data)}")
            return all_data
            
        except Exception as e:
            logger.error(f"Error extracting data: {str(e)}")
            raise
    
    def extract_single(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Extract a single record from API
        
        Args:
            endpoint: API endpoint
            params: Query parameters
            
        Returns:
            Single record as dictionary
        """
        response = self.client.get(endpoint, params=params)
        return response.json()

