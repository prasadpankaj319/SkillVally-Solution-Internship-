"""
Password Validator Module

This module contains the core validation logic for password checking.
It implements various validation rules using regular expressions
and provides detailed error messages for failed validations.
"""

import re
from typing import List, Dict, Tuple


class PasswordValidator:
    """
    A class to validate passwords against various security criteria.
    
    This validator checks for:
    - Minimum length requirement
    - Presence of uppercase letters
    - Presence of lowercase letters
    - Presence of digits
    - Presence of special characters
    """
    
    def __init__(self, min_length: int = 8):
        """
        Initialize the PasswordValidator.
        
        Args:
            min_length (int): Minimum required password length (default: 8)
        """
        self.min_length = min_length
        
        # Compile regex patterns for better performance
        self.uppercase_pattern = re.compile(r'[A-Z]')
        self.lowercase_pattern = re.compile(r'[a-z]')
        self.digit_pattern = re.compile(r'\d')
        self.special_char_pattern = re.compile(r'[!@#$%^&*()_+\-=\[\]{};:"\\|,.<>\/?]')
        
    def validate_length(self, password: str) -> bool:
        """
        Validate password minimum length.
        
        Args:
            password (str): Password to validate
            
        Returns:
            bool: True if password meets minimum length requirement
        """
        return len(password) >= self.min_length
    
    def validate_uppercase(self, password: str) -> bool:
        """
        Validate password contains at least one uppercase letter.
        
        Args:
            password (str): Password to validate
            
        Returns:
            bool: True if password contains uppercase letter
        """
        return bool(self.uppercase_pattern.search(password))
    
    def validate_lowercase(self, password: str) -> bool:
        """
        Validate password contains at least one lowercase letter.
        
        Args:
            password (str): Password to validate
            
        Returns:
            bool: True if password contains lowercase letter
        """
        return bool(self.lowercase_pattern.search(password))
    
    def validate_digit(self, password: str) -> bool:
        """
        Validate password contains at least one digit.
        
        Args:
            password (str): Password to validate
            
        Returns:
            bool: True if password contains digit
        """
        return bool(self.digit_pattern.search(password))
    
    def validate_special_char(self, password: str) -> bool:
        """
        Validate password contains at least one special character.
        
        Args:
            password (str): Password to validate
            
        Returns:
            bool: True if password contains special character
        """
        return bool(self.special_char_pattern.search(password))
    
    def get_validation_errors(self, password: str) -> List[str]:
        """
        Get detailed validation error messages for a password.
        
        Args:
            password (str): Password to validate
            
        Returns:
            List[str]: List of validation error messages
        """
        errors = []
        
        if not self.validate_length(password):
            errors.append(f"Password must be at least {self.min_length} characters long")
        
        if not self.validate_uppercase(password):
            errors.append("Password must contain at least one uppercase letter")
        
        if not self.validate_lowercase(password):
            errors.append("Password must contain at least one lowercase letter")
        
        if not self.validate_digit(password):
            errors.append("Password must contain at least one digit")
        
        if not self.validate_special_char(password):
            errors.append("Password must contain at least one special character")
        
        return errors
    
    def is_valid(self, password: str) -> bool:
        """
        Check if password passes all validation rules.
        
        Args:
            password (str): Password to validate
            
        Returns:
            bool: True if password passes all validations
        """
        return len(self.get_validation_errors(password)) == 0
    
    def get_validation_summary(self, password: str) -> Dict[str, bool]:
        """
        Get a summary of all validation checks.
        
        Args:
            password (str): Password to validate
            
        Returns:
            Dict[str, bool]: Dictionary with validation results for each rule
        """
        return {
            'length': self.validate_length(password),
            'uppercase': self.validate_uppercase(password),
            'lowercase': self.validate_lowercase(password),
            'digit': self.validate_digit(password),
            'special_char': self.validate_special_char(password)
        }
