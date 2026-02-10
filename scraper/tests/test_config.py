"""Test configuration loader"""

import pytest
import tempfile
import os
from pathlib import Path
from src.config import Config


@pytest.fixture
def temp_config_dir():
    """Create temporary directory for config files"""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def sample_config_yaml(temp_config_dir):
    """Create sample config.yaml"""
    config_content = """
database:
  path: "../database/awsui.db"

scraper:
  parallel_accounts: 3
  parallel_regions: 2
  services:
    - iam
    - securityhub
    - guardduty

logging:
  level: "INFO"
"""
    config_file = temp_config_dir / "config.yaml"
    config_file.write_text(config_content)
    return config_file


@pytest.fixture
def sample_accounts_yaml(temp_config_dir):
    """Create sample accounts.yaml"""
    accounts_content = """
accounts:
  - name: "Production"
    account_id: "123456789012"
    profile: "prod-profile"
    regions:
      - "us-east-1"
      - "us-west-2"
  - name: "Development"
    account_id: "210987654321"
    profile: "dev-profile"
    regions:
      - "us-east-1"
"""
    accounts_file = temp_config_dir / "accounts.yaml"
    accounts_file.write_text(accounts_content)
    return accounts_file


def test_config_initialization(sample_config_yaml, sample_accounts_yaml):
    """Test configuration initialization"""
    config = Config(
        config_path=str(sample_config_yaml),
        accounts_path=str(sample_accounts_yaml)
    )
    
    assert config.database_path == "../database/awsui.db"
    assert config.parallel_accounts == 3
    assert config.parallel_regions == 2
    assert config.log_level == "INFO"


def test_config_accounts(sample_config_yaml, sample_accounts_yaml):
    """Test accounts loading"""
    config = Config(
        config_path=str(sample_config_yaml),
        accounts_path=str(sample_accounts_yaml)
    )
    
    accounts = config.accounts
    assert len(accounts) == 2
    assert accounts[0]['name'] == "Production"
    assert accounts[0]['account_id'] == "123456789012"
    assert accounts[1]['name'] == "Development"


def test_config_services(sample_config_yaml, sample_accounts_yaml):
    """Test services list"""
    config = Config(
        config_path=str(sample_config_yaml),
        accounts_path=str(sample_accounts_yaml)
    )
    
    services = config.services
    assert len(services) == 3
    assert 'iam' in services
    assert 'securityhub' in services
    assert 'guardduty' in services


def test_config_defaults_when_files_missing():
    """Test default values when config files don't exist"""
    config = Config(
        config_path="/nonexistent/config.yaml",
        accounts_path="/nonexistent/accounts.yaml"
    )
    
    assert config.accounts == []
    assert config.services == []
    assert config.parallel_accounts == 1
    assert config.log_level == "INFO"
