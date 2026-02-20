# Inventory Management System

A professional CLI-based Inventory Manager built with Python and SQLite database.

## Features

- **Product Management**: Add, update, delete, and search products
- **Stock Tracking**: Monitor product quantities and get low stock alerts
- **Data Validation**: Comprehensive input validation and error handling
- **SQLite Database**: Reliable data storage with parameterized queries
- **User-Friendly CLI**: Intuitive command-line interface with clear menus

## Project Structure

```
inventory_manager/
├── database.py      # Database operations and SQLite management
├── inventory.py     # Business logic for inventory management
├── main.py         # CLI interface and application entry point
└── README.md       # Project documentation
```

## Requirements

- Python 3.7+
- SQLite3 (included with Python)

## Installation

1. Clone or download the project
2. Navigate to the `inventory_manager` directory
3. Run the application:

```bash
python main.py
```

## Usage

### Main Menu Options

1. **Add Product**: Add new products with name, price, and quantity
2. **View All Products**: Display all products in a formatted table
3. **Update Product Quantity**: Modify stock levels for existing products
4. **Delete Product**: Remove products from inventory
5. **Search Product**: Find products by name (partial search supported)
6. **View Inventory Summary**: Get statistics about your inventory
7. **View Low Stock Products**: Identify products with low stock levels
8. **Exit**: Close the application

### Example Workflow

```bash
# Start the application
python main.py

# Add a product
1. Add Product
Enter product name: Laptop
Enter product price: $999.99
Enter product quantity: 15

# View all products
2. View All Products

# Update stock
3. Update Product Quantity
Enter product name: Laptop
Current quantity: 15
Enter new quantity: 12

# Search products
5. Search Product
Enter search term: lap
```

## Data Storage

The application uses SQLite database (`inventory.db`) to store product information:

### Database Schema

```sql
CREATE TABLE products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    price REAL NOT NULL,
    quantity INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Data Validation

- **Product Name**: Must be non-empty and unique
- **Price**: Must be greater than 0
- **Quantity**: Must be non-negative integer
- **Search**: Partial string matching with case sensitivity

## Error Handling

The application handles various edge cases:

- **Invalid Input**: Non-numeric values for price/quantity
- **Negative Values**: Negative prices or quantities
- **Duplicate Products**: Prevents adding products with existing names
- **Not Found Errors**: Handles updates/deletes for non-existent products
- **Database Errors**: Graceful handling of connection/query failures
- **Empty Inventory**: Proper messaging when no products exist

## Code Architecture

### Modular Design

1. **database.py**: Database abstraction layer
   - Connection management
   - Query execution with parameterization
   - Transaction handling
   - Context manager support

2. **inventory.py**: Business logic layer
   - Product CRUD operations
   - Data validation
   - Search functionality
   - Summary statistics

3. **main.py**: Presentation layer
   - CLI interface
   - User input validation
   - Menu navigation
   - Error display

### Design Patterns

- **Repository Pattern**: Database class abstracts data access
- **Service Layer**: InventoryManager contains business logic
- **Input Validation**: Centralized validation methods
- **Error Handling**: Comprehensive exception management

## Stock Management Logic

### Quantity Updates

- **Direct Updates**: Set exact quantity values
- **Validation**: Prevents negative stock levels
- **Transaction Safety**: All updates are atomic
- **Audit Trail**: Timestamps track creation dates

### Low Stock Alerts

- **Configurable Threshold**: User-defined low stock levels
- **Automatic Detection**: Built-in low stock reporting
- **Proactive Management**: Early warning for restocking

## Edge Cases Handled

1. **Input Validation**
   - Empty product names
   - Invalid numeric inputs
   - Negative values
   - Non-integer quantities

2. **Data Integrity**
   - Duplicate product names
   - Product not found scenarios
   - Database connection failures
   - SQL injection prevention

3. **User Experience**
   - Empty inventory display
   - Search with no results
   - Confirmation for destructive actions
   - Clear error messages

## Scaling to Enterprise Level

### Database Improvements

1. **Database Migration**
   - PostgreSQL or MySQL for better performance
   - Connection pooling for high concurrency
   - Database clustering for high availability

2. **Schema Enhancements**
   - Product categories and tags
   - Supplier information
   - Purchase orders and sales tracking
   - Multi-warehouse support

3. **Performance Optimization**
   - Database indexing on frequently queried fields
   - Caching layer (Redis/Memcached)
   - Query optimization and pagination

### Architecture Enhancements

1. **Microservices**
   - Separate services for inventory, orders, users
   - API Gateway for request routing
   - Service discovery and load balancing

2. **Security**
   - User authentication and authorization
   - Role-based access control (RBAC)
   - API rate limiting and throttling
   - Audit logging and compliance

3. **Monitoring and Observability**
   - Application performance monitoring (APM)
   - Centralized logging (ELK stack)
   - Metrics collection and alerting
   - Health checks and circuit breakers

### Business Features

1. **Advanced Inventory Management**
   - Batch and expiry tracking
   - Automated reordering
   - Demand forecasting
   - Multi-currency support

2. **Integration Capabilities**
   - RESTful APIs for third-party integration
   - Webhook support for real-time updates
   - Import/export functionality
   - ERP system integration

## Converting to Web Application

### Technology Stack Options

1. **Backend Frameworks**
   - **Flask**: Lightweight, good for REST APIs
   - **Django**: Full-featured, built-in admin interface
   - **FastAPI**: Modern, high-performance, automatic docs

2. **Frontend Frameworks**
   - **React**: Component-based, large ecosystem
   - **Vue.js**: Progressive, easy to learn
   - **Angular**: Enterprise-grade, comprehensive

3. **Database and Infrastructure**
   - **PostgreSQL**: Advanced features, better performance
   - **Docker**: Containerization for deployment
   - **AWS/Azure/GCP**: Cloud hosting options

### Implementation Steps

1. **API Development**
   ```python
   # Example Flask API endpoint
   from flask import Flask, request, jsonify
   from inventory import InventoryManager
   
   app = Flask(__name__)
   inventory = InventoryManager()
   
   @app.route('/api/products', methods=['GET'])
   def get_products():
       products = inventory.get_all_products()
       return jsonify(products)
   
   @app.route('/api/products', methods=['POST'])
   def add_product():
       data = request.get_json()
       result = inventory.add_product(
           data['name'], 
           data['price'], 
           data['quantity']
       )
       return jsonify({'success': result})
   ```

2. **Frontend Development**
   - React components for product management
   - State management with Redux/Context API
   - Responsive design with Tailwind CSS
   - Real-time updates with WebSockets

3. **Authentication and Security**
   - JWT-based authentication
   - OAuth2 integration
   - Input sanitization and validation
   - HTTPS and secure headers

4. **Deployment**
   - Docker containerization
   - CI/CD pipeline with GitHub Actions
   - Environment configuration management
   - Database migrations and backups

### Sample Web Application Structure

```
web_inventory/
├── backend/
│   ├── app/
│   │   ├── models/
│   │   ├── routes/
│   │   ├── services/
│   │   └── utils/
│   ├── tests/
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   └── utils/
│   ├── public/
│   └── package.json
├── docker-compose.yml
└── README.md
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

This project is open source and available under the MIT License.

## Support

For questions or issues, please create an issue in the repository or contact the development team.

---

**Note**: This application is designed as a learning project and demonstration of best practices in Python development, database management, and CLI application design.
