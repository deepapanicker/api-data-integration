"""
Incremental Sync Example

This example demonstrates incremental data synchronization from an API.
"""

import sys
import os
import logging
from datetime import datetime

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.clients.rest_client import RESTClient
from src.extractors.incremental_extractor import IncrementalExtractor
from src.transformers.response_transformer import ResponseTransformer
from src.loaders.database_loader import DatabaseLoader

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def main():
    """Main example function"""
    print("=" * 60)
    print("API Data Integration - Incremental Sync Example")
    print("=" * 60)
    print()
    
    # Initialize components
    print("1. Initializing API client...")
    client = RESTClient(
        base_url="https://jsonplaceholder.typicode.com",
        api_key=None
    )
    
    print("2. Initializing incremental extractor...")
    extractor = IncrementalExtractor(
        client=client,
        timestamp_field='updatedAt',  # Field name in API response
        last_sync_file='last_sync.json'
    )
    
    print("3. Running incremental extraction...")
    try:
        # Extract only new/updated records
        new_records = extractor.extract_incremental(
            endpoint="/posts",
            params={}
        )
        
        print(f"   ✅ Extracted {len(new_records)} new/updated records")
        
        if new_records:
            print(f"   Sample record: {new_records[0]}")
            print()
            
            # Transform data
            print("4. Transforming data...")
            transformer = ResponseTransformer()
            transformed = transformer.transform(new_records)
            
            print(f"   ✅ Transformed {len(transformed)} records")
            print()
            
            # Load to database (example - requires database connection)
            print("5. Loading to database...")
            # Uncomment and configure if you have a database
            # loader = DatabaseLoader(connection_string="postgresql://user:pass@localhost/db")
            # result = loader.load(
            #     data=transformed,
            #     table_name="api_posts",
            #     load_mode="upsert",
            #     unique_key="id"
            # )
            # print(f"   ✅ Loaded {result['records_loaded']} records")
            
            print("   ⚠️  Database loading skipped (configure connection_string to enable)")
            print()
        
        print("=" * 60)
        print("✅ Incremental sync completed!")
        print("=" * 60)
        print()
        print("Next sync will only fetch records updated after the last sync timestamp.")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        raise


if __name__ == '__main__':
    main()

