"""
Database Loader
Loads extracted data into databases
"""

import logging
from typing import List, Dict, Any, Optional
import pandas as pd
from sqlalchemy import create_engine, text

logger = logging.getLogger(__name__)


class DatabaseLoader:
    """Load data to database"""
    
    def __init__(self, connection_string: str):
        """
        Initialize database loader
        
        Args:
            connection_string: Database connection string
        """
        self.connection_string = connection_string
        self.engine = None
    
    def _get_engine(self):
        """Get or create database engine"""
        if self.engine is None:
            self.engine = create_engine(self.connection_string)
        return self.engine
    
    def load(
        self,
        data: List[Dict[str, Any]],
        table_name: str,
        load_mode: str = 'append',
        unique_key: Optional[str] = None,
        chunksize: int = 1000
    ) -> Dict[str, Any]:
        """
        Load data to database table
        
        Args:
            data: List of records to load
            table_name: Target table name
            load_mode: 'append', 'replace', or 'upsert'
            unique_key: Column name for upsert operations
            chunksize: Number of records per batch
            
        Returns:
            Dictionary with load results
        """
        try:
            if not data:
                logger.warning("No data to load")
                return {'records_loaded': 0, 'status': 'skipped'}
            
            engine = self._get_engine()
            df = pd.DataFrame(data)
            
            logger.info(f"Loading {len(df)} records to {table_name} using {load_mode} mode")
            
            if load_mode == 'append':
                df.to_sql(
                    table_name,
                    engine,
                    if_exists='append',
                    index=False,
                    chunksize=chunksize,
                    method='multi'
                )
                
            elif load_mode == 'replace':
                df.to_sql(
                    table_name,
                    engine,
                    if_exists='replace',
                    index=False,
                    chunksize=chunksize,
                    method='multi'
                )
                
            elif load_mode == 'upsert':
                if not unique_key:
                    raise ValueError("unique_key must be provided for upsert mode")
                self._upsert(df, table_name, unique_key, chunksize)
                
            else:
                raise ValueError(f"Unknown load_mode: {load_mode}")
            
            logger.info(f"Successfully loaded {len(df)} records")
            return {
                'records_loaded': len(df),
                'status': 'success',
                'table': table_name
            }
            
        except Exception as e:
            logger.error(f"Error loading data: {str(e)}")
            raise
    
    def _upsert(
        self,
        df: pd.DataFrame,
        table_name: str,
        unique_key: str,
        chunksize: int = 1000
    ):
        """Perform upsert operation"""
        engine = self._get_engine()
        
        # Get existing columns
        with engine.connect() as conn:
            result = conn.execute(text(f"SELECT * FROM {table_name} LIMIT 0"))
            columns = [col.name for col in result.cursor.description] if hasattr(result, 'cursor') else df.columns.tolist()
        
        # Process in chunks
        for i in range(0, len(df), chunksize):
            chunk = df.iloc[i:i+chunksize]
            
            # Build upsert query (PostgreSQL syntax)
            # Adjust for your database
            set_clause = ', '.join([f"{col} = EXCLUDED.{col}" for col in columns if col != unique_key])
            
            # Convert chunk to list of tuples for insertion
            values = [tuple(row) for row in chunk.values]
            columns_str = ', '.join(columns)
            placeholders = ', '.join(['%s'] * len(columns))
            
            upsert_query = f"""
                INSERT INTO {table_name} ({columns_str})
                VALUES ({placeholders})
                ON CONFLICT ({unique_key}) 
                DO UPDATE SET {set_clause}
            """
            
            with engine.connect() as conn:
                conn.execute(text(upsert_query), values)
                conn.commit()
        
        logger.info(f"Upserted {len(df)} records")

