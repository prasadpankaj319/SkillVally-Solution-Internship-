"""
Inventory module for Inventory Manager.
Contains all business logic for product management.
"""

from typing import List, Dict, Optional
from database import Database


class InventoryManager:
    """Main inventory management class."""
    
    def __init__(self, db_name: str = "inventory.db"):
        """
        Initialize inventory manager.
        
        Args:
            db_name (str): Database file name
        """
        self.db = Database(db_name)
    
    def add_product(self, name: str, price: float, quantity: int) -> bool:
        """
        Add a new product to inventory.
        
        Args:
            name (str): Product name
            price (float): Product price
            quantity (int): Product quantity
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Check if product already exists
            existing = self.get_product_by_name(name)
            if existing:
                print(f"Error: Product '{name}' already exists!")
                return False
            
            # Validate inputs
            if not self._validate_product_data(name, price, quantity):
                return False
            
            # Insert product
            query = "INSERT INTO products (name, price, quantity) VALUES (?, ?, ?)"
            self.db.execute_query(query, (name, price, quantity))
            self.db.commit()
            print(f"Product '{name}' added successfully!")
            return True
            
        except Exception as e:
            print(f"Error adding product: {e}")
            return False
    
    def get_all_products(self) -> List[Dict]:
        """
        Get all products from inventory.
        
        Returns:
            List[Dict]: List of products
        """
        try:
            query = "SELECT * FROM products ORDER BY name"
            rows = self.db.fetch_all(query)
            return [dict(row) for row in rows]
        except Exception as e:
            print(f"Error fetching products: {e}")
            return []
    
    def get_product_by_name(self, name: str) -> Optional[Dict]:
        """
        Get product by name.
        
        Args:
            name (str): Product name
            
        Returns:
            Optional[Dict]: Product data or None if not found
        """
        try:
            query = "SELECT * FROM products WHERE name = ?"
            row = self.db.fetch_one(query, (name,))
            return dict(row) if row else None
        except Exception as e:
            print(f"Error fetching product: {e}")
            return None
    
    def update_product_quantity(self, name: str, new_quantity: int) -> bool:
        """
        Update product quantity.
        
        Args:
            name (str): Product name
            new_quantity (int): New quantity
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Validate quantity
            if new_quantity < 0:
                print("Error: Quantity cannot be negative!")
                return False
            
            # Check if product exists
            product = self.get_product_by_name(name)
            if not product:
                print(f"Error: Product '{name}' not found!")
                return False
            
            # Update quantity
            query = "UPDATE products SET quantity = ? WHERE name = ?"
            self.db.execute_query(query, (new_quantity, name))
            self.db.commit()
            print(f"Product '{name}' quantity updated to {new_quantity}!")
            return True
            
        except Exception as e:
            print(f"Error updating product: {e}")
            return False
    
    def delete_product(self, name: str) -> bool:
        """
        Delete a product from inventory.
        
        Args:
            name (str): Product name
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Check if product exists
            product = self.get_product_by_name(name)
            if not product:
                print(f"Error: Product '{name}' not found!")
                return False
            
            # Delete product
            query = "DELETE FROM products WHERE name = ?"
            cursor = self.db.execute_query(query, (name,))
            self.db.commit()
            
            if cursor.rowcount > 0:
                print(f"Product '{name}' deleted successfully!")
                return True
            else:
                print(f"Error: Failed to delete product '{name}'!")
                return False
                
        except Exception as e:
            print(f"Error deleting product: {e}")
            return False
    
    def search_products(self, search_term: str) -> List[Dict]:
        """
        Search products by name (partial match).
        
        Args:
            search_term (str): Search term
            
        Returns:
            List[Dict]: List of matching products
        """
        try:
            query = "SELECT * FROM products WHERE name LIKE ? ORDER BY name"
            rows = self.db.fetch_all(query, (f"%{search_term}%",))
            return [dict(row) for row in rows]
        except Exception as e:
            print(f"Error searching products: {e}")
            return []
    
    def get_low_stock_products(self, threshold: int = 10) -> List[Dict]:
        """
        Get products with low stock.
        
        Args:
            threshold (int): Stock threshold
            
        Returns:
            List[Dict]: List of low stock products
        """
        try:
            query = "SELECT * FROM products WHERE quantity <= ? ORDER BY quantity"
            rows = self.db.fetch_all(query, (threshold,))
            return [dict(row) for row in rows]
        except Exception as e:
            print(f"Error fetching low stock products: {e}")
            return []
    
    def _validate_product_data(self, name: str, price: float, quantity: int) -> bool:
        """
        Validate product data.
        
        Args:
            name (str): Product name
            price (float): Product price
            quantity (int): Product quantity
            
        Returns:
            bool: True if valid, False otherwise
        """
        # Validate name
        if not name or not name.strip():
            print("Error: Product name cannot be empty!")
            return False
        
        # Validate price
        if price <= 0:
            print("Error: Price must be greater than 0!")
            return False
        
        # Validate quantity
        if quantity < 0:
            print("Error: Quantity cannot be negative!")
            return False
        
        return True
    
    def display_products(self, products: List[Dict]) -> None:
        """
        Display products in a formatted table.
        
        Args:
            products (List[Dict]): List of products to display
        """
        if not products:
            print("No products found.")
            return
        
        print("\n" + "="*80)
        print(f"{'ID':<5} {'Name':<25} {'Price':<15} {'Quantity':<10}")
        print("="*80)
        
        for product in products:
            print(f"{product['id']:<5} {product['name']:<25} ${product['price']:<14.2f} {product['quantity']:<10}")
        
        print("="*80)
        print(f"Total Products: {len(products)}")
    
    def get_inventory_summary(self) -> Dict:
        """
        Get inventory summary statistics.
        
        Returns:
            Dict: Summary statistics
        """
        try:
            products = self.get_all_products()
            
            if not products:
                return {
                    'total_products': 0,
                    'total_value': 0.0,
                    'total_quantity': 0,
                    'low_stock_count': 0
                }
            
            total_products = len(products)
            total_quantity = sum(p['quantity'] for p in products)
            total_value = sum(p['price'] * p['quantity'] for p in products)
            low_stock_count = len(self.get_low_stock_products())
            
            return {
                'total_products': total_products,
                'total_value': total_value,
                'total_quantity': total_quantity,
                'low_stock_count': low_stock_count
            }
            
        except Exception as e:
            print(f"Error generating summary: {e}")
            return {}
    
    def close(self) -> None:
        """Close database connection."""
        self.db.close()
