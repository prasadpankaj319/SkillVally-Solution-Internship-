"""
CLI Calculator - Main Application

This module contains the main CLI interface for the calculator application.
It handles user interaction, input processing, and program flow.
"""

import sys
from calculator import Calculator


class CalculatorApp:
    """
    Main application class for the CLI Calculator.
    """
    
    def __init__(self):
        """Initialize the calculator application."""
        self.calculator = Calculator()
        self.running = True
    
    def display_welcome(self):
        """Display welcome message and instructions."""
        print("=" * 50)
        print("Welcome to CLI Calculator!")
        print("=" * 50)
        print("Instructions:")
        print("- Enter calculations in format: <number> <operator> <number>")
        print("- Supported operators: +, -, *, /")
        print("- You can also use: add, subtract, multiply, divide")
        print("- Type 'quit', 'exit', or 'q' to exit the program")
        print("- Type 'help' or 'h' for instructions")
        print("- Type 'clear' to clear the screen")
        print("=" * 50)
        print()
    
    def display_help(self):
        """Display help information."""
        print("\n" + "=" * 30)
        print("CALCULATOR HELP")
        print("=" * 30)
        print("Supported formats:")
        print("  5 + 3")
        print("  10.5 - 2.3")
        print("  4 * 7")
        print("  15 / 3")
        print("  8 add 2")
        print("  9 subtract 4")
        print("  6 multiply 3")
        print("  12 divide 4")
        print("\nCommands:")
        print("  help, h     - Show this help")
        print("  clear       - Clear screen")
        print("  quit, exit, q - Exit calculator")
        print("=" * 30)
        print()
    
    def clear_screen(self):
        """Clear the terminal screen."""
        import os
        os.system('cls' if os.name == 'nt' else 'clear')
        self.display_welcome()
    
    def format_result(self, result: float) -> str:
        """
        Format the result for display.
        
        Args:
            result (float): Calculation result
            
        Returns:
            str: Formatted result string
        """
        # Remove trailing .0 for whole numbers
        if result == int(result):
            return str(int(result))
        else:
            # Round to 6 decimal places to avoid floating point artifacts
            return f"{result:.6f}".rstrip('0').rstrip('.')
    
    def process_calculation(self, user_input: str):
        """
        Process user calculation input.
        
        Args:
            user_input (str): User input string
        """
        try:
            # Parse input
            parsed = self.calculator.parse_input(user_input)
            
            if parsed is None:
                print("❌ Invalid input format!")
                print("   Please use: <number> <operator> <number>")
                print("   Example: 5 + 3 or 10 divide 2")
                return
            
            num1, num2, operator = parsed
            
            # Perform calculation
            try:
                result = self.calculator.calculate(num1, num2, operator)
                
                # Format and display result
                formatted_result = self.format_result(result)
                print(f"✅ {num1} {operator} {num2} = {formatted_result}")
                
            except ZeroDivisionError:
                print("❌ Error: Cannot divide by zero!")
                
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
    
    def handle_command(self, user_input: str) -> bool:
        """
        Handle special commands.
        
        Args:
            user_input (str): User input
            
        Returns:
            bool: True if command was handled, False otherwise
        """
        command = user_input.lower().strip()
        
        if command in ['quit', 'exit', 'q']:
            print("\nThank you for using CLI Calculator! Goodbye! 👋")
            self.running = False
            return True
        
        elif command in ['help', 'h']:
            self.display_help()
            return True
        
        elif command == 'clear':
            self.clear_screen()
            return True
        
        return False
    
    def run(self):
        """Run the main application loop."""
        self.display_welcome()
        
        while self.running:
            try:
                # Get user input
                user_input = input("🧮 Enter calculation (or command): ").strip()
                
                # Skip empty input
                if not user_input:
                    continue
                
                # Handle commands first
                if self.handle_command(user_input):
                    continue
                
                # Process calculation
                self.process_calculation(user_input)
                
            except KeyboardInterrupt:
                print("\n\n⚠️  Program interrupted by user.")
                choice = input("Do you want to exit? (y/n): ").lower().strip()
                if choice in ['y', 'yes']:
                    print("\nThank you for using CLI Calculator! Goodbye! 👋")
                    break
                else:
                    print("Continuing...")
                    continue
            
            except EOFError:
                print("\n\nThank you for using CLI Calculator! Goodbye! 👋")
                break
            
            except Exception as e:
                print(f"❌ Unexpected error: {e}")
                print("Please try again.")


def main():
    """Main entry point of the application."""
    try:
        app = CalculatorApp()
        app.run()
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
