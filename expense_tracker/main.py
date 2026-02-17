"""
Main module for Expense Tracker CLI application.
Provides command-line interface for expense management.
"""

import sys
from tracker import ExpenseTracker


def display_menu():
    """Display the main menu options."""
    print("\n" + "="*50)
    print("    EXPENSE TRACKER - PERSONAL FINANCE MANAGER")
    print("="*50)
    print("1. Add New Expense")
    print("2. View All Expenses")
    print("3. View Monthly Expenses")
    print("4. Generate Monthly Report")
    print("5. Exit")
    print("="*50)


def get_user_choice():
    """
    Get and validate user menu choice.
    
    Returns:
        int: User's choice (1-5)
    """
    while True:
        try:
            choice = input("\nEnter your choice (1-5): ").strip()
            choice_num = int(choice)
            
            if 1 <= choice_num <= 5:
                return choice_num
            else:
                print("Invalid choice. Please enter a number between 1 and 5.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")


def handle_menu_choice(choice, tracker):
    """
    Handle user's menu choice and execute corresponding action.
    
    Args:
        choice (int): User's menu choice
        tracker (ExpenseTracker): Expense tracker instance
    """
    try:
        if choice == 1:
            tracker.add_expense()
        elif choice == 2:
            tracker.view_all_expenses()
        elif choice == 3:
            tracker.view_monthly_expenses()
        elif choice == 4:
            tracker.generate_monthly_report()
        elif choice == 5:
            print("\nThank you for using Expense Tracker!")
            print("Your data has been saved. Goodbye!")
            return False  # Signal to exit the loop
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")
        print("Please try again or contact support if the issue persists.")
    
    return True  # Continue the loop


def main():
    """Main function to run the Expense Tracker application."""
    tracker = None
    
    try:
        # Initialize the expense tracker
        print("Initializing Expense Tracker...")
        tracker = ExpenseTracker()
        print("Database connected successfully!")
        
        # Main application loop
        running = True
        while running:
            display_menu()
            choice = get_user_choice()
            running = handle_menu_choice(choice, tracker)
            
            # Ask user if they want to continue (except when exiting)
            if running and choice != 5:
                input("\nPress Enter to continue...")
    
    except KeyboardInterrupt:
        print("\n\nApplication interrupted by user.")
    except Exception as e:
        print(f"\nFatal error: {e}")
        print("The application will now exit.")
        sys.exit(1)
    finally:
        # Clean up resources
        if tracker:
            tracker.close()
            print("Database connection closed.")


if __name__ == "__main__":
    main()
