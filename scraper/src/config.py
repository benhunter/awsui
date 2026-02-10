"""Configuration loader for the scraper"""

import os
import yaml
from pathlib import Path
from typing import Dict, List, Any


class Config:
    """Configuration management for AWS scraper"""
    
    def __init__(self, config_path: str = None, accounts_path: str = None):
        """
        Initialize configuration
        
        Args:
            config_path: Path to config.yaml (default: ./config.yaml)
            accounts_path: Path to accounts.yaml (default: ./accounts.yaml)
        """
        self.config_path = config_path or self._find_file("config.yaml")
        self.accounts_path = accounts_path or self._find_file("accounts.yaml")
        
        self._config: Dict[str, Any] = {}
        self._accounts: List[Dict[str, Any]] = []
        
        self._load_config()
        self._load_accounts()
    
    def _find_file(self, filename: str) -> str:
        """Find configuration file in current or parent directories"""
        current = Path.cwd()
        for _ in range(3):  # Check up to 3 levels up
            candidate = current / filename
            if candidate.exists():
                return str(candidate)
            current = current.parent
        return filename  # Return default if not found
    
    def _load_config(self):
        """Load scraper configuration from YAML"""
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r') as f:
                self._config = yaml.safe_load(f) or {}
    
    def _load_accounts(self):
        """Load AWS accounts configuration from YAML"""
        if os.path.exists(self.accounts_path):
            with open(self.accounts_path, 'r') as f:
                data = yaml.safe_load(f) or {}
                self._accounts = data.get('accounts', [])
    
    @property
    def accounts(self) -> List[Dict[str, Any]]:
        """Get list of configured AWS accounts"""
        return self._accounts
    
    @property
    def database_path(self) -> str:
        """Get database path"""
        return self._config.get('database', {}).get('path', '../database/awsui.db')
    
    @property
    def services(self) -> List[str]:
        """Get list of services to scrape"""
        return self._config.get('scraper', {}).get('services', [])
    
    @property
    def parallel_accounts(self) -> int:
        """Get number of accounts to scrape in parallel"""
        return self._config.get('scraper', {}).get('parallel_accounts', 1)
    
    @property
    def parallel_regions(self) -> int:
        """Get number of regions to scrape in parallel"""
        return self._config.get('scraper', {}).get('parallel_regions', 1)
    
    @property
    def log_level(self) -> str:
        """Get logging level"""
        return self._config.get('logging', {}).get('level', 'INFO')
