"""
Rate Limiter
Implements rate limiting for API requests
"""

import logging
import time
from typing import Optional
from threading import Lock

logger = logging.getLogger(__name__)


class RateLimiter:
    """Rate limiter for API requests"""
    
    def __init__(
        self,
        requests_per_second: float = 10.0,
        requests_per_minute: Optional[float] = None
    ):
        """
        Initialize rate limiter
        
        Args:
            requests_per_second: Maximum requests per second
            requests_per_minute: Maximum requests per minute (optional)
        """
        self.requests_per_second = requests_per_second
        self.requests_per_minute = requests_per_minute
        self.min_interval = 1.0 / requests_per_second if requests_per_second > 0 else 0
        self.last_request_time = 0.0
        self.request_times = []
        self.lock = Lock()
    
    def wait_if_needed(self):
        """Wait if necessary to respect rate limits"""
        with self.lock:
            current_time = time.time()
            
            # Per-second rate limiting
            time_since_last = current_time - self.last_request_time
            if time_since_last < self.min_interval:
                sleep_time = self.min_interval - time_since_last
                logger.debug(f"Rate limiting: sleeping {sleep_time:.2f} seconds")
                time.sleep(sleep_time)
            
            # Per-minute rate limiting
            if self.requests_per_minute:
                # Remove requests older than 1 minute
                self.request_times = [
                    t for t in self.request_times
                    if current_time - t < 60
                ]
                
                if len(self.request_times) >= self.requests_per_minute:
                    # Wait until oldest request is 1 minute old
                    oldest_time = min(self.request_times)
                    wait_time = 60 - (current_time - oldest_time) + 0.1
                    if wait_time > 0:
                        logger.debug(f"Rate limiting: sleeping {wait_time:.2f} seconds (minute limit)")
                        time.sleep(wait_time)
                        # Clean up again
                        current_time = time.time()
                        self.request_times = [
                            t for t in self.request_times
                            if current_time - t < 60
                        ]
            
            # Record this request
            self.last_request_time = time.time()
            if self.requests_per_minute:
                self.request_times.append(self.last_request_time)

