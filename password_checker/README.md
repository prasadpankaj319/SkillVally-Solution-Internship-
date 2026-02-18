# Password Strength Checker

A professional CLI-based Password Strength Checker built with Python using modular programming principles and clean code practices.

## Features

- **Password Validation**: Validates passwords against security requirements
- **Strength Analysis**: Calculates password strength with detailed scoring
- **Interactive CLI**: User-friendly command-line interface
- **Secure Input**: Uses `getpass` for secure password entry
- **Detailed Feedback**: Provides specific recommendations for improvement

## Project Structure

```
password_checker/
├── validator.py    # Password validation logic
├── checker.py      # Strength calculation logic
├── main.py         # CLI interface and main application
└── README.md       # This documentation
```

## Requirements

- Python 3.6 or higher
- No external dependencies (uses only Python standard library)

## Installation

1. Clone or download the project
2. Navigate to the `password_checker` directory
3. Run the application:

```bash
python main.py
```

## Usage

### Basic Usage

1. Run the application: `python main.py`
2. Enter a password when prompted
3. View the validation and strength results
4. Choose to check another password or exit

### Example Session

```
============================================================
    PASSWORD STRENGTH CHECKER - Professional Edition
============================================================

This tool helps you evaluate the strength of your passwords.
Your password will not be stored or transmitted anywhere.

Validation Requirements:
• Minimum 8 characters
• At least 1 uppercase letter
• At least 1 lowercase letter
• At least 1 digit
• At least 1 special character

============================================================

Enter a password to check (or type 'exit' to quit):
Password: ********

----------------------------------------
PASSWORD INFORMATION
----------------------------------------
Length: 12 characters
Character Breakdown:
  • Uppercase: 3
  • Lowercase: 6
  • Digits: 2
  • Special: 1

----------------------------------------
VALIDATION RESULTS
----------------------------------------
✓ Length (8+ chars): ✓
✓ Uppercase letter: ✓
✓ Lowercase letter: ✓
✓ Digit: ✓
✓ Special character: ✓

✅ All validation requirements met!

----------------------------------------
STRENGTH ANALYSIS
----------------------------------------
Strength Rating: 🟢 Strong (82%)

Detailed Scores:
  • Length Score: 80%
  • Variety Score: 100%
  • Complexity Score: 73%

🎉 Excellent password! No improvements needed.
```

## Validation Rules

The password validator checks for the following requirements:

1. **Minimum Length**: At least 8 characters
2. **Uppercase Letters**: At least one uppercase letter (A-Z)
3. **Lowercase Letters**: At least one lowercase letter (a-z)
4. **Digits**: At least one digit (0-9)
5. **Special Characters**: At least one special character (!@#$%^&*()_+-=[]{};:"\\|,.<>/?)

## Strength Scoring Algorithm

The password strength is calculated using three main factors:

### 1. Length Score (30% weight)
- < 8 characters: 0%
- 8-10 characters: 30%
- 11-12 characters: 60%
- 13-16 characters: 80%
- > 16 characters: 100%

### 2. Variety Score (40% weight)
Based on character variety:
- Uppercase letters: 25%
- Lowercase letters: 25%
- Digits: 25%
- Special characters: 25%

### 3. Complexity Score (30% weight)
- Base score: 100%
- Penalty: -30% for 3+ repeating characters
- Penalty: -20% for sequential characters
- Bonus: +10% for mixed case
- Bonus: +10% for numbers + special characters

### Strength Categories
- **Weak**: Score < 40%
- **Medium**: Score 40-69%
- **Strong**: Score ≥ 70%

## Module Documentation

### validator.py

Contains the `PasswordValidator` class responsible for:
- Validating password requirements
- Providing detailed error messages
- Checking individual validation rules
- Generating validation summaries

Key methods:
- `is_valid(password)`: Check if password passes all validations
- `get_validation_errors(password)`: Get detailed error messages
- `get_validation_summary(password)`: Get validation results for each rule

### checker.py

Contains the `PasswordStrengthChecker` class responsible for:
- Calculating password strength scores
- Categorizing password strength
- Providing improvement recommendations
- Analyzing password complexity

Key methods:
- `calculate_overall_score(password)`: Calculate overall strength score
- `get_strength_category(score)`: Get strength category
- `get_strength_details(password)`: Get detailed strength analysis
- `get_strength_recommendations(password)`: Get improvement suggestions

### main.py

Contains the `PasswordCheckerApp` class responsible for:
- CLI interface and user interaction
- Secure password input handling
- Displaying results in a user-friendly format
- Managing application flow

Key methods:
- `run_interactive_mode()`: Main application loop
- `display_validation_results(password)`: Show validation results
- `display_strength_results(password)`: Show strength analysis

## Edge Cases Handled

1. **Empty Input**: Handles empty password input gracefully
2. **Keyboard Interrupt**: Properly handles Ctrl+C interruptions
3. **Invalid Characters**: Accepts all Unicode characters
4. **Very Long Passwords**: Efficiently handles long passwords
5. **Exit Commands**: Recognizes 'exit', 'quit', 'n', 'no' to exit
6. **Input Errors**: Catches and handles input-related exceptions

## Security Considerations

- Passwords are not stored or logged
- Uses `getpass` to prevent password echo in terminal
- No network connections or external API calls
- All processing happens locally
- Passwords are cleared from memory after processing

## Real-World Scaling Improvements

For production use, consider these enhancements:

### 1. Database Integration
```python
# Example database integration
class DatabasePasswordChecker:
    def __init__(self, db_connection):
        self.db = db_connection
        self.validator = PasswordValidator()
        self.strength_checker = PasswordStrengthChecker()
    
    def check_password_for_user(self, user_id, password):
        # Check against breached passwords database
        if self.is_breached_password(password):
            return False, "Password found in breached data"
        
        # Standard validation and strength check
        # ... existing logic
```

### 2. Advanced Security Features
- **Breach Detection**: Check against known breached password databases
- **Dictionary Attacks**: Check against common password dictionaries
- **Rate Limiting**: Prevent brute force attacks
- **Password History**: Prevent password reuse
- **Multi-factor Authentication**: Integration with 2FA systems

### 3. Performance Optimizations
- **Caching**: Cache validation results for repeated checks
- **Async Processing**: Handle multiple password checks concurrently
- **Batch Processing**: Process multiple passwords at once
- **Memory Optimization**: Efficient handling of large password datasets

### 4. API Integration
```python
# Example REST API integration
from flask import Flask, request, jsonify

app = Flask(__name__)
password_checker = PasswordCheckerApp()

@app.route('/api/check-password', methods=['POST'])
def check_password_api():
    data = request.get_json()
    password = data.get('password')
    
    if not password:
        return jsonify({'error': 'Password required'}), 400
    
    results = password_checker.strength_checker.get_strength_details(password)
    return jsonify(results)
```

### 5. Configuration Management
```python
# Example configuration system
import yaml

class ConfigurablePasswordChecker:
    def __init__(self, config_file='config.yaml'):
        with open(config_file) as f:
            self.config = yaml.safe_load(f)
        
        self.validator = PasswordValidator(
            min_length=self.config['validation']['min_length']
        )
```

## Database Authentication System Integration

### 1. User Registration Flow
```python
def register_user(username, password, email):
    # Validate password strength
    checker = PasswordStrengthChecker()
    details = checker.get_strength_details(password)
    
    if not details['is_valid']:
        return False, "Password does not meet requirements"
    
    if details['category'] == 'Weak':
        return False, "Password is too weak"
    
    # Hash password with strong algorithm (bcrypt, Argon2, etc.)
    hashed_password = hash_password(password)
    
    # Store in database
    user_id = create_user_in_db(username, hashed_password, email)
    return True, "User registered successfully"
```

### 2. Password Change Flow
```python
def change_password(user_id, current_password, new_password):
    # Verify current password
    if not verify_user_password(user_id, current_password):
        return False, "Current password is incorrect"
    
    # Validate new password
    checker = PasswordStrengthChecker()
    details = checker.get_strength_details(new_password)
    
    if not details['is_valid']:
        return False, "New password does not meet requirements"
    
    # Check password history
    if is_password_reused(user_id, new_password):
        return False, "Password has been used before"
    
    # Update password
    update_user_password(user_id, hash_password(new_password))
    return True, "Password changed successfully"
```

### 3. Authentication System Integration
```python
class AuthenticationSystem:
    def __init__(self):
        self.password_checker = PasswordStrengthChecker()
        self.max_attempts = 5
        self.lockout_duration = 300  # 5 minutes
    
    def authenticate_user(self, username, password):
        # Rate limiting check
        if self.is_account_locked(username):
            return False, "Account temporarily locked"
        
        # Verify password
        if verify_user_password(username, password):
            self.reset_failed_attempts(username)
            return True, "Authentication successful"
        else:
            self.record_failed_attempt(username)
            return False, "Invalid credentials"
```

## Testing

The application includes comprehensive error handling and edge case management. To test the application:

1. **Test Valid Passwords**: Try passwords that meet all requirements
2. **Test Invalid Passwords**: Try passwords missing various requirements
3. **Test Edge Cases**: Empty input, very long passwords, special characters
4. **Test CLI Features**: Exit commands, keyboard interrupts

Example test cases:
- `Password123!` - Should pass all validations
- `weak` - Should fail multiple validations
- `NoSpecialChar123` - Should fail special character requirement
- `EMPTY` - Should handle empty input gracefully

## Contributing

When contributing to this project:
1. Follow PEP8 formatting standards
2. Add appropriate comments and documentation
3. Test your changes thoroughly
4. Maintain the modular architecture
5. Consider security implications

## License

This project is provided as educational code. Feel free to use and modify it for learning purposes.

## Support

For issues or questions about this Password Strength Checker, please refer to the code documentation or create an issue in the project repository.
