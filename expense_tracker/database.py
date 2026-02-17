"""
Database module for Expense Tracker.
Handles all SQLite database operations.
"""

import sqlite3
import os
from datetime import datetime


class Database:
    """Database class for managing expense data."""
    
    def __init__(self, db_name="expenses.db"):
        """
        Initialize database connection.
        
        Args:
            db_name (str): Name of the SQLite database file
        """
        self.db_name = db_name
        self.conn = None
        self.connect()
        self.create_table()
    
    def connect(self):
        """Establish database connection."""
        try:
            self.conn = sqlite3.connect(self.db_name)
            self.conn.row_factory = sqlite3.Row  # Enable dictionary-like access
        except sqlite3.Error as e:
            print(f"Database connection error: {e}")
            raise
    
    def create_table(self):
        """Create expenses table if it doesn't exist."""
        query = """
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            description TEXT,
            date TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute(query)
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Table creation error: {e}")
            raise
    
    def add_expense(self, amount, category, description, date):
        """
        Add a new expense to the database.
        
        Args:
            amount (float): Expense amount
            category (str): Expense category
            description (str): Expense description
            date (str): Expense date in YYYY-MM-DD format
            
        Returns:
            bool: True if successful, False otherwise
        """
        query = """
        INSERT INTO expenses (amount, category, description, date)
        VALUES (?, ?, ?, ?)
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute(query, (amount, category, description, date))
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error adding expense: {e}")
            return False
    
    def get_all_expenses(self):
        """
        Retrieve all expenses from the database.
        
        Returns:
            list: List of expense records as dictionaries
        """
        query = """
        SELECT id, amount, category, description, date, created_at
        FROM expenses
        ORDER BY date DESC, created_at DESC
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute(query)
            expenses = [dict(row) for row in cursor.fetchall()]
            return expenses
        except sqlite3.Error as e:
            print(f"Error retrieving expenses: {e}")
            return []
    
    def get_monthly_report(self, year=None):
        """
        Generate monthly expense report for a given year.
        
        Args:
            year (int): Year for report (default: current year)
            
        Returns:
            list: List of monthly totals as dictionaries
        """
        if year is None:
            year = datetime.now().year
        
        query = """
        SELECT 
            strftime('%m', date) as month,
            strftime('%Y', date) as year,
            SUM(amount) as total_amount,
            COUNT(*) as expense_count
        FROM expenses
        WHERE strftime('%Y', date) = ?
        GROUP BY strftime('%m', date), strftime('%Y', date)
        ORDER BY month
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute(query, (str(year),))
            report = [dict(row) for row in cursor.fetchall()]
            return report
        except sqlite3.Error as e:
            print(f"Error generating monthly report: {e}")
            return []
    
    def get_expenses_by_month(self, year, month):
        """
        Get all expenses for a specific month and year.
        
        Args:
            year (int): Year
            month (int): Month (1-12)
            
        Returns:
            list: List of expense records for the specified month
        """
        query = """
        SELECT id, amount, category, description, date, created_at
        FROM expenses
        WHERE strftime('%Y', date) = ? AND strftime('%m', date) = ?
        ORDER BY date DESC, created_at DESC
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute(query, (str(year), f"{month:02d}"))
            expenses = [dict(row) for row in cursor.fetchall()]
            return expenses
        except sqlite3.Error as e:
            print(f"Error retrieving monthly expenses: {e}")
            return []
    
    def close(self):
        """Close database connection."""
        if self.conn:
            self.conn.close()
    
    def __del__(self):
        """Destructor to ensure connection is closed."""
        self.close()
