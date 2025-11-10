"""
REST API Client
Simple REST client with API key authentication
"""

import logging
from typing import Dict, Any, Optional
from .base_client import BaseClient

logger = logging.getLogger(__name__)


class RESTClient(BaseClient):
    """REST API client with API key authentication"""
    
    def __init__(
        self,
        base_url: str,
        api_key: Optional[str] = None,
        api_key_header: str = "X-API-Key",
        timeout: int = 30,
        max_retries: int = 3
    ):
        """
        Initialize REST client
        
        Args:
            base_url: Base URL for the API
            api_key: API key for authentication
            api_key_header: Header name for API key
            timeout: Request timeout
            max_retries: Maximum retries
        """
        super().__init__(base_url, timeout, max_retries)
        self.api_key = api_key
        self.api_key_header = api_key_header
    
    def _get_headers(self) -> Dict[str, str]:
        """Get headers including API key"""
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        if self.api_key:
            headers[self.api_key_header] = self.api_key
        
        return headers
    
    def get_json(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Make GET request and return JSON
        
        Args:
            endpoint: API endpoint
            params: Query parameters
            
        Returns:
            JSON response as dictionary
        """
        response = self.get(endpoint, params=params)
        return response.json()
    
    def post_json(
        self,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Make POST request and return JSON
        
        Args:
            endpoint: API endpoint
            data: JSON data to send
            
        Returns:
            JSON response as dictionary
        """
        response = self.post(endpoint, json=data)
        return response.json()

