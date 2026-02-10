"""Base scraper class for AWS services"""

import logging
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
import boto3
from botocore.exceptions import ClientError, BotoCoreError


logger = logging.getLogger(__name__)


class BaseScraper(ABC):
    """Base class for AWS service scrapers"""
    
    def __init__(self, account_id: str, region: str, profile: Optional[str] = None):
        """
        Initialize scraper
        
        Args:
            account_id: AWS account ID
            region: AWS region
            profile: AWS profile name (optional)
        """
        self.account_id = account_id
        self.region = region
        self.profile = profile
        self._session: Optional[boto3.Session] = None
    
    @property
    def session(self) -> boto3.Session:
        """Get or create boto3 session"""
        if not self._session:
            if self.profile:
                self._session = boto3.Session(
                    profile_name=self.profile,
                    region_name=self.region
                )
            else:
                self._session = boto3.Session(region_name=self.region)
        return self._session
    
    @abstractmethod
    def scrape(self) -> List[Dict[str, Any]]:
        """
        Scrape data from AWS service
        
        Returns:
            List of scraped data items
        """
        pass
    
    @abstractmethod
    def get_service_name(self) -> str:
        """
        Get the name of the AWS service
        
        Returns:
            Service name
        """
        pass
    
    def handle_error(self, error: Exception, context: str = "") -> None:
        """
        Handle and log errors
        
        Args:
            error: Exception that occurred
            context: Additional context information
        """
        error_msg = f"Error in {self.get_service_name()} scraper"
        if context:
            error_msg += f" ({context})"
        error_msg += f": {str(error)}"
        
        logger.error(error_msg)
        
        if isinstance(error, ClientError):
            error_code = error.response.get('Error', {}).get('Code', 'Unknown')
            logger.error(f"AWS Error Code: {error_code}")
