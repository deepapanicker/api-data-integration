"""
Incremental Extractor
Extracts only new/updated data since last sync
"""

import logging
import json
from typing import List, Dict, Any, Optional
from pathlib import Path
from datetime import datetime
from ..clients.base_client import BaseClient
from .api_extractor import APIExtractor

logger = logging.getLogger(__name__)


class IncrementalExtractor(APIExtractor):
    """Extract data incrementally based on timestamps"""
    
    def __init__(
        self,
        client: BaseClient,
        timestamp_field: str = 'updated_at',
        last_sync_file: str = 'last_sync.json'
    ):
        """
        Initialize incremental extractor
        
        Args:
            client: API client instance
            timestamp_field: Field name containing timestamp
            last_sync_file: Path to file storing last sync timestamp
        """
        super().__init__(client)
        self.timestamp_field = timestamp_field
        self.last_sync_file = Path(last_sync_file)
        self.last_sync_timestamp = self._load_last_sync()
    
    def _load_last_sync(self) -> Optional[datetime]:
        """Load last sync timestamp from file"""
        if self.last_sync_file.exists():
            try:
                with open(self.last_sync_file, 'r') as f:
                    data = json.load(f)
                    timestamp_str = data.get('last_sync')
                    if timestamp_str:
                        return datetime.fromisoformat(timestamp_str)
            except Exception as e:
                logger.warning(f"Error loading last sync: {str(e)}")
        return None
    
    def _save_last_sync(self, timestamp: datetime):
        """Save last sync timestamp to file"""
        try:
            self.last_sync_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.last_sync_file, 'w') as f:
                json.dump({
                    'last_sync': timestamp.isoformat(),
                    'updated_at': datetime.now().isoformat()
                }, f, indent=2)
            logger.info(f"Saved last sync timestamp: {timestamp.isoformat()}")
        except Exception as e:
            logger.error(f"Error saving last sync: {str(e)}")
    
    def extract_incremental(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Extract only records updated since last sync
        
        Args:
            endpoint: API endpoint
            params: Query parameters
            
        Returns:
            List of new/updated records
        """
        try:
            # Add timestamp filter to params
            query_params = params or {}
            
            if self.last_sync_timestamp:
                # Format timestamp for API (adjust format as needed)
                timestamp_str = self.last_sync_timestamp.isoformat()
                query_params[f'{self.timestamp_field}_gte'] = timestamp_str
                logger.info(f"Extracting records updated after: {timestamp_str}")
            else:
                logger.info("No previous sync found, extracting all records")
            
            # Extract data
            all_records = self.extract(endpoint, params=query_params, pagination=True)
            
            # Filter records by timestamp (in case API doesn't filter properly)
            if self.last_sync_timestamp and all_records:
                filtered_records = []
                for record in all_records:
                    record_timestamp_str = record.get(self.timestamp_field)
                    if record_timestamp_str:
                        try:
                            record_timestamp = datetime.fromisoformat(record_timestamp_str.replace('Z', '+00:00'))
                            if record_timestamp > self.last_sync_timestamp:
                                filtered_records.append(record)
                        except Exception:
                            # If timestamp parsing fails, include the record
                            filtered_records.append(record)
                    else:
                        # If no timestamp field, include the record
                        filtered_records.append(record)
                
                all_records = filtered_records
            
            # Update last sync timestamp
            if all_records:
                # Find the latest timestamp
                latest_timestamp = self.last_sync_timestamp or datetime.min
                for record in all_records:
                    record_timestamp_str = record.get(self.timestamp_field)
                    if record_timestamp_str:
                        try:
                            record_timestamp = datetime.fromisoformat(record_timestamp_str.replace('Z', '+00:00'))
                            if record_timestamp > latest_timestamp:
                                latest_timestamp = record_timestamp
                        except Exception:
                            pass
                
                self._save_last_sync(latest_timestamp)
            
            logger.info(f"Extracted {len(all_records)} incremental records")
            return all_records
            
        except Exception as e:
            logger.error(f"Error in incremental extraction: {str(e)}")
            raise

