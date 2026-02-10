"""Test IAM scraper"""

import pytest
from datetime import datetime
from unittest.mock import Mock, MagicMock, patch
from botocore.exceptions import ClientError
from src.scrapers.iam_scraper import IAMScraper


@pytest.fixture
def iam_scraper():
    """Create IAM scraper instance"""
    return IAMScraper(
        account_id="123456789012",
        region="us-east-1",
        profile="test-profile"
    )


@pytest.fixture
def mock_iam_client():
    """Create mock IAM client"""
    client = Mock()
    return client


def test_iam_scraper_initialization(iam_scraper):
    """Test IAM scraper initialization"""
    assert iam_scraper.account_id == "123456789012"
    assert iam_scraper.region == "us-east-1"
    assert iam_scraper.profile == "test-profile"
    assert iam_scraper.get_service_name() == "iam"


def test_scrape_users(iam_scraper, mock_iam_client):
    """Test scraping IAM users"""
    # Mock paginator for list_users
    mock_paginator = Mock()
    mock_paginator.paginate.return_value = [
        {
            'Users': [
                {
                    'UserName': 'test-user-1',
                    'UserId': 'AIDAI123456',
                    'Arn': 'arn:aws:iam::123456789012:user/test-user-1',
                    'CreateDate': datetime(2024, 1, 1),
                    'PasswordLastUsed': datetime(2024, 2, 1)
                },
                {
                    'UserName': 'test-user-2',
                    'UserId': 'AIDAI789012',
                    'Arn': 'arn:aws:iam::123456789012:user/test-user-2',
                    'CreateDate': datetime(2024, 1, 15)
                }
            ]
        }
    ]
    
    mock_iam_client.get_paginator.return_value = mock_paginator
    mock_iam_client.list_mfa_devices.side_effect = [
        {'MFADevices': [{'SerialNumber': 'arn:aws:iam::123:mfa/test'}]},
        {'MFADevices': []}
    ]
    
    users = iam_scraper._scrape_users(mock_iam_client)
    
    assert len(users) == 2
    assert users[0]['user_name'] == 'test-user-1'
    assert users[0]['mfa_enabled'] is True
    assert users[1]['user_name'] == 'test-user-2'
    assert users[1]['mfa_enabled'] is False
    assert users[1]['password_last_used'] is None


def test_scrape_roles(iam_scraper, mock_iam_client):
    """Test scraping IAM roles"""
    mock_paginator = Mock()
    mock_paginator.paginate.return_value = [
        {
            'Roles': [
                {
                    'RoleName': 'test-role-1',
                    'RoleId': 'AROAI123456',
                    'Arn': 'arn:aws:iam::123456789012:role/test-role-1',
                    'CreateDate': datetime(2024, 1, 1),
                    'Description': 'Test role',
                    'MaxSessionDuration': 3600
                }
            ]
        }
    ]
    
    mock_iam_client.get_paginator.return_value = mock_paginator
    
    roles = iam_scraper._scrape_roles(mock_iam_client)
    
    assert len(roles) == 1
    assert roles[0]['role_name'] == 'test-role-1'
    assert roles[0]['description'] == 'Test role'


def test_scrape_policies(iam_scraper, mock_iam_client):
    """Test scraping IAM policies"""
    mock_paginator = Mock()
    mock_paginator.paginate.return_value = [
        {
            'Policies': [
                {
                    'PolicyName': 'test-policy',
                    'PolicyId': 'ANPAI123456',
                    'Arn': 'arn:aws:iam::123456789012:policy/test-policy',
                    'DefaultVersionId': 'v1',
                    'AttachmentCount': 2,
                    'CreateDate': datetime(2024, 1, 1),
                    'Description': 'Test policy'
                }
            ]
        }
    ]
    
    mock_iam_client.get_paginator.return_value = mock_paginator
    
    policies = iam_scraper._scrape_policies(mock_iam_client)
    
    assert len(policies) == 1
    assert policies[0]['policy_name'] == 'test-policy'
    assert policies[0]['attachment_count'] == 2


@patch('src.scrapers.iam_scraper.BaseScraper.session')
def test_scrape_full(mock_session, iam_scraper, mock_iam_client):
    """Test full scrape"""
    mock_session.client.return_value = mock_iam_client
    
    # Setup mock paginators for all operations
    user_paginator = Mock()
    user_paginator.paginate.return_value = [{'Users': []}]
    
    role_paginator = Mock()
    role_paginator.paginate.return_value = [{'Roles': []}]
    
    policy_paginator = Mock()
    policy_paginator.paginate.return_value = [{'Policies': []}]
    
    mock_iam_client.get_paginator.side_effect = [
        user_paginator, role_paginator, policy_paginator
    ]
    
    results = iam_scraper.scrape()
    
    assert 'users' in results
    assert 'roles' in results
    assert 'policies' in results
    assert isinstance(results['users'], list)
    assert isinstance(results['roles'], list)
    assert isinstance(results['policies'], list)


def test_scrape_with_client_error(iam_scraper, mock_iam_client):
    """Test scraping with AWS client error"""
    mock_paginator = Mock()
    error_response = {'Error': {'Code': 'AccessDenied', 'Message': 'Access denied'}}
    mock_paginator.paginate.side_effect = ClientError(error_response, 'ListUsers')
    mock_iam_client.get_paginator.return_value = mock_paginator
    
    with pytest.raises(ClientError):
        iam_scraper._scrape_users(mock_iam_client)
