"""
Main CLI application for Student Management System.

This module provides the command-line interface for interacting with
the Student Management System. It handles user input, validation,
and displays results in a user-friendly format.
"""

import sys
from typing import Optional
from manager import StudentManager


class StudentManagementCLI:
    """Command-line interface for the Student Management System."""
    
    def __init__(self) -> None:
        """Initialize the CLI."""
        self.manager = StudentManager()
    
    def display_header(self) -> None:
        """Display the application header."""
        print("\n" + "="*60)
        print(" "*20 + "STUDENT MANAGEMENT SYSTEM")
        print("="*60)
    
    def display_menu(self) -> None:
        """Display the main menu options."""
        print("\nMAIN MENU:")
        print("1. Add Student")
        print("2. View All Students")
        print("3. Search Student by Roll Number")
        print("4. Update Student Marks")
        print("5. Delete Student")
        print("6. View Class Statistics")
        print("7. Search Students by Name")
        print("8. View Students by Grade")
        print("9. Exit")
        print("-"*60)
    
    def get_valid_input(self, prompt: str, input_type: type, 
                       validation_func=None, error_message: str = None) -> any:
        """Get and validate user input."""
        while True:
            try:
                user_input = input(prompt).strip()
                if input_type == int:
                    value = int(user_input)
                elif input_type == float:
                    value = float(user_input)
                else:
                    value = user_input
                if validation_func and not validation_func(value):
                    if error_message:
                        print(f"Error: {error_message}")
                    else:
                        print("Error: Invalid input")
                    continue
                return value
            except ValueError:
                print(f"Error: Please enter a valid {input_type.__name__}")
    
    def validate_name(self, name: str) -> bool:
        """Validate student name."""
        return bool(name.strip())
    
    def validate_roll_number(self, roll_num: int) -> bool:
        """Validate roll number."""
        return roll_num > 0
    
    def validate_marks(self, marks: float) -> bool:
        """Validate marks."""
        return 0 <= marks <= 100
    
    def add_student(self) -> None:
        """Handle adding a new student."""
        print("\n--- ADD NEW STUDENT ---")
        
        name = self.get_valid_input(
            "Enter student name: ",
            str,
            self.validate_name,
            "Name cannot be empty"
        )
        
        roll_number = self.get_valid_input(
            "Enter roll number: ",
            int,
            lambda x: self.validate_roll_number(x) and not self.manager.is_roll_number_exists(x),
            "Roll number must be positive and unique"
        )
        
        marks = self.get_valid_input(
            "Enter marks (0-100): ",
            float,
            self.validate_marks,
            "Marks must be between 0 and 100"
        )
        
        try:
            if self.manager.add_student(name, roll_number, marks):
                print(f"\n✓ Student '{name}' added successfully!")
            else:
                print("\n✗ Failed to add student. Roll number might already exist.")
        except ValueError as e:
            print(f"\n✗ Error: {e}")
    
    def view_all_students(self) -> None:
        """Display all students."""
        print("\n--- ALL STUDENTS ---")
        
        if self.manager.is_empty():
            print("No students found in the system.")
            return
        
        students = self.manager.get_all_students()
        print(f"\nTotal Students: {len(students)}")
        print("-"*60)
        
        for i, student in enumerate(students, 1):
            print(f"\nStudent #{i}:")
            print(student.display_info())
            print("-"*40)
    
    def search_student_by_roll(self) -> None:
        """Search for a student by roll number."""
        print("\n--- SEARCH STUDENT BY ROLL NUMBER ---")
        
        roll_number = self.get_valid_input(
            "Enter roll number to search: ",
            int,
            self.validate_roll_number,
            "Roll number must be positive"
        )
        
        student = self.manager.get_student(roll_number)
        
        if student:
            print(f"\n✓ Student found:")
            print("-"*40)
            print(student.display_info())
        else:
            print(f"\n✗ No student found with roll number: {roll_number}")
    
    def update_student_marks(self) -> None:
        """Update a student's marks."""
        print("\n--- UPDATE STUDENT MARKS ---")
        
        roll_number = self.get_valid_input(
            "Enter roll number: ",
            int,
            self.validate_roll_number,
            "Roll number must be positive"
        )
        
        student = self.manager.get_student(roll_number)
        
        if not student:
            print(f"\n✗ No student found with roll number: {roll_number}")
            return
        
        print(f"\nCurrent marks for {student.name}: {student.marks:.1f}")
        
        new_marks = self.get_valid_input(
            "Enter new marks (0-100): ",
            float,
            self.validate_marks,
            "Marks must be between 0 and 100"
        )
        
        try:
            if self.manager.update_student_marks(roll_number, new_marks):
                print(f"\n✓ Marks updated successfully!")
                print(f"New grade: {student.calculate_grade()}")
            else:
                print("\n✗ Failed to update marks.")
        except ValueError as e:
            print(f"\n✗ Error: {e}")
    
    def delete_student(self) -> None:
        """Delete a student."""
        print("\n--- DELETE STUDENT ---")
        
        roll_number = self.get_valid_input(
            "Enter roll number to delete: ",
            int,
            self.validate_roll_number,
            "Roll number must be positive"
        )
        
        student = self.manager.get_student(roll_number)
        
        if not student:
            print(f"\n✗ No student found with roll number: {roll_number}")
            return
        
        print(f"\nStudent to delete: {student.name} (Roll: {roll_number})")
        
        confirm = input("Are you sure you want to delete this student? (y/N): ").strip().lower()
        
        if confirm == 'y':
            if self.manager.delete_student(roll_number):
                print(f"\n✓ Student '{student.name}' deleted successfully!")
            else:
                print("\n✗ Failed to delete student.")
        else:
            print("\nDeletion cancelled.")
    
    def view_class_statistics(self) -> None:
        """Display class statistics."""
        print("\n--- CLASS STATISTICS ---")
        
        stats = self.manager.get_class_statistics()
        
        if stats['total_students'] == 0:
            print("No students found in the system.")
            return
        
        print(f"\nTotal Students: {stats['total_students']}")
        print(f"Average Marks: {stats['average_marks']:.2f}")
        print(f"Highest Marks: {stats['highest_marks']:.1f}")
        print(f"Lowest Marks: {stats['lowest_marks']:.1f}")
        
        print("\nGrade Distribution:")
        print("-"*30)
        for grade, count in sorted(stats['grade_distribution'].items()):
            percentage = (count / stats['total_students']) * 100
            print(f"{grade:>3}: {count:>3} students ({percentage:>5.1f}%)")
    
    def search_students_by_name(self) -> None:
        """Search students by name."""
        print("\n--- SEARCH STUDENTS BY NAME ---")
        
        name = self.get_valid_input(
            "Enter name or part of name to search: ",
            str,
            self.validate_name,
            "Search term cannot be empty"
        )
        
        students = self.manager.search_students_by_name(name)
        
        if not students:
            print(f"\nNo students found matching '{name}'")
            return
        
        print(f"\nFound {len(students)} matching students:")
        print("-"*60)
        
        for i, student in enumerate(students, 1):
            print(f"\nStudent #{i}:")
            print(student.display_info())
            print("-"*40)
    
    def view_students_by_grade(self) -> None:
        """View students filtered by grade."""
        print("\n--- VIEW STUDENTS BY GRADE ---")
        
        valid_grades = ['A+', 'A', 'B', 'C', 'D', 'F']
        grade_prompt = "Enter grade (A+, A, B, C, D, F): "
        
        def validate_grade(grade):
            return grade.upper() in valid_grades
        
        grade = self.get_valid_input(
            grade_prompt,
            str,
            validate_grade,
            "Invalid grade. Please enter A+, A, B, C, D, or F"
        ).upper()
        
        students = self.manager.get_students_by_grade(grade)
        
        if not students:
            print(f"\nNo students found with grade '{grade}'")
            return
        
        print(f"\nStudents with grade '{grade}' ({len(students)} total):")
        print("-"*60)
        
        for i, student in enumerate(students, 1):
            print(f"\nStudent #{i}:")
            print(student.display_info())
            print("-"*40)
    
    def run(self) -> None:
        """Run the main application loop."""
        while True:
            try:
                self.display_header()
                self.display_menu()
                
                choice = self.get_valid_input(
                    "Enter your choice (1-9): ",
                    int,
                    lambda x: 1 <= x <= 9,
                    "Please enter a number between 1 and 9"
                )
                
                if choice == 1:
                    self.add_student()
                elif choice == 2:
                    self.view_all_students()
                elif choice == 3:
                    self.search_student_by_roll()
                elif choice == 4:
                    self.update_student_marks()
                elif choice == 5:
                    self.delete_student()
                elif choice == 6:
                    self.view_class_statistics()
                elif choice == 7:
                    self.search_students_by_name()
                elif choice == 8:
                    self.view_students_by_grade()
                elif choice == 9:
                    print("\nThank you for using Student Management System!")
                    print("Goodbye!")
                    break
                
                input("\nPress Enter to continue...")
                
            except KeyboardInterrupt:
                print("\n\nProgram interrupted by user. Goodbye!")
                sys.exit(0)
            except Exception as e:
                print(f"\nAn unexpected error occurred: {e}")
                input("Press Enter to continue...")


def main() -> None:
    """Main entry point of the application."""
    cli = StudentManagementCLI()
    cli.run()


if __name__ == "__main__":
    main()
