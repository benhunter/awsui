"""Database manager for storing AWS data"""

import sqlite3
import logging
from pathlib import Path
from typing import Optional, List, Dict, Any
from datetime import datetime


logger = logging.getLogger(__name__)


class DatabaseManager:
    """Manages SQLite database connections and operations"""
    
    def __init__(self, db_path: str):
        """
        Initialize database manager
        
        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = Path(db_path)
        self.connection: Optional[sqlite3.Connection] = None
        
    def connect(self):
        """Establish database connection"""
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.connection = sqlite3.connect(str(self.db_path))
        self.connection.row_factory = sqlite3.Row
        logger.info(f"Connected to database: {self.db_path}")
        
    def close(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()
            self.connection = None
            logger.info("Database connection closed")
    
    def execute(self, query: str, params: tuple = ()) -> sqlite3.Cursor:
        """
        Execute a SQL query
        
        Args:
            query: SQL query string
            params: Query parameters
            
        Returns:
            Cursor object
        """
        if not self.connection:
            raise RuntimeError("Database not connected")
        return self.connection.execute(query, params)
    
    def commit(self):
        """Commit current transaction"""
        if self.connection:
            self.connection.commit()
    
    def insert_account(self, account_id: str, account_name: str, 
                      account_alias: Optional[str] = None) -> int:
        """
        Insert or update an account
        
        Args:
            account_id: AWS account ID
            account_name: Account name
            account_alias: Account alias (optional)
            
        Returns:
            Row ID
        """
        cursor = self.execute(
            """
            INSERT INTO accounts (account_id, account_name, account_alias, updated_at)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(account_id) DO UPDATE SET
                account_name = excluded.account_name,
                account_alias = excluded.account_alias,
                updated_at = excluded.updated_at
            """,
            (account_id, account_name, account_alias, datetime.now())
        )
        self.commit()
        return cursor.lastrowid
    
    def insert_iam_user(self, account_id: str, user_data: Dict[str, Any]) -> int:
        """Insert or update IAM user"""
        cursor = self.execute(
            """
            INSERT INTO iam_users (
                account_id, user_name, user_id, arn, create_date,
                password_last_used, mfa_enabled, updated_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(account_id, user_name) DO UPDATE SET
                user_id = excluded.user_id,
                arn = excluded.arn,
                password_last_used = excluded.password_last_used,
                mfa_enabled = excluded.mfa_enabled,
                updated_at = excluded.updated_at
            """,
            (
                account_id,
                user_data['user_name'],
                user_data.get('user_id'),
                user_data.get('arn'),
                user_data.get('create_date'),
                user_data.get('password_last_used'),
                user_data.get('mfa_enabled', False),
                datetime.now()
            )
        )
        self.commit()
        return cursor.lastrowid
    
    def start_scan(self, account_id: str, service_name: str) -> int:
        """Record the start of a scan"""
        cursor = self.execute(
            """
            INSERT INTO scan_history (account_id, service_name, scan_start, status)
            VALUES (?, ?, ?, 'running')
            """,
            (account_id, service_name, datetime.now())
        )
        self.commit()
        return cursor.lastrowid
    
    def end_scan(self, scan_id: int, status: str, records_collected: int = 0,
                error_message: Optional[str] = None):
        """Record the end of a scan"""
        self.execute(
            """
            UPDATE scan_history
            SET scan_end = ?, status = ?, records_collected = ?, error_message = ?
            WHERE id = ?
            """,
            (datetime.now(), status, records_collected, error_message, scan_id)
        )
        self.commit()
    
    def get_accounts(self) -> List[Dict[str, Any]]:
        """Get all accounts from database"""
        cursor = self.execute("SELECT * FROM accounts")
        return [dict(row) for row in cursor.fetchall()]
    
    def __enter__(self):
        """Context manager entry"""
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close()
