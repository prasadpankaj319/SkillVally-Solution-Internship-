"""
Main module for Inventory Manager CLI application.
Provides command-line interface for inventory management.
"""

import os
import sys
from typing import Optional
from inventory import InventoryManager


class InventoryCLI:
    """Command-line interface for inventory management."""
    
    def __init__(self):
        """Initialize CLI application."""
        self.inventory = InventoryManager()
        self.running = True
    
    def display_menu(self) -> None:
        """Display main menu options."""
        print("\n" + "="*50)
        print("     INVENTORY MANAGEMENT SYSTEM")
        print("="*50)
        print("1. Add Product")
        print("2. View All Products")
        print("3. Update Product Quantity")
        print("4. Delete Product")
        print("5. Search Product")
        print("6. View Inventory Summary")
        print("7. View Low Stock Products")
        print("8. Exit")
        print("="*50)
    
    def get_user_choice(self) -> int:
        """
        Get user menu choice.
        
        Returns:
            int: User's menu choice
        """
        while True:
            try:
                choice = input("Enter your choice (1-8): ").strip()
                choice_num = int(choice)
                if 1 <= choice_num <= 8:
                    return choice_num
                else:
                    print("Invalid choice! Please enter a number between 1 and 8.")
            except ValueError:
                print("Invalid input! Please enter a valid number.")
    
    def get_string_input(self, prompt: str, allow_empty: bool = False) -> str:
        """
        Get string input from user.
        
        Args:
            prompt (str): Input prompt
            allow_empty (bool): Whether to allow empty input
            
        Returns:
            str: User input
        """
        while True:
            value = input(prompt).strip()
            if value or allow_empty:
                return value
            print("Input cannot be empty! Please try again.")
    
    def get_float_input(self, prompt: str, min_value: float = 0.01) -> float:
        """
        Get float input from user with validation.
        
        Args:
            prompt (str): Input prompt
            min_value (float): Minimum allowed value
            
        Returns:
            float: Validated float input
        """
        while True:
            try:
                value = float(input(prompt).strip())
                if value >= min_value:
                    return value
                else:
                    print(f"Value must be at least {min_value}!")
            except ValueError:
                print("Invalid input! Please enter a valid number.")
    
    def get_int_input(self, prompt: str, min_value: int = 0) -> int:
        """
        Get integer input from user with validation.
        
        Args:
            prompt (str): Input prompt
            min_value (int): Minimum allowed value
            
        Returns:
            int: Validated integer input
        """
        while True:
            try:
                value = int(input(prompt).strip())
                if value >= min_value:
                    return value
                else:
                    print(f"Value must be at least {min_value}!")
            except ValueError:
                print("Invalid input! Please enter a valid integer.")
    
    def add_product(self) -> None:
        """Handle add product functionality."""
        print("\n--- Add New Product ---")
        
        name = self.get_string_input("Enter product name: ")
        price = self.get_float_input("Enter product price: $", 0.01)
        quantity = self.get_int_input("Enter product quantity: ", 0)
        
        self.inventory.add_product(name, price, quantity)
    
    def view_all_products(self) -> None:
        """Handle view all products functionality."""
        print("\n--- All Products ---")
        
        products = self.inventory.get_all_products()
        self.inventory.display_products(products)
    
    def update_product_quantity(self) -> None:
        """Handle update product quantity functionality."""
        print("\n--- Update Product Quantity ---")
        
        name = self.get_string_input("Enter product name: ")
        
        # Check if product exists
        product = self.inventory.get_product_by_name(name)
        if not product:
            print(f"Product '{name}' not found!")
            return
        
        print(f"Current quantity: {product['quantity']}")
        new_quantity = self.get_int_input("Enter new quantity: ", 0)
        
        self.inventory.update_product_quantity(name, new_quantity)
    
    def delete_product(self) -> None:
        """Handle delete product functionality."""
        print("\n--- Delete Product ---")
        
        name = self.get_string_input("Enter product name to delete: ")
        
        # Show product details before deletion
        product = self.inventory.get_product_by_name(name)
        if not product:
            print(f"Product '{name}' not found!")
            return
        
        print(f"\nProduct to delete:")
        print(f"Name: {product['name']}")
        print(f"Price: ${product['price']:.2f}")
        print(f"Quantity: {product['quantity']}")
        
        # Confirm deletion
        confirm = input("\nAre you sure you want to delete this product? (y/n): ").strip().lower()
        if confirm == 'y':
            self.inventory.delete_product(name)
        else:
            print("Deletion cancelled.")
    
    def search_product(self) -> None:
        """Handle search product functionality."""
        print("\n--- Search Product ---")
        
        search_term = self.get_string_input("Enter search term: ")
        
        products = self.inventory.search_products(search_term)
        
        if products:
            print(f"\nFound {len(products)} product(s) matching '{search_term}':")
            self.inventory.display_products(products)
        else:
            print(f"No products found matching '{search_term}'.")
    
    def view_inventory_summary(self) -> None:
        """Handle view inventory summary functionality."""
        print("\n--- Inventory Summary ---")
        
        summary = self.inventory.get_inventory_summary()
        
        if summary:
            print(f"Total Products: {summary['total_products']}")
            print(f"Total Quantity: {summary['total_quantity']}")
            print(f"Total Value: ${summary['total_value']:.2f}")
            print(f"Low Stock Products: {summary['low_stock_count']}")
        else:
            print("Unable to generate summary.")
    
    def view_low_stock_products(self) -> None:
        """Handle view low stock products functionality."""
        print("\n--- Low Stock Products ---")
        
        threshold = self.get_int_input("Enter low stock threshold (default 10): ", 1)
        if threshold == 0:
            threshold = 10  # Default value
        
        products = self.inventory.get_low_stock_products(threshold)
        
        if products:
            print(f"\n{len(products)} product(s) with stock <= {threshold}:")
            self.inventory.display_products(products)
        else:
            print(f"No products with stock <= {threshold}.")
    
    def clear_screen(self) -> None:
        """Clear the console screen."""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def run(self) -> None:
        """Run the main application loop."""
        print("Welcome to Inventory Management System!")
        
        try:
            while self.running:
                self.display_menu()
                choice = self.get_user_choice()
                
                if choice == 1:
                    self.add_product()
                elif choice == 2:
                    self.view_all_products()
                elif choice == 3:
                    self.update_product_quantity()
                elif choice == 4:
                    self.delete_product()
                elif choice == 5:
                    self.search_product()
                elif choice == 6:
                    self.view_inventory_summary()
                elif choice == 7:
                    self.view_low_stock_products()
                elif choice == 8:
                    self.exit_application()
                
                # Pause before showing menu again
                if self.running:
                    input("\nPress Enter to continue...")
                    self.clear_screen()
                    
        except KeyboardInterrupt:
            print("\n\nApplication interrupted by user.")
        except Exception as e:
            print(f"\nUnexpected error: {e}")
        finally:
            self.inventory.close()
    
    def exit_application(self) -> None:
        """Exit the application."""
        print("\nThank you for using Inventory Management System!")
        print("Goodbye!")
        self.running = False


def main():
    """Main entry point for the application."""
    try:
        cli = InventoryCLI()
        cli.run()
    except Exception as e:
        print(f"Failed to start application: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
