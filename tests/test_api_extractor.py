"""
Unit tests for APIExtractor
"""

import pytest
from unittest.mock import Mock, patch
from src.clients.rest_client import RESTClient
from src.extractors.api_extractor import APIExtractor


class TestAPIExtractor:
    """Test cases for APIExtractor"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.client = Mock(spec=RESTClient)
        self.extractor = APIExtractor(self.client)
    
    def test_extract_list_response(self):
        """Test extraction with list response"""
        mock_response = Mock()
        mock_response.json.return_value = [{"id": 1}, {"id": 2}]
        self.client.get.return_value = mock_response
        
        result = self.extractor.extract("/test")
        
        assert len(result) == 2
        assert result[0]["id"] == 1
    
    def test_extract_dict_response(self):
        """Test extraction with dict response containing data key"""
        mock_response = Mock()
        mock_response.json.return_value = {"data": [{"id": 1}, {"id": 2}]}
        self.client.get.return_value = mock_response
        
        result = self.extractor.extract("/test")
        
        assert len(result) == 2


if __name__ == '__main__':
    pytest.main([__file__, '-v'])

