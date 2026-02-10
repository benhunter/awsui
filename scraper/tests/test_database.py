"""Test database manager"""

import pytest
import tempfile
import sqlite3
from pathlib import Path
from src.database import DatabaseManager


@pytest.fixture
def temp_db():
    """Create temporary database"""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "test.db"
        
        # Create schema
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        
        # Create minimal schema for testing
        cursor.execute("""
            CREATE TABLE accounts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                account_id TEXT NOT NULL UNIQUE,
                account_name TEXT NOT NULL,
                account_alias TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        cursor.execute("""
            CREATE TABLE iam_users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                account_id TEXT NOT NULL,
                user_name TEXT NOT NULL,
                user_id TEXT,
                arn TEXT,
                create_date TIMESTAMP,
                password_last_used TIMESTAMP,
                mfa_enabled BOOLEAN DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(account_id, user_name)
            )
        """)
        
        cursor.execute("""
            CREATE TABLE scan_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                account_id TEXT NOT NULL,
                service_name TEXT NOT NULL,
                scan_start TIMESTAMP NOT NULL,
                scan_end TIMESTAMP,
                status TEXT NOT NULL,
                error_message TEXT,
                records_collected INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        conn.commit()
        conn.close()
        
        yield str(db_path)


def test_database_connect(temp_db):
    """Test database connection"""
    db = DatabaseManager(temp_db)
    db.connect()
    assert db.connection is not None
    db.close()
    assert db.connection is None


def test_database_context_manager(temp_db):
    """Test database as context manager"""
    db = DatabaseManager(temp_db)
    with db:
        assert db.connection is not None
    # Verify connection is closed after exiting context
    assert db.connection is None


def test_insert_account(temp_db):
    """Test inserting an account"""
    with DatabaseManager(temp_db) as db:
        row_id = db.insert_account(
            account_id="123456789012",
            account_name="Test Account",
            account_alias="test"
        )
        assert row_id > 0
        
        # Verify insertion
        accounts = db.get_accounts()
        assert len(accounts) == 1
        assert accounts[0]['account_id'] == "123456789012"
        assert accounts[0]['account_name'] == "Test Account"


def test_insert_account_update(temp_db):
    """Test updating an existing account"""
    with DatabaseManager(temp_db) as db:
        # Insert
        db.insert_account(
            account_id="123456789012",
            account_name="Test Account"
        )
        
        # Update
        db.insert_account(
            account_id="123456789012",
            account_name="Updated Account"
        )
        
        # Verify only one record exists with updated name
        accounts = db.get_accounts()
        assert len(accounts) == 1
        assert accounts[0]['account_name'] == "Updated Account"


def test_insert_iam_user(temp_db):
    """Test inserting IAM user"""
    with DatabaseManager(temp_db) as db:
        db.insert_account("123456789012", "Test Account")
        
        user_data = {
            'user_name': 'test-user',
            'user_id': 'AIDAI123456',
            'arn': 'arn:aws:iam::123456789012:user/test-user',
            'mfa_enabled': True
        }
        
        row_id = db.insert_iam_user("123456789012", user_data)
        assert row_id > 0


def test_scan_history(temp_db):
    """Test scan history tracking"""
    with DatabaseManager(temp_db) as db:
        db.insert_account("123456789012", "Test Account")
        
        # Start scan
        scan_id = db.start_scan("123456789012", "iam")
        assert scan_id > 0
        
        # End scan
        db.end_scan(scan_id, "completed", records_collected=10)
        
        # Verify
        cursor = db.execute("SELECT * FROM scan_history WHERE id = ?", (scan_id,))
        scan = dict(cursor.fetchone())
        assert scan['status'] == "completed"
        assert scan['records_collected'] == 10


def test_scan_history_with_error(temp_db):
    """Test scan history with error"""
    with DatabaseManager(temp_db) as db:
        db.insert_account("123456789012", "Test Account")
        
        scan_id = db.start_scan("123456789012", "iam")
        db.end_scan(scan_id, "failed", error_message="Connection timeout")
        
        cursor = db.execute("SELECT * FROM scan_history WHERE id = ?", (scan_id,))
        scan = dict(cursor.fetchone())
        assert scan['status'] == "failed"
        assert scan['error_message'] == "Connection timeout"
