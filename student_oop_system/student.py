"""
Student class for the Student Management System.

This module contains the Student class which represents a single student
with their personal information and academic details.
"""

from typing import Union


class Student:
    """
    Represents a student with personal information and academic details.
    
    Attributes:
        _name (str): The student's full name
        _roll_number (int): Unique roll number for identification
        _marks (float): Academic marks (0-100)
    """
    
    def __init__(self, name: str, roll_number: int, marks: float) -> None:
        """Initialize a Student object."""
        self._validate_student_data(name, roll_number, marks)
        self._name = name.strip()
        self._roll_number = roll_number
        self._marks = marks
    
    @property
    def name(self) -> str:
        """Get the student's name."""
        return self._name
    
    @property
    def roll_number(self) -> int:
        """Get the student's roll number."""
        return self._roll_number
    
    @property
    def marks(self) -> float:
        """Get the student's marks."""
        return self._marks
    
    @marks.setter
    def marks(self, value: float) -> None:
        """Set the student's marks with validation."""
        if not isinstance(value, (int, float)):
            raise TypeError("Marks must be a number")
        if not 0 <= value <= 100:
            raise ValueError("Marks must be between 0 and 100")
        self._marks = float(value)
    
    def _validate_student_data(self, name: str, roll_number: int, marks: float) -> None:
        """Validate student data during initialization."""
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Name must be a non-empty string")
        if not isinstance(roll_number, int):
            raise TypeError("Roll number must be an integer")
        if roll_number <= 0:
            raise ValueError("Roll number must be a positive integer")
        if not isinstance(marks, (int, float)):
            raise TypeError("Marks must be a number")
        if not 0 <= marks <= 100:
            raise ValueError("Marks must be between 0 and 100")
    
    def calculate_grade(self) -> str:
        """Calculate grade based on marks."""
        if self._marks >= 90:
            return "A+"
        elif self._marks >= 80:
            return "A"
        elif self._marks >= 70:
            return "B"
        elif self._marks >= 60:
            return "C"
        elif self._marks >= 50:
            return "D"
        else:
            return "F"
    
    def display_info(self) -> str:
        """Get formatted student information."""
        grade = self.calculate_grade()
        return (f"Roll Number: {self._roll_number}\n"
                f"Name: {self._name}\n"
                f"Marks: {self._marks:.1f}\n"
                f"Grade: {grade}")
    
    def __str__(self) -> str:
        """String representation of the student."""
        return f"Student({self._roll_number}, {self._name}, {self._marks:.1f})"
    
    def __eq__(self, other) -> bool:
        """Check if two students are equal based on roll number."""
        if not isinstance(other, Student):
            return False
        return self._roll_number == other._roll_number
    
    def __hash__(self) -> int:
        """Hash function based on roll number."""
        return hash(self._roll_number)
