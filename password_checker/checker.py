"""
Password Strength Checker Module

This module contains the logic for calculating password strength
based on various factors like length, character variety, and complexity.
"""

import re
from typing import Dict, Tuple
from validator import PasswordValidator


class PasswordStrengthChecker:
    """
    A class to calculate and categorize password strength.
    
    This class evaluates passwords based on:
    - Length score
    - Character variety score
    - Complexity score
    - Overall strength rating (Weak/Medium/Strong)
    """
    
    def __init__(self):
        """Initialize the PasswordStrengthChecker."""
        self.validator = PasswordValidator()
        
        # Scoring weights for different factors
        self.length_weight = 0.3
        self.variety_weight = 0.4
        self.complexity_weight = 0.3
        
        # Regex patterns for additional complexity checks
        self.repeating_chars_pattern = re.compile(r'(.)\1{2,}')  # 3+ repeating chars
        self.sequential_chars_pattern = re.compile(r'(?:abc|bcd|cde|def|efg|fgh|ghi|hij|ijk|jkl|klm|lmn|mno|nop|opq|pqr|qrs|rst|stu|tuv|uvw|vwx|wxy|xyz|012|123|234|345|456|567|678|789)', re.IGNORECASE)
    
    def calculate_length_score(self, password: str) -> float:
        """
        Calculate score based on password length.
        
        Args:
            password (str): Password to evaluate
            
        Returns:
            float: Length score (0-1)
        """
        length = len(password)
        
        if length < 8:
            return 0.0
        elif length <= 10:
            return 0.3
        elif length <= 12:
            return 0.6
        elif length <= 16:
            return 0.8
        else:
            return 1.0
    
    def calculate_variety_score(self, password: str) -> float:
        """
        Calculate score based on character variety.
        
        Args:
            password (str): Password to evaluate
            
        Returns:
            float: Variety score (0-1)
        """
        variety_count = 0
        
        if self.validator.validate_uppercase(password):
            variety_count += 1
        if self.validator.validate_lowercase(password):
            variety_count += 1
        if self.validator.validate_digit(password):
            variety_count += 1
        if self.validator.validate_special_char(password):
            variety_count += 1
        
        return variety_count / 4.0
    
    def calculate_complexity_score(self, password: str) -> float:
        """
        Calculate score based on password complexity factors.
        
        Args:
            password (str): Password to evaluate
            
        Returns:
            float: Complexity score (0-1)
        """
        score = 1.0
        
        # Penalize repeating characters
        if self.repeating_chars_pattern.search(password):
            score -= 0.3
        
        # Penalize sequential characters
        if self.sequential_chars_pattern.search(password):
            score -= 0.2
        
        # Bonus for mixed case
        if self.validator.validate_uppercase(password) and self.validator.validate_lowercase(password):
            score += 0.1
        
        # Bonus for numbers and special chars
        if self.validator.validate_digit(password) and self.validator.validate_special_char(password):
            score += 0.1
        
        return max(0.0, min(1.0, score))
    
    def calculate_overall_score(self, password: str) -> float:
        """
        Calculate overall password strength score.
        
        Args:
            password (str): Password to evaluate
            
        Returns:
            float: Overall score (0-1)
        """
        length_score = self.calculate_length_score(password)
        variety_score = self.calculate_variety_score(password)
        complexity_score = self.calculate_complexity_score(password)
        
        overall_score = (
            length_score * self.length_weight +
            variety_score * self.variety_weight +
            complexity_score * self.complexity_weight
        )
        
        return round(overall_score, 2)
    
    def get_strength_category(self, score: float) -> str:
        """
        Categorize password strength based on score.
        
        Args:
            score (float): Overall strength score (0-1)
            
        Returns:
            str: Strength category (Weak/Medium/Strong)
        """
        if score < 0.4:
            return "Weak"
        elif score < 0.7:
            return "Medium"
        else:
            return "Strong"
    
    def get_strength_details(self, password: str) -> Dict[str, any]:
        """
        Get detailed strength analysis for a password.
        
        Args:
            password (str): Password to analyze
            
        Returns:
            Dict[str, any]: Detailed strength analysis
        """
        length_score = self.calculate_length_score(password)
        variety_score = self.calculate_variety_score(password)
        complexity_score = self.calculate_complexity_score(password)
        overall_score = self.calculate_overall_score(password)
        category = self.get_strength_category(overall_score)
        
        return {
            'length_score': length_score,
            'variety_score': variety_score,
            'complexity_score': complexity_score,
            'overall_score': overall_score,
            'category': category,
            'is_valid': self.validator.is_valid(password),
            'validation_errors': self.validator.get_validation_errors(password)
        }
    
    def get_strength_recommendations(self, password: str) -> list:
        """
        Get recommendations to improve password strength.
        
        Args:
            password (str): Password to analyze
            
        Returns:
            list: List of recommendations
        """
        recommendations = []
        
        if len(password) < 12:
            recommendations.append("Consider using a longer password (12+ characters)")
        
        if not self.validator.validate_uppercase(password):
            recommendations.append("Add uppercase letters")
        
        if not self.validator.validate_lowercase(password):
            recommendations.append("Add lowercase letters")
        
        if not self.validator.validate_digit(password):
            recommendations.append("Add numbers")
        
        if not self.validator.validate_special_char(password):
            recommendations.append("Add special characters")
        
        if self.repeating_chars_pattern.search(password):
            recommendations.append("Avoid repeating characters")
        
        if self.sequential_chars_pattern.search(password):
            recommendations.append("Avoid sequential characters")
        
        return recommendations
