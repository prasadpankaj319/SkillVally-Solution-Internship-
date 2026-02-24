"""
Banking operations module for Safe Banking System.

This module handles:
- Deposit operations
- Withdrawal operations
- Balance inquiries
- Transaction history
- Transaction safety and validation
"""

from typing import Dict, Any, List
from decimal import Decimal, InvalidOperation
from database import db_manager
from auth import auth_manager


class BankingError(Exception):
    """Custom exception for banking operations errors."""
    pass


class BankingManager:
    """Manages banking operations and transaction logic."""
    
    def __init__(self):
        """Initialize banking manager."""
        self.max_transaction_amount = 1000000  # Maximum transaction limit
        self.min_transaction_amount = 0.01    # Minimum transaction amount
    
    def _validate_amount(self, amount: float) -> tuple:
        """
        Validate transaction amount.
        
        Args:
            amount (float): Amount to validate
            
        Returns:
            tuple: (is_valid, error_message)
        """
        try:
            # Convert to Decimal for precise financial calculations
            decimal_amount = Decimal(str(amount))
            
            if decimal_amount <= Decimal('0'):
                return False, "Amount must be greater than zero."
            
            if decimal_amount < Decimal(str(self.min_transaction_amount)):
                return False, f"Minimum transaction amount is ${self.min_transaction_amount:.2f}"
            
            if decimal_amount > Decimal(str(self.max_transaction_amount)):
                return False, f"Maximum transaction amount is ${self.max_transaction_amount:,.2f}"
            
            # Check for reasonable decimal places (max 2 for currency)
            if decimal_amount.as_tuple().exponent < -2:
                return False, "Amount cannot have more than 2 decimal places."
            
            return True, ""
            
        except (InvalidOperation, ValueError):
            return False, "Invalid amount format."
    
    def _get_current_balance(self, user_id: int) -> Decimal:
        """
        Get current balance for a user.
        
        Args:
            user_id (int): User ID
            
        Returns:
            Decimal: Current balance
            
        Raises:
            BankingError: If user not found or balance retrieval fails
        """
        balance = db_manager.get_user_balance(user_id)
        if balance is None:
            raise BankingError("User account not found.")
        
        return Decimal(str(balance))
    
    def deposit(self, amount: float, description: str = None) -> Dict[str, Any]:
        """
        Deposit money into user's account.
        
        Args:
            amount (float): Amount to deposit
            description (str): Transaction description
            
        Returns:
            dict: Deposit result with success status and details
        """
        try:
            # Check if user is logged in
            if not auth_manager.require_login():
                return {
                    "success": False,
                    "message": "You must be logged in to make a deposit."
                }
            
            # Validate amount
            is_valid, error_msg = self._validate_amount(amount)
            if not is_valid:
                return {
                    "success": False,
                    "message": error_msg
                }
            
            decimal_amount = Decimal(str(amount))
            user_id = auth_manager.get_current_user()['id']
            
            # Get current balance
            current_balance = self._get_current_balance(user_id)
            
            # Calculate new balance
            new_balance = current_balance + decimal_amount
            
            # Update balance in database
            db_manager.update_balance(user_id, float(new_balance))
            
            # Create transaction record
            transaction_id = db_manager.create_transaction(
                user_id=user_id,
                transaction_type="DEPOSIT",
                amount=float(decimal_amount),
                balance_after=float(new_balance),
                description=description or f"Deposit of ${decimal_amount:.2f}"
            )
            
            # Update current user session balance
            auth_manager.current_user['balance'] = float(new_balance)
            
            return {
                "success": True,
                "message": f"Successfully deposited ${decimal_amount:.2f}",
                "transaction_id": transaction_id,
                "new_balance": float(new_balance)
            }
            
        except BankingError as e:
            return {
                "success": False,
                "message": str(e)
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Deposit failed: {str(e)}"
            }
    
    def withdraw(self, amount: float, description: str = None) -> Dict[str, Any]:
        """
        Withdraw money from user's account.
        
        Args:
            amount (float): Amount to withdraw
            description (str): Transaction description
            
        Returns:
            dict: Withdrawal result with success status and details
        """
        try:
            # Check if user is logged in
            if not auth_manager.require_login():
                return {
                    "success": False,
                    "message": "You must be logged in to make a withdrawal."
                }
            
            # Validate amount
            is_valid, error_msg = self._validate_amount(amount)
            if not is_valid:
                return {
                    "success": False,
                    "message": error_msg
                }
            
            decimal_amount = Decimal(str(amount))
            user_id = auth_manager.get_current_user()['id']
            
            # Get current balance
            current_balance = self._get_current_balance(user_id)
            
            # Check for sufficient funds
            if decimal_amount > current_balance:
                return {
                    "success": False,
                    "message": f"Insufficient funds. Available balance: ${current_balance:.2f}"
                }
            
            # Calculate new balance
            new_balance = current_balance - decimal_amount
            
            # Ensure balance doesn't go negative (additional safety check)
            if new_balance < Decimal('0'):
                raise BankingError("Transaction would result in negative balance.")
            
            # Update balance in database
            db_manager.update_balance(user_id, float(new_balance))
            
            # Create transaction record
            transaction_id = db_manager.create_transaction(
                user_id=user_id,
                transaction_type="WITHDRAWAL",
                amount=float(decimal_amount),
                balance_after=float(new_balance),
                description=description or f"Withdrawal of ${decimal_amount:.2f}"
            )
            
            # Update current user session balance
            auth_manager.current_user['balance'] = float(new_balance)
            
            return {
                "success": True,
                "message": f"Successfully withdrew ${decimal_amount:.2f}",
                "transaction_id": transaction_id,
                "new_balance": float(new_balance)
            }
            
        except BankingError as e:
            return {
                "success": False,
                "message": str(e)
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Withdrawal failed: {str(e)}"
            }
    
    def check_balance(self) -> Dict[str, Any]:
        """
        Check current account balance.
        
        Returns:
            dict: Balance information
        """
        try:
            # Check if user is logged in
            if not auth_manager.require_login():
                return {
                    "success": False,
                    "message": "You must be logged in to check your balance."
                }
            
            user_id = auth_manager.get_current_user()['id']
            current_balance = self._get_current_balance(user_id)
            
            return {
                "success": True,
                "balance": float(current_balance),
                "message": f"Your current balance is ${current_balance:.2f}"
            }
            
        except BankingError as e:
            return {
                "success": False,
                "message": str(e)
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Failed to retrieve balance: {str(e)}"
            }
    
    def get_transaction_history(self, limit: int = 50) -> Dict[str, Any]:
        """
        Get transaction history for the current user.
        
        Args:
            limit (int): Maximum number of transactions to retrieve
            
        Returns:
            dict: Transaction history
        """
        try:
            # Check if user is logged in
            if not auth_manager.require_login():
                return {
                    "success": False,
                    "message": "You must be logged in to view transaction history."
                }
            
            user_id = auth_manager.get_current_user()['id']
            transactions = db_manager.get_transaction_history(user_id, limit)
            
            if not transactions:
                return {
                    "success": True,
                    "message": "No transactions found.",
                    "transactions": []
                }
            
            # Format transactions for display
            formatted_transactions = []
            for transaction in transactions:
                formatted_transactions.append({
                    "type": transaction['transaction_type'],
                    "amount": float(transaction['amount']),
                    "balance_after": float(transaction['balance_after']),
                    "description": transaction['description'],
                    "date": transaction['created_at']
                })
            
            return {
                "success": True,
                "message": f"Found {len(formatted_transactions)} transactions.",
                "transactions": formatted_transactions
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Failed to retrieve transaction history: {str(e)}"
            }
    
    def get_account_summary(self) -> Dict[str, Any]:
        """
        Get complete account summary for the current user.
        
        Returns:
            dict: Account summary
        """
        try:
            # Check if user is logged in
            if not auth_manager.require_login():
                return {
                    "success": False,
                    "message": "You must be logged in to view account summary."
                }
            
            current_user = auth_manager.get_current_user()
            balance_result = self.check_balance()
            history_result = self.get_transaction_history(limit=10)  # Last 10 transactions
            
            if not balance_result['success']:
                return balance_result
            
            # Calculate total deposits and withdrawals
            total_deposits = 0.0
            total_withdrawals = 0.0
            
            if history_result['success'] and history_result['transactions']:
                for transaction in history_result['transactions']:
                    if transaction['type'] == 'DEPOSIT':
                        total_deposits += transaction['amount']
                    elif transaction['type'] == 'WITHDRAWAL':
                        total_withdrawals += transaction['amount']
            
            return {
                "success": True,
                "account_info": {
                    "username": current_user['username'],
                    "current_balance": balance_result['balance'],
                    "total_deposits": total_deposits,
                    "total_withdrawals": total_withdrawals,
                    "recent_transactions": history_result.get('transactions', [])
                }
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Failed to retrieve account summary: {str(e)}"
            }


# Global banking instance
banking_manager = BankingManager()
