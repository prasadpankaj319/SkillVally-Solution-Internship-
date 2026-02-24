"""
Database module for Safe Banking System.

This module handles all database operations including:
- Database initialization
- Connection management
- Schema creation
- Transaction management
"""

import sqlite3
import os
from typing import Optional, Tuple, List, Dict, Any
from contextlib import contextmanager


class DatabaseManager:
    """Manages SQLite database operations for the banking system."""
    
    def __init__(self, db_name: str = "banking_system.db"):
        """
        Initialize database manager.
        
        Args:
            db_name (str): Name of the SQLite database file
        """
        self.db_name = db_name
        self.db_path = os.path.join(os.path.dirname(__file__), db_name)
        self.initialize_database()
    
    def initialize_database(self) -> None:
        """Create database tables if they don't exist."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Create users table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    balance DECIMAL(15, 2) DEFAULT 0.00,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Create transactions table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS transactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    transaction_type TEXT NOT NULL CHECK (transaction_type IN ('DEPOSIT', 'WITHDRAWAL')),
                    amount DECIMAL(15, 2) NOT NULL CHECK (amount > 0),
                    balance_after DECIMAL(15, 2) NOT NULL,
                    description TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            """)
            
            # Create indexes for better performance
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_users_username ON users(username)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_transactions_user_id ON transactions(user_id)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_transactions_created_at ON transactions(created_at)")
            
            conn.commit()
    
    @contextmanager
    def get_connection(self):
        """
        Context manager for database connections.
        
        Yields:
            sqlite3.Connection: Database connection object
        """
        conn = None
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row  # Enable dictionary-like access
            # Enable foreign key constraints
            conn.execute("PRAGMA foreign_keys = ON")
            yield conn
        except sqlite3.Error as e:
            if conn:
                conn.rollback()
            raise e
        finally:
            if conn:
                conn.close()
    
    def execute_query(self, query: str, params: Tuple = (), fetch_one: bool = False, 
                      fetch_all: bool = False, commit: bool = False) -> Optional[Any]:
        """
        Execute a database query with parameters.
        
        Args:
            query (str): SQL query to execute
            params (Tuple): Query parameters
            fetch_one (bool): Whether to fetch one result
            fetch_all (bool): Whether to fetch all results
            commit (bool): Whether to commit the transaction
            
        Returns:
            Query result if fetch_one or fetch_all is True, else None
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            
            if commit:
                conn.commit()
            
            if fetch_one:
                return cursor.fetchone()
            elif fetch_all:
                return cursor.fetchall()
            
            return cursor.lastrowid
    
    def user_exists(self, username: str) -> bool:
        """
        Check if a user exists in the database.
        
        Args:
            username (str): Username to check
            
        Returns:
            bool: True if user exists, False otherwise
        """
        result = self.execute_query(
            "SELECT id FROM users WHERE username = ?",
            (username,),
            fetch_one=True
        )
        return result is not None
    
    def create_user(self, username: str, password_hash: str, initial_balance: float) -> int:
        """
        Create a new user account.
        
        Args:
            username (str): Username
            password_hash (str): Hashed password
            initial_balance (float): Initial deposit amount
            
        Returns:
            int: ID of the newly created user
            
        Raises:
            sqlite3.IntegrityError: If username already exists
        """
        return self.execute_query(
            "INSERT INTO users (username, password_hash, balance) VALUES (?, ?, ?)",
            (username, password_hash, initial_balance),
            commit=True
        )
    
    def get_user(self, username: str) -> Optional[Dict[str, Any]]:
        """
        Get user information by username.
        
        Args:
            username (str): Username
            
        Returns:
            dict: User information or None if not found
        """
        result = self.execute_query(
            "SELECT id, username, password_hash, balance FROM users WHERE username = ?",
            (username,),
            fetch_one=True
        )
        return dict(result) if result else None
    
    def update_balance(self, user_id: int, new_balance: float) -> bool:
        """
        Update user account balance.
        
        Args:
            user_id (int): User ID
            new_balance (float): New balance amount
            
        Returns:
            bool: True if update successful, False otherwise
        """
        self.execute_query(
            "UPDATE users SET balance = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
            (new_balance, user_id),
            commit=True
        )
        return True
    
    def create_transaction(self, user_id: int, transaction_type: str, amount: float, 
                          balance_after: float, description: str = None) -> int:
        """
        Create a transaction record.
        
        Args:
            user_id (int): User ID
            transaction_type (str): Type of transaction ('DEPOSIT' or 'WITHDRAWAL')
            amount (float): Transaction amount
            balance_after (float): Balance after transaction
            description (str): Transaction description
            
        Returns:
            int: ID of the newly created transaction
        """
        return self.execute_query(
            """INSERT INTO transactions 
               (user_id, transaction_type, amount, balance_after, description) 
               VALUES (?, ?, ?, ?, ?)""",
            (user_id, transaction_type, amount, balance_after, description),
            commit=True
        )
    
    def get_transaction_history(self, user_id: int, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Get transaction history for a user.
        
        Args:
            user_id (int): User ID
            limit (int): Maximum number of transactions to retrieve
            
        Returns:
            list: List of transaction dictionaries
        """
        results = self.execute_query(
            """SELECT transaction_type, amount, balance_after, description, created_at 
               FROM transactions 
               WHERE user_id = ? 
               ORDER BY created_at DESC 
               LIMIT ?""",
            (user_id, limit),
            fetch_all=True
        )
        return [dict(result) for result in results] if results else []
    
    def get_user_balance(self, user_id: int) -> Optional[float]:
        """
        Get current balance for a user.
        
        Args:
            user_id (int): User ID
            
        Returns:
            float: Current balance or None if user not found
        """
        result = self.execute_query(
            "SELECT balance FROM users WHERE id = ?",
            (user_id,),
            fetch_one=True
        )
        return float(result['balance']) if result else None


# Global database instance
db_manager = DatabaseManager()
