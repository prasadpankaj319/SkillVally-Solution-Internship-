# Safe Banking System CLI

A secure, professional CLI-based banking system built with Python and SQLite, designed as an internship-level project with enterprise-grade security practices.

## 🏦 Features

### Core Banking Operations
- **User Registration**: Create new accounts with secure password storage
- **Secure Login**: Password-based authentication with salted hashing
- **Deposit Money**: Add funds to account with transaction logging
- **Withdraw Money**: Remove funds with overdraft protection
- **Balance Inquiry**: Check current account balance
- **Transaction History**: View detailed transaction records
- **Account Summary**: Complete account overview with statistics

### Security Features
- **Password Hashing**: SHA-256 with salt for secure password storage
- **Input Validation**: Strict validation for all user inputs
- **SQL Injection Protection**: Parameterized queries throughout
- **Transaction Safety**: Atomic operations with rollback support
- **Session Management**: Secure user session handling

## 📁 Project Structure

```
safe_banking_cli/
├── database.py      # Database operations and schema management
├── auth.py          # Authentication and session management
├── banking.py       # Core banking operations
├── main.py          # CLI interface and application entry point
├── README.md        # Project documentation
└── banking_system.db  # SQLite database (created automatically)
```

## 🚀 Getting Started

### Prerequisites
- Python 3.7 or higher
- No external dependencies required (uses only Python standard library)

### Installation
1. Clone or download the project
2. Navigate to the `safe_banking_cli` directory
3. Run the application:

```bash
python main.py
```

The database will be created automatically on first run.

## 🎮 Usage Guide

### Main Menu
When you start the application, you'll see the main menu:

**Not Logged In:**
1. Register New Account
2. Login
0. Exit

**Logged In:**
1. Deposit Money
2. Withdraw Money
3. Check Balance
4. View Transaction History
5. Account Summary
6. Logout
0. Exit

### Registration Process
1. Choose option 1 (Register New Account)
2. Enter a username (3-50 characters, alphanumeric + underscore/hyphen)
3. Enter a password (minimum 8 characters, must include uppercase, lowercase, and digit)
4. Confirm your password
5. Enter initial deposit amount (optional, up to $1,000,000)

### Login Process
1. Choose option 2 (Login)
2. Enter your username
3. Enter your password
4. System will authenticate and display your current balance

### Banking Operations

#### Deposit Money
- Enter amount ($0.01 - $1,000,000)
- Optional: Add a description for the transaction
- System updates balance and creates transaction record

#### Withdraw Money
- View current balance
- Enter withdrawal amount
- Confirm the transaction
- System checks for sufficient funds before processing

#### Transaction History
- Displays last 50 transactions by default
- Shows date, type, amount, balance after, and description
- Most recent transactions appear first

#### Account Summary
- Complete account overview
- Current balance
- Total deposits and withdrawals
- Recent transaction history

## 🔒 Security Architecture

### Password Hashing
- Uses SHA-256 algorithm with unique salt per user
- Salt: 32-byte hexadecimal string generated using `secrets.token_hex()`
- Storage format: `salt:hash`
- Verification: Hashes input password with stored salt and compares

### Database Security
- SQLite with foreign key constraints enabled
- Parameterized queries prevent SQL injection
- Atomic transactions with commit/rollback
- Input validation at application layer

### Transaction Safety
- All financial operations use Decimal for precise calculations
- Negative balance prevention through multiple checks
- Transaction logging for audit trail
- Database constraints ensure data integrity

## 🛠️ Technical Implementation

### Database Schema

#### Users Table
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    balance DECIMAL(15, 2) DEFAULT 0.00,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### Transactions Table
```sql
CREATE TABLE transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    transaction_type TEXT NOT NULL CHECK (transaction_type IN ('DEPOSIT', 'WITHDRAWAL')),
    amount DECIMAL(15, 2) NOT NULL CHECK (amount > 0),
    balance_after DECIMAL(15, 2) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id)
);
```

### Key Classes

#### DatabaseManager
- Handles all SQLite operations
- Connection management with context managers
- Schema creation and migrations
- Query execution with error handling

#### AuthenticationManager
- User registration and login
- Password hashing and verification
- Session management
- Input validation for credentials

#### BankingManager
- Core banking operations
- Transaction processing
- Balance management
- Account summaries

#### BankingCLI
- Command-line interface
- Menu navigation
- User input handling
- Display formatting

## 🔍 Edge Cases Handled

### Authentication
- ✅ Duplicate username detection
- ✅ Invalid login credentials
- ✅ Password strength validation
- ✅ Username format validation
- ✅ Session timeout handling

### Banking Operations
- ✅ Negative deposit prevention
- ✅ Insufficient balance protection
- ✅ Maximum transaction limits
- ✅ Decimal precision handling
- ✅ Concurrent transaction safety

### Input Validation
- ✅ Non-numeric input handling
- ✅ Empty field validation
- ✅ Length limits enforcement
- ✅ Special character handling
- ✅ SQL injection prevention

### Database Operations
- ✅ Connection error handling
- ✅ Transaction rollback on failure
- ✅ Foreign key constraint violations
- ✅ Unique constraint violations
- ✅ Database file permissions

## 📈 Scaling to Enterprise Level

### Architecture Improvements
1. **Database Layer**
   - Migrate to PostgreSQL or MySQL for better performance
   - Implement connection pooling
   - Add database replication for high availability
   - Use Redis for caching frequently accessed data

2. **Security Enhancements**
   - Implement multi-factor authentication (MFA)
   - Add rate limiting and brute force protection
   - Use bcrypt or Argon2 for password hashing
   - Implement OAuth 2.0 for third-party authentication

3. **API Layer**
   - Create RESTful API using FastAPI or Django REST Framework
   - Implement JWT-based authentication
   - Add API versioning and documentation
   - Use GraphQL for flexible data queries

4. **Microservices Architecture**
   - Separate authentication service
   - Dedicated transaction service
   - Notification service for alerts
   - Audit logging service

5. **Performance Optimizations**
   - Implement database indexing strategies
   - Add horizontal scaling capabilities
   - Use message queues for async operations
   - Implement caching layers

6. **Monitoring & Observability**
   - Add application performance monitoring (APM)
   - Implement centralized logging
   - Add health check endpoints
   - Set up alerting and incident response

7. **Compliance & Regulations**
   - Implement GDPR compliance features
   - Add audit trails for regulatory requirements
   - Implement data encryption at rest and in transit
   - Add role-based access control (RBAC)

### Technology Stack Recommendations
- **Backend**: FastAPI, Django, or Spring Boot
- **Database**: PostgreSQL with Redis caching
- **Authentication**: OAuth 2.0 + JWT
- **Message Queue**: RabbitMQ or Apache Kafka
- **Monitoring**: Prometheus + Grafana
- **Containerization**: Docker + Kubernetes
- **CI/CD**: Jenkins or GitLab CI

## 🧪 Testing

### Manual Testing Steps
1. **Registration Test**
   - Try registering with valid data
   - Attempt duplicate username registration
   - Test password validation rules

2. **Login Test**
   - Login with correct credentials
   - Attempt login with wrong password
   - Try login with non-existent username

3. **Banking Operations Test**
   - Deposit various amounts
   - Withdraw within limits
   - Attempt overdraft
   - Check transaction history

4. **Edge Cases Test**
   - Enter negative amounts
   - Use special characters in inputs
   - Test concurrent operations
   - Verify database constraints

## 📝 Development Notes

### Code Quality
- Follows PEP 8 formatting standards
- Comprehensive error handling
- Type hints for better code documentation
- Modular design for maintainability
- Clean code principles throughout

### Best Practices Implemented
- Separation of concerns
- Dependency injection
- Context managers for resource management
- Custom exceptions for better error handling
- Input validation at multiple layers

## 🤝 Contributing

This project serves as a learning example for secure banking system development. Feel free to:
- Study the code architecture
- Suggest improvements
- Report security issues
- Extend functionality

## 📄 License

This project is for educational purposes. Use responsibly and ensure compliance with financial regulations in production environments.

---

**Note**: This is a demonstration project and should not be used in production without additional security measures and regulatory compliance checks.
