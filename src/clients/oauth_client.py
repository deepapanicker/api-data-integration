"""
OAuth2 API Client
Client for OAuth2 authenticated APIs
"""

import logging
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
import requests
from requests_oauthlib import OAuth2Session
from .base_client import BaseClient

logger = logging.getLogger(__name__)


class OAuthClient(BaseClient):
    """OAuth2 authenticated API client"""
    
    def __init__(
        self,
        base_url: str,
        client_id: str,
        client_secret: str,
        token_url: str,
        scope: Optional[list] = None,
        timeout: int = 30
    ):
        """
        Initialize OAuth client
        
        Args:
            base_url: Base URL for the API
            client_id: OAuth client ID
            client_secret: OAuth client secret
            token_url: OAuth token endpoint URL
            scope: OAuth scopes
            timeout: Request timeout
        """
        super().__init__(base_url, timeout)
        self.client_id = client_id
        self.client_secret = client_secret
        self.token_url = token_url
        self.scope = scope or []
        self.oauth_session = None
        self.token_expires_at = None
        self._authenticate()
    
    def _authenticate(self):
        """Authenticate and get access token"""
        try:
            oauth = OAuth2Session(
                client_id=self.client_id,
                scope=self.scope
            )
            
            token = oauth.fetch_token(
                token_url=self.token_url,
                client_id=self.client_id,
                client_secret=self.client_secret
            )
            
            self.oauth_session = OAuth2Session(
                client_id=self.client_id,
                token=token
            )
            
            # Calculate token expiration
            expires_in = token.get('expires_in', 3600)
            self.token_expires_at = datetime.now() + timedelta(seconds=expires_in)
            
            logger.info("OAuth authentication successful")
            
        except Exception as e:
            logger.error(f"OAuth authentication failed: {str(e)}")
            raise
    
    def _refresh_token_if_needed(self):
        """Refresh token if expired"""
        if self.token_expires_at and datetime.now() >= self.token_expires_at:
            logger.info("Token expired, refreshing...")
            self._authenticate()
    
    def _get_headers(self) -> Dict[str, str]:
        """Get headers with OAuth token"""
        self._refresh_token_if_needed()
        return {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
    
    def get(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None
    ) -> requests.Response:
        """Make GET request with OAuth"""
        self._refresh_token_if_needed()
        url = self._build_url(endpoint)
        request_headers = {**self._get_headers(), **(headers or {})}
        
        logger.info(f"GET {url}")
        
        try:
            response = self.oauth_session.get(
                url,
                params=params,
                headers=request_headers,
                timeout=self.timeout
            )
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            logger.error(f"GET request failed: {str(e)}")
            raise
    
    def post(
        self,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None
    ) -> requests.Response:
        """Make POST request with OAuth"""
        self._refresh_token_if_needed()
        url = self._build_url(endpoint)
        request_headers = {**self._get_headers(), **(headers or {})}
        
        logger.info(f"POST {url}")
        
        try:
            response = self.oauth_session.post(
                url,
                data=data,
                json=json,
                headers=request_headers,
                timeout=self.timeout
            )
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            logger.error(f"POST request failed: {str(e)}")
            raise

