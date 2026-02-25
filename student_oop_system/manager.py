"""
StudentManager class for managing student records.

This module contains the StudentManager class which handles all operations
related to student record management including CRUD operations.
"""

from typing import List, Optional, Dict, Any
from student import Student


class StudentManager:
    """
    Manages a collection of student records.
    
    This class provides functionality to add, view, search, update,
    and delete student records while maintaining data integrity.
    
    Attributes:
        _students (Dict[int, Student]): Dictionary mapping roll numbers to Student objects
    """
    
    def __init__(self) -> None:
        """Initialize the StudentManager."""
        self._students: Dict[int, Student] = {}
    
    def add_student(self, name: str, roll_number: int, marks: float) -> bool:
        """Add a new student to the system."""
        if roll_number in self._students:
            return False
        try:
            student = Student(name, roll_number, marks)
            self._students[roll_number] = student
            return True
        except (ValueError, TypeError) as e:
            raise ValueError(f"Invalid student data: {e}")
    
    def get_student(self, roll_number: int) -> Optional[Student]:
        """Retrieve a student by roll number."""
        return self._students.get(roll_number)
    
    def get_all_students(self) -> List[Student]:
        """Get all students in the system."""
        return [self._students[roll_num] for roll_num in sorted(self._students.keys())]
    
    def update_student_marks(self, roll_number: int, new_marks: float) -> bool:
        """Update a student's marks."""
        student = self._students.get(roll_number)
        if not student:
            return False
        try:
            student.marks = new_marks
            return True
        except (ValueError, TypeError) as e:
            raise ValueError(f"Invalid marks: {e}")
    
    def delete_student(self, roll_number: int) -> bool:
        """Delete a student from the system."""
        if roll_number in self._students:
            del self._students[roll_number]
            return True
        return False
    
    def is_roll_number_exists(self, roll_number: int) -> bool:
        """Check if a roll number already exists."""
        return roll_number in self._students
    
    def get_student_count(self) -> int:
        """Get the total number of students."""
        return len(self._students)
    
    def is_empty(self) -> bool:
        """Check if the student collection is empty."""
        return len(self._students) == 0
    
    def get_class_statistics(self) -> Dict[str, Any]:
        """Calculate class statistics."""
        if self.is_empty():
            return {
                'total_students': 0,
                'average_marks': 0.0,
                'highest_marks': 0.0,
                'lowest_marks': 0.0,
                'grade_distribution': {}
            }
        
        all_students = self.get_all_students()
        marks_list = [student.marks for student in all_students]
        
        grade_distribution = {}
        for student in all_students:
            grade = student.calculate_grade()
            grade_distribution[grade] = grade_distribution.get(grade, 0) + 1
        
        return {
            'total_students': len(all_students),
            'average_marks': sum(marks_list) / len(marks_list),
            'highest_marks': max(marks_list),
            'lowest_marks': min(marks_list),
            'grade_distribution': grade_distribution
        }
    
    def search_students_by_name(self, name: str) -> List[Student]:
        """Search students by name (case-insensitive partial match)."""
        search_term = name.lower().strip()
        matching_students = []
        for student in self._students.values():
            if search_term in student.name.lower():
                matching_students.append(student)
        return matching_students
    
    def get_students_by_grade(self, grade: str) -> List[Student]:
        """Get all students with a specific grade."""
        matching_students = []
        for student in self._students.values():
            if student.calculate_grade() == grade.upper():
                matching_students.append(student)
        return matching_students
    
    def clear_all_students(self) -> None:
        """Remove all students from the system."""
        self._students.clear()
    
    def export_student_data(self) -> List[Dict[str, Any]]:
        """Export student data for external use."""
        export_data = []
        for student in self.get_all_students():
            export_data.append({
                'roll_number': student.roll_number,
                'name': student.name,
                'marks': student.marks,
                'grade': student.calculate_grade()
            })
        return export_data
