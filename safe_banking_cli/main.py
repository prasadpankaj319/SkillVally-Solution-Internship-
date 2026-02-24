"""
Main CLI interface for Safe Banking System.

This module provides:
- Command-line interface
- Menu navigation
- User input handling
- System entry point
"""

import os
import sys
import getpass
from typing import Optional
from auth import auth_manager
from banking import banking_manager


class BankingCLI:
    """Command-line interface for the banking system."""
    
    def __init__(self):
        """Initialize CLI application."""
        self.running = True
    
    def clear_screen(self):
        """Clear the terminal screen."""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_header(self, title: str):
        """Print application header."""
        print("=" * 60)
        print(f"{title:^60}")
        print("=" * 60)
        print()
    
    def print_success(self, message: str):
        """Print success message in green."""
        print(f"✓ {message}")
        print()
    
    def print_error(self, message: str):
        """Print error message in red."""
        print(f"✗ {message}")
        print()
    
    def print_info(self, message: str):
        """Print info message in blue."""
        print(f"ℹ {message}")
        print()
    
    def get_valid_float(self, prompt: str, min_value: float = 0.01, 
                        max_value: float = 1000000) -> Optional[float]:
        """
        Get valid float input from user.
        
        Args:
            prompt (str): Input prompt
            min_value (float): Minimum allowed value
            max_value (float): Maximum allowed value
            
        Returns:
            float: Validated float value or None if cancelled
        """
        while True:
            try:
                user_input = input(prompt).strip()
                
                # Allow user to cancel
                if user_input.lower() in ['cancel', 'exit', 'quit']:
                    return None
                
                amount = float(user_input)
                
                if amount < min_value:
                    self.print_error(f"Amount must be at least ${min_value:.2f}")
                    continue
                
                if amount > max_value:
                    self.print_error(f"Amount cannot exceed ${max_value:,.2f}")
                    continue
                
                return amount
                
            except ValueError:
                self.print_error("Please enter a valid number.")
    
    def get_valid_string(self, prompt: str, min_length: int = 1, 
                         max_length: int = 50, allow_empty: bool = False) -> Optional[str]:
        """
        Get valid string input from user.
        
        Args:
            prompt (str): Input prompt
            min_length (int): Minimum length
            max_length (int): Maximum length
            allow_empty (bool): Allow empty input
            
        Returns:
            str: Validated string or None if cancelled
        """
        while True:
            user_input = input(prompt).strip()
            
            # Allow user to cancel
            if user_input.lower() in ['cancel', 'exit', 'quit']:
                return None
            
            if not allow_empty and not user_input:
                self.print_error("This field is required.")
                continue
            
            if len(user_input) < min_length:
                self.print_error(f"Minimum length is {min_length} characters.")
                continue
            
            if len(user_input) > max_length:
                self.print_error(f"Maximum length is {max_length} characters.")
                continue
            
            return user_input
    
    def get_password(self, prompt: str = "Password: ") -> Optional[str]:
        """
        Get password input securely.
        
        Args:
            prompt (str): Password prompt
            
        Returns:
            str: Password or None if cancelled
        """
        while True:
            try:
                password = getpass.getpass(prompt)
                
                # Allow user to cancel
                if password.lower() in ['cancel', 'exit', 'quit']:
                    return None
                
                return password
                
            except KeyboardInterrupt:
                print("\nOperation cancelled.")
                return None
    
    def confirm_action(self, message: str) -> bool:
        """
        Get user confirmation for an action.
        
        Args:
            message (str): Confirmation message
            
        Returns:
            bool: True if confirmed, False otherwise
        """
        while True:
            response = input(f"{message} (y/n): ").strip().lower()
            
            if response in ['y', 'yes']:
                return True
            elif response in ['n', 'no']:
                return False
            else:
                self.print_error("Please enter 'y' or 'n'.")
    
    def display_transaction_history(self, transactions: list):
        """Display transaction history in a formatted table."""
        if not transactions:
            self.print_info("No transactions to display.")
            return
        
        print("\n" + "=" * 80)
        print(f"{'Date':<20} {'Type':<12} {'Amount':<12} {'Balance After':<15} {'Description'}")
        print("=" * 80)
        
        for transaction in transactions:
            date = transaction['date'][:19]  # Remove microseconds
            trans_type = transaction['type']
            amount = f"${transaction['amount']:.2f}"
            balance = f"${transaction['balance_after']:.2f}"
            description = transaction['description'][:30] + "..." if len(transaction['description']) > 30 else transaction['description']
            
            print(f"{date:<20} {trans_type:<12} {amount:<12} {balance:<15} {description}")
        
        print("=" * 80)
        print()
    
    def show_main_menu(self):
        """Display main menu options."""
        self.print_header("SAFE BANKING SYSTEM")
        
        if auth_manager.is_logged_in():
            current_user = auth_manager.get_current_user()
            print(f"Logged in as: {current_user['username']}")
            print(f"Current Balance: ${current_user['balance']:.2f}")
            print()
            print("1. Deposit Money")
            print("2. Withdraw Money")
            print("3. Check Balance")
            print("4. View Transaction History")
            print("5. Account Summary")
            print("6. Logout")
        else:
            print("1. Register New Account")
            print("2. Login")
        
        print("0. Exit")
        print()
    
    def handle_registration(self):
        """Handle user registration process."""
        self.clear_screen()
        self.print_header("USER REGISTRATION")
        
        try:
            # Get username
            username = self.get_valid_string(
                "Enter username (letters, numbers, underscore, hyphen only): ",
                min_length=3,
                max_length=50
            )
            
            if username is None:
                return
            
            # Get password
            password = self.get_password("Enter password: ")
            if password is None:
                return
            
            # Confirm password
            confirm_password = self.get_password("Confirm password: ")
            if confirm_password is None:
                return
            
            if password != confirm_password:
                self.print_error("Passwords do not match.")
                input("Press Enter to continue...")
                return
            
            # Get initial deposit
            initial_deposit = self.get_valid_float(
                "Enter initial deposit amount (0-1000000): ",
                min_value=0,
                max_value=1000000
            )
            
            if initial_deposit is None:
                return
            
            # Register user
            result = auth_manager.register_user(username, password, initial_deposit)
            
            if result['success']:
                self.print_success(result['message'])
                if initial_deposit > 0:
                    print(f"Initial deposit: ${initial_deposit:.2f}")
            else:
                self.print_error(result['message'])
            
        except Exception as e:
            self.print_error(f"Registration failed: {str(e)}")
        
        input("Press Enter to continue...")
    
    def handle_login(self):
        """Handle user login process."""
        self.clear_screen()
        self.print_header("USER LOGIN")
        
        try:
            # Get username
            username = self.get_valid_string(
                "Enter username: ",
                min_length=1,
                max_length=50
            )
            
            if username is None:
                return
            
            # Get password
            password = self.get_password("Enter password: ")
            if password is None:
                return
            
            # Attempt login
            result = auth_manager.login(username, password)
            
            if result['success']:
                self.print_success(result['message'])
                print(f"Current Balance: ${result['user']['balance']:.2f}")
            else:
                self.print_error(result['message'])
            
        except Exception as e:
            self.print_error(f"Login failed: {str(e)}")
        
        input("Press Enter to continue...")
    
    def handle_deposit(self):
        """Handle deposit process."""
        self.clear_screen()
        self.print_header("DEPOSIT MONEY")
        
        try:
            # Get amount
            amount = self.get_valid_float(
                "Enter deposit amount (0.01-1000000): ",
                min_value=0.01,
                max_value=1000000
            )
            
            if amount is None:
                return
            
            # Get description (optional)
            description = self.get_valid_string(
                "Enter description (optional): ",
                allow_empty=True,
                max_length=100
            )
            
            # Process deposit
            result = banking_manager.deposit(amount, description if description else None)
            
            if result['success']:
                self.print_success(result['message'])
                print(f"New Balance: ${result['new_balance']:.2f}")
            else:
                self.print_error(result['message'])
            
        except Exception as e:
            self.print_error(f"Deposit failed: {str(e)}")
        
        input("Press Enter to continue...")
    
    def handle_withdrawal(self):
        """Handle withdrawal process."""
        self.clear_screen()
        self.print_header("WITHDRAW MONEY")
        
        try:
            # Show current balance
            balance_result = banking_manager.check_balance()
            if balance_result['success']:
                print(f"Current Balance: ${balance_result['balance']:.2f}")
                print()
            
            # Get amount
            amount = self.get_valid_float(
                "Enter withdrawal amount (0.01-1000000): ",
                min_value=0.01,
                max_value=1000000
            )
            
            if amount is None:
                return
            
            # Get description (optional)
            description = self.get_valid_string(
                "Enter description (optional): ",
                allow_empty=True,
                max_length=100
            )
            
            # Confirm withdrawal
            if not self.confirm_action(f"Confirm withdrawal of ${amount:.2f}?"):
                self.print_info("Withdrawal cancelled.")
                input("Press Enter to continue...")
                return
            
            # Process withdrawal
            result = banking_manager.withdraw(amount, description if description else None)
            
            if result['success']:
                self.print_success(result['message'])
                print(f"New Balance: ${result['new_balance']:.2f}")
            else:
                self.print_error(result['message'])
            
        except Exception as e:
            self.print_error(f"Withdrawal failed: {str(e)}")
        
        input("Press Enter to continue...")
    
    def handle_balance_check(self):
        """Handle balance check."""
        self.clear_screen()
        self.print_header("ACCOUNT BALANCE")
        
        try:
            result = banking_manager.check_balance()
            
            if result['success']:
                print(f"Your current balance is: ${result['balance']:.2f}")
                self.print_success("Balance retrieved successfully.")
            else:
                self.print_error(result['message'])
            
        except Exception as e:
            self.print_error(f"Failed to check balance: {str(e)}")
        
        input("Press Enter to continue...")
    
    def handle_transaction_history(self):
        """Handle transaction history display."""
        self.clear_screen()
        self.print_header("TRANSACTION HISTORY")
        
        try:
            result = banking_manager.get_transaction_history()
            
            if result['success']:
                if result['transactions']:
                    self.display_transaction_history(result['transactions'])
                else:
                    self.print_info(result['message'])
            else:
                self.print_error(result['message'])
            
        except Exception as e:
            self.print_error(f"Failed to retrieve transaction history: {str(e)}")
        
        input("Press Enter to continue...")
    
    def handle_account_summary(self):
        """Handle account summary display."""
        self.clear_screen()
        self.print_header("ACCOUNT SUMMARY")
        
        try:
            result = banking_manager.get_account_summary()
            
            if result['success']:
                account_info = result['account_info']
                
                print(f"Username: {account_info['username']}")
                print(f"Current Balance: ${account_info['current_balance']:.2f}")
                print(f"Total Deposits: ${account_info['total_deposits']:.2f}")
                print(f"Total Withdrawals: ${account_info['total_withdrawals']:.2f}")
                
                if account_info['recent_transactions']:
                    print("\nRecent Transactions:")
                    self.display_transaction_history(account_info['recent_transactions'])
                
                self.print_success("Account summary retrieved successfully.")
            else:
                self.print_error(result['message'])
            
        except Exception as e:
            self.print_error(f"Failed to retrieve account summary: {str(e)}")
        
        input("Press Enter to continue...")
    
    def handle_logout(self):
        """Handle user logout."""
        try:
            result = auth_manager.logout()
            
            if result['success']:
                self.print_success(result['message'])
            else:
                self.print_error(result['message'])
            
        except Exception as e:
            self.print_error(f"Logout failed: {str(e)}")
        
        input("Press Enter to continue...")
    
    def run(self):
        """Main application loop."""
        while self.running:
            try:
                self.clear_screen()
                self.show_main_menu()
                
                # Get user choice
                if auth_manager.is_logged_in():
                    choice = input("Enter your choice (0-6): ").strip()
                else:
                    choice = input("Enter your choice (0-2): ").strip()
                
                # Handle menu selection
                if choice == '0':
                    if self.confirm_action("Are you sure you want to exit?"):
                        self.running = False
                        self.print_success("Thank you for using Safe Banking System!")
                        break
                
                elif auth_manager.is_logged_in():
                    if choice == '1':
                        self.handle_deposit()
                    elif choice == '2':
                        self.handle_withdrawal()
                    elif choice == '3':
                        self.handle_balance_check()
                    elif choice == '4':
                        self.handle_transaction_history()
                    elif choice == '5':
                        self.handle_account_summary()
                    elif choice == '6':
                        self.handle_logout()
                    else:
                        self.print_error("Invalid choice. Please try again.")
                        input("Press Enter to continue...")
                
                else:  # Not logged in
                    if choice == '1':
                        self.handle_registration()
                    elif choice == '2':
                        self.handle_login()
                    else:
                        self.print_error("Invalid choice. Please try again.")
                        input("Press Enter to continue...")
            
            except KeyboardInterrupt:
                print("\n\nExiting application...")
                self.running = True
                break
            
            except Exception as e:
                self.print_error(f"An unexpected error occurred: {str(e)}")
                input("Press Enter to continue...")


def main():
    """Main entry point for the application."""
    try:
        app = BankingCLI()
        app.run()
    except Exception as e:
        print(f"Application failed to start: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
