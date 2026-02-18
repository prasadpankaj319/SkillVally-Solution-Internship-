"""
Password Strength Checker - Main CLI Application

This is the main entry point for the Password Strength Checker application.
It provides a command-line interface for users to check password strength
and get detailed feedback on their passwords.
"""

import sys
import getpass
from typing import Optional
from validator import PasswordValidator
from checker import PasswordStrengthChecker


class PasswordCheckerApp:
    """
    Main application class for the Password Strength Checker CLI.
    """
    
    def __init__(self):
        """Initialize the application."""
        self.validator = PasswordValidator()
        self.strength_checker = PasswordStrengthChecker()
    
    def display_welcome(self):
        """Display welcome message and instructions."""
        print("=" * 60)
        print("    PASSWORD STRENGTH CHECKER - Professional Edition")
        print("=" * 60)
        print("\nThis tool helps you evaluate the strength of your passwords.")
        print("Your password will not be stored or transmitted anywhere.")
        print("\nValidation Requirements:")
        print("• Minimum 8 characters")
        print("• At least 1 uppercase letter")
        print("• At least 1 lowercase letter")
        print("• At least 1 digit")
        print("• At least 1 special character")
        print("\n" + "=" * 60)
    
    def get_password_input(self) -> Optional[str]:
        """
        Get password input from user securely.
        
        Returns:
            Optional[str]: Password input or None if user wants to exit
        """
        try:
            print("\nEnter a password to check (or type 'exit' to quit):")
            password = getpass.getpass("Password: ")
            
            if password.lower() == 'exit':
                return None
            
            return password
        
        except KeyboardInterrupt:
            print("\n\nOperation cancelled by user.")
            return None
        except Exception as e:
            print(f"\nError reading input: {e}")
            return None
    
    def display_validation_results(self, password: str):
        """
        Display password validation results.
        
        Args:
            password (str): Password to display results for
        """
        print("\n" + "-" * 40)
        print("VALIDATION RESULTS")
        print("-" * 40)
        
        validation_summary = self.validator.get_validation_summary(password)
        
        print(f"✓ Length (8+ chars): {'✓' if validation_summary['length'] else '✗'}")
        print(f"✓ Uppercase letter: {'✓' if validation_summary['uppercase'] else '✗'}")
        print(f"✓ Lowercase letter: {'✓' if validation_summary['lowercase'] else '✗'}")
        print(f"✓ Digit: {'✓' if validation_summary['digit'] else '✗'}")
        print(f"✓ Special character: {'✓' if validation_summary['special_char'] else '✗'}")
        
        errors = self.validator.get_validation_errors(password)
        if errors:
            print("\n❌ Validation Errors:")
            for error in errors:
                print(f"  • {error}")
        else:
            print("\n✅ All validation requirements met!")
    
    def display_strength_results(self, password: str):
        """
        Display password strength analysis results.
        
        Args:
            password (str): Password to display results for
        """
        print("\n" + "-" * 40)
        print("STRENGTH ANALYSIS")
        print("-" * 40)
        
        details = self.strength_checker.get_strength_details(password)
        
        # Display strength category with color-coded indicators
        category = details['category']
        score = details['overall_score']
        
        if category == "Weak":
            indicator = "🔴"
        elif category == "Medium":
            indicator = "🟡"
        else:
            indicator = "🟢"
        
        print(f"Strength Rating: {indicator} {category} ({score:.0%})")
        
        # Display detailed scores
        print(f"\nDetailed Scores:")
        print(f"  • Length Score: {details['length_score']:.0%}")
        print(f"  • Variety Score: {details['variety_score']:.0%}")
        print(f"  • Complexity Score: {details['complexity_score']:.0%}")
        
        # Display recommendations
        recommendations = self.strength_checker.get_strength_recommendations(password)
        if recommendations:
            print(f"\n💡 Recommendations:")
            for rec in recommendations:
                print(f"  • {rec}")
        else:
            print(f"\n🎉 Excellent password! No improvements needed.")
    
    def display_password_info(self, password: str):
        """
        Display general password information (without revealing the password).
        
        Args:
            password (str): Password to analyze
        """
        print(f"\n" + "-" * 40)
        print("PASSWORD INFORMATION")
        print("-" * 40)
        print(f"Length: {len(password)} characters")
        
        # Character count breakdown
        char_counts = {
            'Uppercase': sum(1 for c in password if c.isupper()),
            'Lowercase': sum(1 for c in password if c.islower()),
            'Digits': sum(1 for c in password if c.isdigit()),
            'Special': sum(1 for c in password if not c.isalnum())
        }
        
        print("Character Breakdown:")
        for char_type, count in char_counts.items():
            print(f"  • {char_type}: {count}")
    
    def run_single_check(self):
        """Run a single password check."""
        password = self.get_password_input()
        
        if password is None:
            return False
        
        if not password:
            print("\n❌ Error: Empty password provided.")
            return True
        
        # Display all results
        self.display_password_info(password)
        self.display_validation_results(password)
        self.display_strength_results(password)
        
        return True
    
    def run_interactive_mode(self):
        """Run the application in interactive mode."""
        self.display_welcome()
        
        while True:
            if not self.run_single_check():
                break
            
            # Ask if user wants to continue
            try:
                print("\n" + "=" * 60)
                choice = input("Check another password? (y/n): ").lower().strip()
                
                if choice in ['n', 'no', 'exit', 'quit']:
                    print("\nThank you for using Password Strength Checker!")
                    break
                elif choice in ['y', 'yes']:
                    print("\n" + "=" * 60)
                    continue
                else:
                    print("Invalid choice. Please enter 'y' or 'n'.")
                    continue
                    
            except KeyboardInterrupt:
                print("\n\nOperation cancelled by user.")
                break
            except Exception as e:
                print(f"\nError: {e}")
                break
    
    def run(self):
        """Run the password checker application."""
        try:
            self.run_interactive_mode()
        except Exception as e:
            print(f"\nUnexpected error: {e}")
            sys.exit(1)


def main():
    """Main entry point for the application."""
    app = PasswordCheckerApp()
    app.run()


if __name__ == "__main__":
    main()
