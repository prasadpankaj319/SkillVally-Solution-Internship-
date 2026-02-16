# CLI Calculator

A professional command-line calculator built with Python, featuring modular design, comprehensive error handling, and a user-friendly interface.

## Features

- **Basic Arithmetic Operations**: Addition, subtraction, multiplication, division
- **Flexible Input Format**: Supports both symbolic (+, -, *, /) and word-based (add, subtract, multiply, divide) operators
- **Robust Error Handling**: Comprehensive input validation and error management
- **User-Friendly Interface**: Interactive CLI with helpful prompts and messages
- **Continuous Operation**: Runs in a loop until user chooses to exit
- **Cross-Platform Compatibility**: Works on Windows, macOS, and Linux

## Project Structure

```
cli_calculator/
├── calculator.py    # Core calculation logic and validation
├── main.py          # CLI interface and main application loop
└── README.md        # Project documentation
```

## Installation & Usage

### Prerequisites
- Python 3.6 or higher

### Running the Calculator

1. Navigate to the project directory:
   ```bash
   cd cli_calculator
   ```

2. Run the application:
   ```bash
   python main.py
   ```

### Usage Examples

#### Basic Operations
```bash
🧮 Enter calculation (or command): 5 + 3
✅ 5 + 3 = 8

🧮 Enter calculation (or command): 10.5 - 2.3
✅ 10.5 - 2.3 = 8.2

🧮 Enter calculation (or command): 4 * 7
✅ 4 * 7 = 28

🧮 Enter calculation (or command): 15 / 3
✅ 15 / 3 = 5
```

#### Word-Based Operators
```bash
🧮 Enter calculation (or command): 8 add 2
✅ 8 add 2 = 10

🧮 Enter calculation (or command): 9 subtract 4
✅ 9 subtract 4 = 5

🧮 Enter calculation (or command): 6 multiply 3
✅ 6 multiply 3 = 18

🧮 Enter calculation (or command): 12 divide 4
✅ 12 divide 4 = 3
```

#### Commands
```bash
🧮 Enter calculation (or command): help
[Shows help information]

🧮 Enter calculation (or command): clear
[Clears the screen]

🧮 Enter calculation (or command): quit
Thank you for using CLI Calculator! Goodbye! 👋
```

## Architecture

### Modular Design

The project follows a clean, modular architecture with clear separation of concerns:

#### `calculator.py` - Core Logic Module
- **Calculator Class**: Contains all mathematical operations
- **Static Methods**: Stateless operations for better performance
- **Input Validation**: Comprehensive validation for numbers and operators
- **Error Handling**: Proper exception handling for edge cases

#### `main.py` - Application Interface
- **CalculatorApp Class**: Manages user interaction and application flow
- **Command Handling**: Processes special commands (help, clear, quit)
- **User Experience**: Provides clear prompts, error messages, and formatting
- **Graceful Exit**: Handles keyboard interrupts and EOF properly

### Key Design Principles

1. **Single Responsibility**: Each class and method has a single, well-defined purpose
2. **Separation of Concerns**: Business logic separated from user interface
3. **Error Resilience**: Comprehensive error handling throughout the application
4. **User Experience**: Clear, helpful messages and intuitive interface
5. **Maintainability**: Clean, well-documented code following PEP8 standards

## Edge Cases Handled

### Input Validation
- **Invalid Number Format**: Non-numeric inputs are rejected with helpful messages
- **Invalid Operators**: Unsupported operators are detected and reported
- **Incorrect Input Format**: Missing or extra components are handled gracefully
- **Empty Input**: Blank entries are ignored without errors

### Mathematical Edge Cases
- **Division by Zero**: Properly caught and reported with clear error message
- **Floating Point Precision**: Results are formatted to avoid floating-point artifacts
- **Large Numbers**: Handles very large and very small numbers appropriately
- **Negative Numbers**: Fully supports negative number operations

### System Edge Cases
- **Keyboard Interrupt (Ctrl+C)**: Gracefully handled with user confirmation
- **EOF (Ctrl+D)**: Cleanly exits the application
- **Unexpected Errors**: Caught and reported without crashing the application

## Error Handling Examples

```bash
🧮 Enter calculation (or command): 5 / 0
❌ Error: Cannot divide by zero!

🧮 Enter calculation (or command): abc + 2
❌ Invalid input format!
   Please use: <number> <operator> <number>
   Example: 5 + 3 or 10 divide 2

🧮 Enter calculation (or command): 5 ^ 2
❌ Invalid input format!
   Please use: <number> <operator> <number>
   Example: 5 + 3 or 10 divide 2
```

## Scaling Improvements

### Immediate Enhancements
1. **Memory Feature**: Store and recall previous calculations
2. **History**: Display calculation history
3. **Constants**: Support for mathematical constants (π, e)
4. **Parentheses**: Support for complex expressions with order of operations
5. **Scientific Functions**: Trigonometric, logarithmic, and exponential functions

### Advanced Features
1. **Unit Conversion**: Convert between different units (length, weight, temperature)
2. **Currency Conversion**: Real-time currency exchange rates
3. **Expression Parser**: Support for complex mathematical expressions
4. **Configuration File**: User preferences and custom settings
5. **Plugin System**: Extensible architecture for custom operations

### Development Improvements
1. **Unit Tests**: Comprehensive test suite for all functions
2. **Logging**: Detailed logging for debugging and monitoring
3. **Package Distribution**: PyPI package for easy installation
4. **Command-line Arguments**: Support for command-line parameters
5. **Configuration Management**: Professional configuration handling

### Performance Optimizations
1. **Caching**: Cache frequently used calculations
2. **Lazy Loading**: Load modules only when needed
3. **Memory Management**: Optimize memory usage for large calculations
4. **Parallel Processing**: Support for batch calculations

## Code Quality

- **PEP8 Compliance**: Follows Python style guidelines
- **Type Hints**: Includes type annotations for better code documentation
- **Docstrings**: Comprehensive documentation for all classes and methods
- **Error Handling**: Robust exception handling throughout
- **Clean Code**: Readable, maintainable, and well-structured code

## Contributing

This project serves as a foundation for learning and development. Feel free to:
- Study the code structure and patterns
- Implement the suggested improvements
- Add new features and functionality
- Report issues or suggest enhancements

## License

This project is open source and available under the MIT License.
