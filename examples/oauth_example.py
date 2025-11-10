"""
OAuth2 Authentication Example

This example demonstrates how to use OAuth2 authentication with APIs.
"""

import sys
import os
import logging

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.clients.oauth_client import OAuthClient
from src.extractors.api_extractor import APIExtractor

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def main():
    """Main example function"""
    print("=" * 60)
    print("API Data Integration - OAuth2 Example")
    print("=" * 60)
    print()
    
    print("This example shows how to use OAuth2 authentication.")
    print("Replace the credentials with your actual OAuth2 credentials.")
    print()
    
    # Example OAuth client setup
    # Uncomment and configure with your actual credentials
    """
    client = OAuthClient(
        base_url="https://api.example.com",
        client_id="your-client-id",
        client_secret="your-client-secret",
        token_url="https://api.example.com/oauth/token",
        scope=["read", "write"]
    )
    
    extractor = APIExtractor(client)
    
    # Extract data from protected endpoint
    data = extractor.extract("/api/v1/protected-data")
    print(f"Extracted {len(data)} records")
    """
    
    print("OAuth2 Client Configuration:")
    print("-" * 60)
    print("""
    client = OAuthClient(
        base_url="https://api.example.com",
        client_id="your-client-id",
        client_secret="your-client-secret",
        token_url="https://api.example.com/oauth/token",
        scope=["read", "write"]
    )
    
    extractor = APIExtractor(client)
    data = extractor.extract("/api/v1/endpoint")
    """)


if __name__ == '__main__':
    main()

