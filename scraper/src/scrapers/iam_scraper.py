"""IAM scraper for collecting IAM users, roles, and policies"""

import logging
from typing import Dict, Any, List
from datetime import datetime
from botocore.exceptions import ClientError
from ..base_scraper import BaseScraper


logger = logging.getLogger(__name__)


class IAMScraper(BaseScraper):
    """Scraper for AWS IAM service"""
    
    def get_service_name(self) -> str:
        """Get service name"""
        return "iam"
    
    def scrape(self) -> List[Dict[str, Any]]:
        """
        Scrape IAM data
        
        Returns:
            List containing users, roles, and policies
        """
        results = {
            'users': [],
            'roles': [],
            'policies': []
        }
        
        try:
            iam_client = self.session.client('iam')
            
            # Scrape users
            results['users'] = self._scrape_users(iam_client)
            logger.info(f"Scraped {len(results['users'])} IAM users")
            
            # Scrape roles
            results['roles'] = self._scrape_roles(iam_client)
            logger.info(f"Scraped {len(results['roles'])} IAM roles")
            
            # Scrape policies
            results['policies'] = self._scrape_policies(iam_client)
            logger.info(f"Scraped {len(results['policies'])} IAM policies")
            
        except ClientError as e:
            self.handle_error(e, "scraping IAM data")
            raise
        
        return results
    
    def _scrape_users(self, iam_client) -> List[Dict[str, Any]]:
        """Scrape IAM users"""
        users = []
        paginator = iam_client.get_paginator('list_users')
        
        try:
            for page in paginator.paginate():
                for user in page['Users']:
                    user_data = {
                        'user_name': user['UserName'],
                        'user_id': user['UserId'],
                        'arn': user['Arn'],
                        'create_date': user['CreateDate'].isoformat() if isinstance(user['CreateDate'], datetime) else user['CreateDate'],
                        'password_last_used': None,
                        'mfa_enabled': False
                    }
                    
                    # Get password last used
                    if 'PasswordLastUsed' in user:
                        user_data['password_last_used'] = user['PasswordLastUsed'].isoformat() if isinstance(user['PasswordLastUsed'], datetime) else user['PasswordLastUsed']
                    
                    # Check MFA devices
                    try:
                        mfa_response = iam_client.list_mfa_devices(UserName=user['UserName'])
                        user_data['mfa_enabled'] = len(mfa_response['MFADevices']) > 0
                    except ClientError:
                        pass  # If we can't get MFA info, leave as False
                    
                    users.append(user_data)
        except ClientError as e:
            self.handle_error(e, "listing users")
            raise
        
        return users
    
    def _scrape_roles(self, iam_client) -> List[Dict[str, Any]]:
        """Scrape IAM roles"""
        roles = []
        paginator = iam_client.get_paginator('list_roles')
        
        try:
            for page in paginator.paginate():
                for role in page['Roles']:
                    role_data = {
                        'role_name': role['RoleName'],
                        'role_id': role['RoleId'],
                        'arn': role['Arn'],
                        'create_date': role['CreateDate'].isoformat() if isinstance(role['CreateDate'], datetime) else role['CreateDate'],
                        'description': role.get('Description', ''),
                        'max_session_duration': role.get('MaxSessionDuration', 3600)
                    }
                    roles.append(role_data)
        except ClientError as e:
            self.handle_error(e, "listing roles")
            raise
        
        return roles
    
    def _scrape_policies(self, iam_client) -> List[Dict[str, Any]]:
        """Scrape IAM policies (customer managed only)"""
        policies = []
        paginator = iam_client.get_paginator('list_policies')
        
        try:
            # Only get customer managed policies
            for page in paginator.paginate(Scope='Local'):
                for policy in page['Policies']:
                    policy_data = {
                        'policy_name': policy['PolicyName'],
                        'policy_id': policy['PolicyId'],
                        'arn': policy['Arn'],
                        'default_version_id': policy['DefaultVersionId'],
                        'attachment_count': policy.get('AttachmentCount', 0),
                        'create_date': policy['CreateDate'].isoformat() if isinstance(policy['CreateDate'], datetime) else policy['CreateDate'],
                        'description': policy.get('Description', '')
                    }
                    policies.append(policy_data)
        except ClientError as e:
            self.handle_error(e, "listing policies")
            raise
        
        return policies
