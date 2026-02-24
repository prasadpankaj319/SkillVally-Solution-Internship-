"""
Authentication module for Safe Banking System.

This module handles:
- User registration
- Secure login/logout
- Password hashing and verification
- Session management
"""

import hashlib
import secrets
import re
from typing import Optional, Dict, Any
from database import db_manager


class AuthenticationError(Exception):
    """Custom exception for authentication errors."""
    pass


class AuthenticationManager:
    """Manages user authentication and session handling."""
    
    def __init__(self):
        """Initialize authentication manager."""
        self.current_user: Optional[Dict[str, Any]] = None
        self.min_password_length = 8
        self.max_username_length = 50
    
    def _hash_password(self, password: str, salt: str = None) -> tuple:
        """
        Hash password using SHA-256 with salt.
        
        Args:
            password (str): Plain text password
            salt (str): Salt for hashing (generated if not provided)
            
        Returns:
            tuple: (salt, password_hash)
        """
        if salt is None:
            salt = secrets.token_hex(32)  # Generate random salt
        
        # Combine password and salt
        salted_password = password + salt
        
        # Hash using SHA-256
        password_hash = hashlib.sha256(salted_password.encode()).hexdigest()
        
        return salt, password_hash
    
    def _verify_password(self, password: str, salt: str, stored_hash: str) -> bool:
        """
        Verify password against stored hash.
        
        Args:
            password (str): Plain text password to verify
            salt (str): Salt used in original hashing
            stored_hash (str): Stored password hash
            
        Returns:
            bool: True if password matches, False otherwise
        """
        _, computed_hash = self._hash_password(password, salt)
        return computed_hash == stored_hash
    
    def _validate_username(self, username: str) -> bool:
        """
        Validate username format.
        
        Args:
            username (str): Username to validate
            
        Returns:
            bool: True if valid, False otherwise
        """
        if not username:
            return False
        
        if len(username) > self.max_username_length:
            return False
        
        # Allow alphanumeric characters, underscores, and hyphens
        pattern = r'^[a-zA-Z0-9_-]+$'
        return bool(re.match(pattern, username))
    
    def _validate_password(self, password: str) -> tuple:
        """
        Validate password strength.
        
        Args:
            password (str): Password to validate
            
        Returns:
            tuple: (is_valid, error_message)
        """
        if not password:
            return False, "Password cannot be empty"
        
        if len(password) < self.min_password_length:
            return False, f"Password must be at least {self.min_password_length} characters long"
        
        # Check for at least one uppercase letter
        if not re.search(r'[A-Z]', password):
            return False, "Password must contain at least one uppercase letter"
        
        # Check for at least one lowercase letter
        if not re.search(r'[a-z]', password):
            return False, "Password must contain at least one lowercase letter"
        
        # Check for at least one digit
        if not re.search(r'\d', password):
            return False, "Password must contain at least one digit"
        
        return True, ""
    
    def register_user(self, username: str, password: str, initial_deposit: float) -> Dict[str, Any]:
        """
        Register a new user account.
        
        Args:
            username (str): Username
            password (str): Plain text password
            initial_deposit (float): Initial deposit amount
            
        Returns:
            dict: Registration result with success status and message
            
        Raises:
            AuthenticationError: If registration fails
        """
        try:
            # Validate username
            if not self._validate_username(username):
                raise AuthenticationError("Invalid username. Use only letters, numbers, underscores, and hyphens.")
            
            # Check if username already exists
            if db_manager.user_exists(username):
                raise AuthenticationError("Username already exists. Please choose a different username.")
            
            # Validate password
            is_valid, error_msg = self._validate_password(password)
            if not is_valid:
                raise AuthenticationError(error_msg)
            
            # Validate initial deposit
            if initial_deposit < 0:
                raise AuthenticationError("Initial deposit cannot be negative.")
            
            if initial_deposit > 1000000:  # Reasonable upper limit
                raise AuthenticationError("Initial deposit amount too large. Maximum allowed: $1,000,000")
            
            # Hash password
            salt, password_hash = self._hash_password(password)
            
            # Store salt and hash together (format: salt:hash)
            full_password_hash = f"{salt}:{password_hash}"
            
            # Create user in database
            user_id = db_manager.create_user(username, full_password_hash, initial_deposit)
            
            # Create initial deposit transaction record
            if initial_deposit > 0:
                db_manager.create_transaction(
                    user_id=user_id,
                    transaction_type="DEPOSIT",
                    amount=initial_deposit,
                    balance_after=initial_deposit,
                    description="Initial deposit"
                )
            
            return {
                "success": True,
                "message": "User registered successfully!",
                "user_id": user_id
            }
            
        except AuthenticationError as e:
            return {
                "success": False,
                "message": str(e)
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Registration failed: {str(e)}"
            }
    
    def login(self, username: str, password: str) -> Dict[str, Any]:
        """
        Authenticate user login.
        
        Args:
            username (str): Username
            password (str): Plain text password
            
        Returns:
            dict: Login result with success status and message
        """
        try:
            # Validate input
            if not username or not password:
                raise AuthenticationError("Username and password are required.")
            
            # Get user from database
            user = db_manager.get_user(username)
            if not user:
                raise AuthenticationError("Invalid username or password.")
            
            # Extract salt and hash from stored password
            try:
                stored_salt, stored_hash = user['password_hash'].split(':', 1)
            except ValueError:
                raise AuthenticationError("Invalid password format in database.")
            
            # Verify password
            if not self._verify_password(password, stored_salt, stored_hash):
                raise AuthenticationError("Invalid username or password.")
            
            # Set current user session
            self.current_user = {
                "id": user['id'],
                "username": user['username'],
                "balance": float(user['balance'])
            }
            
            return {
                "success": True,
                "message": f"Welcome back, {username}!",
                "user": self.current_user
            }
            
        except AuthenticationError as e:
            return {
                "success": False,
                "message": str(e)
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Login failed: {str(e)}"
            }
    
    def logout(self) -> Dict[str, Any]:
        """
        Logout current user.
        
        Returns:
            dict: Logout result
        """
        username = self.current_user['username'] if self.current_user else "User"
        self.current_user = None
        
        return {
            "success": True,
            "message": f"Goodbye, {username}!"
        }
    
    def is_logged_in(self) -> bool:
        """
        Check if user is currently logged in.
        
        Returns:
            bool: True if user is logged in, False otherwise
        """
        return self.current_user is not None
    
    def get_current_user(self) -> Optional[Dict[str, Any]]:
        """
        Get current logged-in user information.
        
        Returns:
            dict: Current user information or None if not logged in
        """
        return self.current_user
    
    def require_login(self) -> bool:
        """
        Check if login is required for current operation.
        
        Returns:
            bool: True if user is logged in, False otherwise
        """
        if not self.is_logged_in():
            print("Error: You must be logged in to perform this operation.")
            return False
        return True


# Global authentication instance
auth_manager = AuthenticationManager()
