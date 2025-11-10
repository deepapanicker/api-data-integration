"""
Unit tests for RESTClient
"""

import pytest
from unittest.mock import Mock, patch
from src.clients.rest_client import RESTClient


class TestRESTClient:
    """Test cases for RESTClient"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.client = RESTClient(
            base_url="https://api.example.com",
            api_key="test-api-key"
        )
    
    def test_init(self):
        """Test client initialization"""
        assert self.client.base_url == "https://api.example.com"
        assert self.client.api_key == "test-api-key"
    
    def test_get_headers(self):
        """Test header generation"""
        headers = self.client._get_headers()
        assert "Content-Type" in headers
        assert "X-API-Key" in headers
        assert headers["X-API-Key"] == "test-api-key"
    
    @patch('src.clients.rest_client.requests.Session.get')
    def test_get_json(self, mock_get):
        """Test GET request returning JSON"""
        mock_response = Mock()
        mock_response.json.return_value = {"data": "test"}
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        result = self.client.get_json("/test")
        
        assert result == {"data": "test"}
        mock_get.assert_called_once()


if __name__ == '__main__':
    pytest.main([__file__, '-v'])

