"""CLI for running AWS scraper"""

import sys
import logging
import argparse
from pathlib import Path

from .config import Config
from .database import DatabaseManager
from .scrapers import IAMScraper


# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def run_scraper(config: Config, service: str = None):
    """
    Run scraper for specified service or all services
    
    Args:
        config: Configuration object
        service: Service name to scrape (None for all)
    """
    # Initialize database
    db_path = Path(__file__).parent.parent.parent / config.database_path
    db = DatabaseManager(str(db_path))
    
    with db:
        # Get accounts to scrape
        accounts = config.accounts
        
        if not accounts:
            logger.error("No accounts configured. Please update accounts.yaml")
            return
        
        logger.info(f"Starting scrape for {len(accounts)} account(s)")
        
        # Services to scrape
        services_to_scrape = [service] if service else config.services
        
        if not services_to_scrape:
            logger.warning("No services configured to scrape")
            return
        
        # Iterate through accounts
        for account in accounts:
            account_id = account['account_id']
            account_name = account['name']
            profile = account.get('profile')
            regions = account.get('regions', ['us-east-1'])
            
            logger.info(f"Processing account: {account_name} ({account_id})")
            
            # Insert/update account in database
            db.insert_account(account_id, account_name, account.get('alias'))
            
            # Use first region for IAM (IAM is global)
            region = regions[0] if regions else 'us-east-1'
            
            # Scrape services
            for service_name in services_to_scrape:
                scan_id = db.start_scan(account_id, service_name)
                
                try:
                    if service_name == 'iam':
                        scraper = IAMScraper(account_id, region, profile)
                        results = scraper.scrape()
                        
                        # Store results
                        user_count = 0
                        for user in results.get('users', []):
                            db.insert_iam_user(account_id, user)
                            user_count += 1
                        
                        total_records = user_count
                        db.end_scan(scan_id, 'completed', total_records)
                        logger.info(f"Completed {service_name} scrape: {total_records} records")
                    
                    else:
                        logger.warning(f"Service '{service_name}' not yet implemented")
                        db.end_scan(scan_id, 'skipped', 0, f"Service not implemented")
                
                except Exception as e:
                    logger.error(f"Error scraping {service_name}: {str(e)}")
                    db.end_scan(scan_id, 'failed', 0, str(e))
        
        logger.info("Scraping completed")


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(description='AWS Multi-Account Scraper')
    parser.add_argument(
        '--service',
        type=str,
        help='Specific service to scrape (default: all configured services)'
    )
    parser.add_argument(
        '--config',
        type=str,
        help='Path to config.yaml'
    )
    parser.add_argument(
        '--accounts',
        type=str,
        help='Path to accounts.yaml'
    )
    parser.add_argument(
        '--debug',
        action='store_true',
        help='Enable debug logging'
    )
    
    args = parser.parse_args()
    
    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
    
    try:
        # Load configuration
        config = Config(config_path=args.config, accounts_path=args.accounts)
        
        # Run scraper
        run_scraper(config, args.service)
        
    except KeyboardInterrupt:
        logger.info("Scraping interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}", exc_info=True)
        sys.exit(1)


if __name__ == '__main__':
    main()
