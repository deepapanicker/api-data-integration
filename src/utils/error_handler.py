"""
Error Handler
Handles and logs API errors
"""

import logging
from typing import Dict, Any, Optional
from datetime import datetime
import traceback

logger = logging.getLogger(__name__)


class ErrorHandler:
    """Handle API errors"""
    
    def __init__(self, log_file: Optional[str] = None):
        """
        Initialize error handler
        
        Args:
            log_file: Optional file path for error logs
        """
        self.log_file = log_file
        self.error_history = []
    
    def handle_error(
        self,
        error: Exception,
        context: Optional[Dict[str, Any]] = None,
        retry: bool = False
    ) -> Dict[str, Any]:
        """
        Handle an error
        
        Args:
            error: Exception that occurred
            context: Additional context information
            retry: Whether to retry the operation
            
        Returns:
            Dictionary with error information
        """
        error_info = {
            'timestamp': datetime.now().isoformat(),
            'error_type': type(error).__name__,
            'error_message': str(error),
            'context': context or {},
            'traceback': traceback.format_exc(),
            'retry': retry
        }
        
        # Log error
        logger.error(f"Error occurred: {error_info['error_message']}")
        if context:
            logger.error(f"Context: {context}")
        
        # Add to history
        self.error_history.append(error_info)
        
        # Write to log file if specified
        if self.log_file:
            self._write_to_log(error_info)
        
        return error_info
    
    def _write_to_log(self, error_info: Dict[str, Any]):
        """Write error to log file"""
        try:
            from pathlib import Path
            log_path = Path(self.log_file)
            log_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(log_path, 'a') as f:
                f.write(f"\n{'='*60}\n")
                f.write(f"Timestamp: {error_info['timestamp']}\n")
                f.write(f"Error Type: {error_info['error_type']}\n")
                f.write(f"Error Message: {error_info['error_message']}\n")
                if error_info['context']:
                    f.write(f"Context: {error_info['context']}\n")
                f.write(f"Traceback:\n{error_info['traceback']}\n")
        except Exception as e:
            logger.error(f"Error writing to log file: {str(e)}")
    
    def get_error_summary(self) -> Dict[str, Any]:
        """Get summary of errors"""
        if not self.error_history:
            return {'total_errors': 0}
        
        error_types = {}
        for error in self.error_history:
            error_type = error['error_type']
            error_types[error_type] = error_types.get(error_type, 0) + 1
        
        return {
            'total_errors': len(self.error_history),
            'error_types': error_types,
            'latest_error': self.error_history[-1] if self.error_history else None
        }

