"""
CLI Calculator - Core Logic Module

This module contains the core calculation logic and input validation
for the CLI Calculator application.
"""

from typing import Union, Tuple


class Calculator:
    """
    A simple calculator class that performs basic arithmetic operations.
    """
    
    @staticmethod
    def add(a: float, b: float) -> float:
        """
        Add two numbers.
        
        Args:
            a (float): First number
            b (float): Second number
            
        Returns:
            float: Sum of a and b
        """
        return a + b
    
    @staticmethod
    def subtract(a: float, b: float) -> float:
        """
        Subtract second number from first number.
        
        Args:
            a (float): First number
            b (float): Second number
            
        Returns:
            float: Difference of a and b
        """
        return a - b
    
    @staticmethod
    def multiply(a: float, b: float) -> float:
        """
        Multiply two numbers.
        
        Args:
            a (float): First number
            b (float): Second number
            
        Returns:
            float: Product of a and b
        """
        return a * b
    
    @staticmethod
    def divide(a: float, b: float) -> float:
        """
        Divide first number by second number.
        
        Args:
            a (float): First number (dividend)
            b (float): Second number (divisor)
            
        Returns:
            float: Quotient of a divided by b
            
        Raises:
            ZeroDivisionError: If b is zero
        """
        if b == 0:
            raise ZeroDivisionError("Cannot divide by zero")
        return a / b
    
    @staticmethod
    def validate_number(input_str: str) -> Union[float, None]:
        """
        Validate and convert string input to a number.
        
        Args:
            input_str (str): String input to validate
            
        Returns:
            float: Validated number
            None: If input is invalid
        """
        try:
            return float(input_str)
        except ValueError:
            return None
    
    @staticmethod
    def validate_operator(operator: str) -> bool:
        """
        Validate if the operator is supported.
        
        Args:
            operator (str): Operator to validate
            
        Returns:
            bool: True if operator is valid, False otherwise
        """
        valid_operators = ['+', '-', '*', '/', 'add', 'subtract', 'multiply', 'divide']
        return operator.lower() in valid_operators
    
    @staticmethod
    def get_operation(operator: str) -> Union[callable, None]:
        """
        Get the corresponding operation function for the operator.
        
        Args:
            operator (str): Operator string
            
        Returns:
            callable: Corresponding operation function
            None: If operator is invalid
        """
        operations = {
            '+': Calculator.add,
            'add': Calculator.add,
            '-': Calculator.subtract,
            'subtract': Calculator.subtract,
            '*': Calculator.multiply,
            'multiply': Calculator.multiply,
            '/': Calculator.divide,
            'divide': Calculator.divide
        }
        return operations.get(operator.lower())
    
    @staticmethod
    def calculate(a: float, b: float, operator: str) -> Union[float, None]:
        """
        Perform calculation based on operator.
        
        Args:
            a (float): First number
            b (float): Second number
            operator (str): Operation to perform
            
        Returns:
            float: Result of calculation
            None: If operation fails
        """
        operation = Calculator.get_operation(operator)
        if operation is None:
            return None
        
        try:
            return operation(a, b)
        except ZeroDivisionError as e:
            raise e
        except Exception:
            return None
    
    @staticmethod
    def parse_input(input_str: str) -> Union[Tuple[float, float, str], None]:
        """
        Parse user input into numbers and operator.
        
        Args:
            input_str (str): User input string
            
        Returns:
            tuple: (num1, num2, operator) if valid
            None: If invalid
        """
        # Remove extra spaces and split
        parts = input_str.strip().split()
        
        if len(parts) != 3:
            return None
        
        num1_str, operator, num2_str = parts
        
        # Validate numbers
        num1 = Calculator.validate_number(num1_str)
        num2 = Calculator.validate_number(num2_str)
        
        if num1 is None or num2 is None:
            return None
        
        # Validate operator
        if not Calculator.validate_operator(operator):
            return None
        
        return (num1, num2, operator)
