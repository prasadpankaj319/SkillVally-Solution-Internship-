# Expense Tracker - Python Internship Project

A professional CLI-based Expense Tracker built with Python and SQLite for personal finance management.

**Project Type:** Python Backend Development Internship  
**Technologies:** Python, SQLite, CLI  
**Architecture:** Modular Programming  

## Features

- ✅ Add expenses with amount, category, description, and date
- ✅ View all expenses in formatted table
- ✅ Generate monthly expense reports
- ✅ View detailed expenses for specific months
- ✅ Input validation and error handling
- ✅ SQLite database for persistent storage
- ✅ Modular and clean code architecture

## Project Structure

```
expense_tracker/
├── database.py    # Database operations and SQLite management
├── tracker.py     # Business logic and expense tracking
├── main.py        # CLI interface and application entry point
├── README.md      # Project documentation
├── requirements.txt # Dependencies (built-in modules only)
├── run.bat        # Windows launcher
└── expenses.db    # SQLite database (created automatically)
```

## Installation & Running

### Prerequisites
- Python 3.6 or higher
- No external dependencies (uses built-in sqlite3)

### How to Run

#### Method 1: Double-click (Windows)
```
Double-click: run.bat
```

#### Method 2: Command Line
```bash
cd expense_tracker
python main.py
```

### Application Menu
1. **Add New Expense** - Record expense with validation
2. **View All Expenses** - Display all recorded expenses
3. **View Monthly Expenses** - Filter by specific month
4. **Generate Monthly Report** - Get statistics by month
5. **Exit** - Save and close application

## Technical Implementation

### Database Schema
```sql
CREATE TABLE expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    amount REAL NOT NULL,
    category TEXT NOT NULL,
    description TEXT,
    date TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Modular Architecture
- **database.py**: SQLite operations, connection management, data persistence
- **tracker.py**: Business logic, input validation, expense management
- **main.py**: CLI interface, menu handling, application flow

### Key Features
- **Input Validation**: Comprehensive validation for amounts, dates, user inputs
- **Error Handling**: Graceful error handling with user-friendly messages
- **Security**: Parameterized queries prevent SQL injection
- **Resource Management**: Automatic database connection cleanup

## Code Quality

### Standards Followed
- ✅ PEP8 formatting and style guidelines
- ✅ Clean code principles
- ✅ Comprehensive error handling
- ✅ Input validation and sanitization
- ✅ Modular programming structure
- ✅ Helpful comments and documentation

### Edge Cases Handled
1. Invalid input (non-numeric amounts, invalid dates)
2. Database errors (connection failures, query errors)
3. User interruption (Ctrl+C handling)
4. Empty database (graceful handling)
5. File permissions and access issues

## Monthly Report System

The monthly report provides:
- Total expenses per month
- Number of transactions per month
- Average expense per transaction
- Yearly totals and averages

**Implementation**: Uses SQLite's `strftime()` function for date grouping and aggregation.

## Data Storage

- **Database**: SQLite (`expenses.db`)
- **Location**: Same directory as application
- **Format**: Single file database (portable)
- **Backup**: Simply copy the `.db` file

## Testing & Validation

The application includes comprehensive input validation:
- **Amount Validation**: Positive numbers only
- **Date Validation**: Multiple formats (YYYY-MM-DD, DD-MM-YYYY, "today")
- **Category Validation**: Predefined categories with custom option
- **Description Validation**: Optional field with default value

## Future Enhancements (Scalability)

### Short-term Improvements
1. User authentication system
2. Budget management and alerts
3. Data export (CSV, PDF)
4. Advanced search and filtering

### Long-term Architecture
1. Web interface (Flask/Django)
2. Cloud database integration
3. Mobile application
4. Bank API integration
5. Analytics and reporting dashboard

## Learning Outcomes

This project demonstrates proficiency in:
- Python programming and modular design
- SQLite database operations
- CLI application development
- Input validation and error handling
- Clean code principles and best practices
- Software architecture and design patterns

## Submission Requirements Met

✅ **Modular Programming**: Separate files for different functions  
✅ **SQLite Database**: Proper table creation and parameterized queries  
✅ **Input Validation**: Numeric validation and exception handling  
✅ **Clean Code**: PEP8 formatting, comments, proper structure  
✅ **Professional Quality**: Error handling, resource management  
✅ **Documentation**: Comprehensive README and code comments  

## Author

**Internship Project** - Python Backend Development  
Demonstrates professional software development skills and best practices.
