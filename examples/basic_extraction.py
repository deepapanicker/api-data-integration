"""
Basic API Extraction Example

This example demonstrates basic API data extraction using the framework.
"""

import sys
import os
import logging

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.clients.rest_client import RESTClient
from src.extractors.api_extractor import APIExtractor
from src.transformers.response_transformer import ResponseTransformer
from src.utils.rate_limiter import RateLimiter
from src.utils.error_handler import ErrorHandler

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def main():
    """Main example function"""
    print("=" * 60)
    print("API Data Integration - Basic Extraction Example")
    print("=" * 60)
    print()
    
    # Initialize components
    print("1. Initializing API client...")
    client = RESTClient(
        base_url="https://jsonplaceholder.typicode.com",  # Example API
        api_key=None  # This API doesn't require authentication
    )
    
    print("2. Initializing extractor...")
    extractor = APIExtractor(client)
    
    print("3. Extracting data from API...")
    try:
        # Extract users data
        users = extractor.extract(
            endpoint="/users",
            pagination=False
        )
        
        print(f"   ✅ Extracted {len(users)} users")
        print(f"   Sample user: {users[0] if users else 'No data'}")
        print()
        
        # Extract posts data
        posts = extractor.extract(
            endpoint="/posts",
            pagination=True,
            page_size=10
        )
        
        print(f"   ✅ Extracted {len(posts)} posts")
        print(f"   Sample post: {posts[0] if posts else 'No data'}")
        print()
        
        # Transform data
        print("4. Transforming data...")
        transformer = ResponseTransformer()
        
        # Example: Flatten nested user address
        def flatten_address(record):
            if 'address' in record and isinstance(record['address'], dict):
                address = record['address']
                record['street'] = address.get('street', '')
                record['city'] = address.get('city', '')
                record['zipcode'] = address.get('zipcode', '')
                del record['address']
            return record
        
        transformed_users = transformer.transform(
            users[:3],  # Transform first 3 for example
            custom_transforms=[flatten_address]
        )
        
        print(f"   ✅ Transformed {len(transformed_users)} records")
        print(f"   Transformed sample: {transformed_users[0] if transformed_users else 'No data'}")
        print()
        
        print("=" * 60)
        print("✅ Extraction completed successfully!")
        print("=" * 60)
        
    except Exception as e:
        error_handler = ErrorHandler()
        error_info = error_handler.handle_error(e, context={'endpoint': '/users'})
        print(f"❌ Error: {error_info['error_message']}")
        raise


if __name__ == '__main__':
    main()

