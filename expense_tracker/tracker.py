"""
Expense Tracker module.
Contains business logic for expense management.
"""

from datetime import datetime
from database import Database


class ExpenseTracker:
    """Main expense tracking class."""
    
    # Common expense categories
    CATEGORIES = [
        "Food", "Transportation", "Entertainment", "Shopping",
        "Healthcare", "Education", "Bills", "Salary", "Other"
    ]
    
    def __init__(self):
        """Initialize the expense tracker with database connection."""
        self.db = Database()
    
    def validate_amount(self, amount_str):
        """
        Validate and convert amount string to float.
        
        Args:
            amount_str (str): Amount as string
            
        Returns:
            tuple: (is_valid, amount_float or None)
        """
        try:
            amount = float(amount_str)
            if amount <= 0:
                print("Amount must be greater than 0.")
                return False, None
            return True, amount
        except ValueError:
            print("Invalid amount. Please enter a valid number.")
            return False, None
    
    def validate_date(self, date_str):
        """
        Validate date string and return in YYYY-MM-DD format.
        
        Args:
            date_str (str): Date as string
            
        Returns:
            tuple: (is_valid, formatted_date or None)
        """
        try:
            # Try to parse the date
            if date_str.lower() == "today":
                return True, datetime.now().strftime("%Y-%m-%d")
            
            # Try different date formats
            formats = ["%Y-%m-%d", "%d-%m-%Y", "%m-%d-%Y"]
            for fmt in formats:
                try:
                    date_obj = datetime.strptime(date_str, fmt)
                    return True, date_obj.strftime("%Y-%m-%d")
                except ValueError:
                    continue
            
            print("Invalid date format. Use YYYY-MM-DD, DD-MM-YYYY, or 'today'.")
            return False, None
        except Exception as e:
            print(f"Date validation error: {e}")
            return False, None
    
    def get_category_input(self):
        """
        Get category input from user with suggestions.
        
        Returns:
            str: Selected category
        """
        print("\nAvailable categories:")
        for i, category in enumerate(self.CATEGORIES, 1):
            print(f"{i}. {category}")
        print("9. Other (custom category)")
        
        while True:
            try:
                choice = input("Select category (1-9): ").strip()
                choice_num = int(choice)
                
                if 1 <= choice_num <= 8:
                    return self.CATEGORIES[choice_num - 1]
                elif choice_num == 9:
                    custom_category = input("Enter custom category: ").strip()
                    if custom_category:
                        return custom_category
                    else:
                        print("Category cannot be empty.")
                else:
                    print("Invalid choice. Please select 1-9.")
            except ValueError:
                print("Invalid input. Please enter a number.")
    
    def add_expense(self):
        """Add a new expense with user input validation."""
        print("\n--- Add New Expense ---")
        
        # Get amount
        while True:
            amount_str = input("Enter amount: ").strip()
            is_valid, amount = self.validate_amount(amount_str)
            if is_valid:
                break
        
        # Get category
        category = self.get_category_input()
        
        # Get description
        description = input("Enter description (optional): ").strip()
        if not description:
            description = "No description"
        
        # Get date
        while True:
            date_str = input("Enter date (YYYY-MM-DD or 'today'): ").strip()
            is_valid, date = self.validate_date(date_str)
            if is_valid:
                break
        
        # Add to database
        if self.db.add_expense(amount, category, description, date):
            print(f"\nExpense added successfully!")
            print(f"  Amount: ${amount:.2f}")
            print(f"  Category: {category}")
            print(f"  Description: {description}")
            print(f"  Date: {date}")
        else:
            print("Failed to add expense. Please try again.")
    
    def view_all_expenses(self):
        """Display all expenses in a formatted table."""
        print("\n--- All Expenses ---")
        
        expenses = self.db.get_all_expenses()
        
        if not expenses:
            print("No expenses found.")
            return
        
        # Display header
        print(f"{'ID':<4} {'Date':<12} {'Category':<15} {'Amount':<10} {'Description':<20}")
        print("-" * 70)
        
        # Display expenses
        total = 0
        for expense in expenses:
            print(f"{expense['id']:<4} {expense['date']:<12} {expense['category']:<15} "
                  f"${expense['amount']:<9.2f} {expense['description']:<20}")
            total += expense['amount']
        
        print("-" * 70)
        print(f"{'Total:':<44} ${total:.2f}")
        print(f"\nTotal expenses: {len(expenses)}")
    
    def generate_monthly_report(self):
        """Generate and display monthly expense report."""
        print("\n--- Monthly Expense Report ---")
        
        # Get year input
        while True:
            year_str = input("Enter year (press Enter for current year): ").strip()
            if not year_str:
                year = datetime.now().year
                break
            try:
                year = int(year_str)
                if year < 1900 or year > 2100:
                    print("Please enter a valid year between 1900 and 2100.")
                    continue
                break
            except ValueError:
                print("Invalid year. Please enter a valid number.")
        
        # Get report data
        report_data = self.db.get_monthly_report(year)
        
        if not report_data:
            print(f"No expenses found for year {year}.")
            return
        
        # Display report
        print(f"\nMonthly Report for {year}:")
        print(f"{'Month':<10} {'Total':<12} {'Count':<8} {'Average':<12}")
        print("-" * 45)
        
        year_total = 0
        year_count = 0
        
        for month_data in report_data:
            month_name = datetime.strptime(month_data['month'], "%m").strftime("%B")
            average = month_data['total_amount'] / month_data['expense_count']
            
            print(f"{month_name:<10} ${month_data['total_amount']:<11.2f} "
                  f"{month_data['expense_count']:<8} ${average:<11.2f}")
            
            year_total += month_data['total_amount']
            year_count += month_data['expense_count']
        
        print("-" * 45)
        year_average = year_total / year_count if year_count > 0 else 0
        print(f"{'Year Total':<10} ${year_total:<11.2f} {year_count:<8} ${year_average:<11.2f}")
    
    def view_monthly_expenses(self):
        """View detailed expenses for a specific month."""
        print("\n--- View Monthly Expenses ---")
        
        # Get year and month input
        current_year = datetime.now().year
        current_month = datetime.now().month
        
        while True:
            try:
                year_str = input(f"Enter year (default {current_year}): ").strip()
                year = int(year_str) if year_str else current_year
                
                month_str = input(f"Enter month (1-12, default {current_month}): ").strip()
                month = int(month_str) if month_str else current_month
                
                if month < 1 or month > 12:
                    print("Month must be between 1 and 12.")
                    continue
                
                break
            except ValueError:
                print("Invalid input. Please enter valid numbers.")
        
        # Get expenses for the specified month
        expenses = self.db.get_expenses_by_month(year, month)
        month_name = datetime.strptime(str(month), "%m").strftime("%B")
        
        if not expenses:
            print(f"No expenses found for {month_name} {year}.")
            return
        
        # Display expenses
        print(f"\nExpenses for {month_name} {year}:")
        print(f"{'ID':<4} {'Date':<12} {'Category':<15} {'Amount':<10} {'Description':<20}")
        print("-" * 70)
        
        total = 0
        for expense in expenses:
            print(f"{expense['id']:<4} {expense['date']:<12} {expense['category']:<15} "
                  f"${expense['amount']:<9.2f} {expense['description']:<20}")
            total += expense['amount']
        
        print("-" * 70)
        print(f"{'Monthly Total:':<44} ${total:.2f}")
        print(f"Number of expenses: {len(expenses)}")
    
    def close(self):
        """Close database connection."""
        self.db.close()
