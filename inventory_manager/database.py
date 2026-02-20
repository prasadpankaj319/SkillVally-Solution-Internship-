"""
Database module for Inventory Manager.
Handles all SQLite database operations.
"""

import sqlite3
import os
from typing import List, Tuple, Optional


class Database:
    """Database class for managing inventory data storage."""
    
    def __init__(self, db_name: str = "inventory.db"):
        """
        Initialize database connection.
        
        Args:
            db_name (str): Name of the SQLite database file
        """
        self.db_name = db_name
        self.connection = None
        self.connect()
        self.create_table()
    
    def connect(self) -> None:
        """Establish database connection."""
        try:
            self.connection = sqlite3.connect(self.db_name)
            self.connection.row_factory = sqlite3.Row  # Enable dict-like access
        except sqlite3.Error as e:
            raise Exception(f"Database connection failed: {e}")
    
    def create_table(self) -> None:
        """Create products table if it doesn't exist."""
        query = """
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            price REAL NOT NULL,
            quantity INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute(query)
            self.connection.commit()
        except sqlite3.Error as e:
            raise Exception(f"Table creation failed: {e}")
    
    def execute_query(self, query: str, params: Tuple = ()) -> sqlite3.Cursor:
        """
        Execute a parameterized query.
        
        Args:
            query (str): SQL query with placeholders
            params (Tuple): Query parameters
            
        Returns:
            sqlite3.Cursor: Query cursor
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params)
            return cursor
        except sqlite3.Error as e:
            raise Exception(f"Query execution failed: {e}")
    
    def fetch_all(self, query: str, params: Tuple = ()) -> List[sqlite3.Row]:
        """
        Fetch all results from a query.
        
        Args:
            query (str): SQL query with placeholders
            params (Tuple): Query parameters
            
        Returns:
            List[sqlite3.Row]: Query results
        """
        cursor = self.execute_query(query, params)
        return cursor.fetchall()
    
    def fetch_one(self, query: str, params: Tuple = ()) -> Optional[sqlite3.Row]:
        """
        Fetch single result from a query.
        
        Args:
            query (str): SQL query with placeholders
            params (Tuple): Query parameters
            
        Returns:
            Optional[sqlite3.Row]: Single query result or None
        """
        cursor = self.execute_query(query, params)
        return cursor.fetchone()
    
    def commit(self) -> None:
        """Commit transaction to database."""
        try:
            self.connection.commit()
        except sqlite3.Error as e:
            raise Exception(f"Commit failed: {e}")
    
    def close(self) -> None:
        """Close database connection."""
        if self.connection:
            try:
                self.connection.close()
            except sqlite3.Error as e:
                print(f"Warning: Failed to close database connection: {e}")
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
