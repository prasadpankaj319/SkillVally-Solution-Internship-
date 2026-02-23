# Log Analyzer - Professional Log Analysis Tool

A comprehensive CLI-based log analyzer built with Python that reads log files, analyzes their content, and generates useful summary reports with professional-grade features.

## Features

- **Dual Mode Operation**: Both file-based and text-based analysis
- **Modular Architecture**: Clean separation of concerns with dedicated modules
- **Efficient File Handling**: Memory-efficient line-by-line processing for large log files
- **Comprehensive Analysis**: Counts log entries by level (ERROR, WARNING, INFO, DEBUG)
- **Frequency Analysis**: Identifies most frequent error and warning messages
- **Health Metrics**: Calculates error rates and health scores
- **Multiple Output Formats**: Console reports and JSON export
- **Robust Error Handling**: Handles various edge cases gracefully
- **Interactive & CLI Modes**: Flexible usage options

## Project Structure

```
log_analyzer_new/
├── parser.py          # Log file parsing and validation
├── analyzer.py        # Log analysis and statistics generation
├── main.py            # CLI interface for file-based analysis
├── text_analyzer.py   # Text-based analysis engine
├── text_main.py       # CLI interface for text-based analysis
└── README.md          # This documentation
```

## Installation

### Prerequisites

- Python 3.7 or higher
- No external dependencies required (uses only Python standard library)
- Optional: `pyperclip` for clipboard support

### Setup

1. Clone or download the project
2. Navigate to the `log_analyzer_new` directory
3. Ensure Python is installed and accessible

```bash
cd log_analyzer_new
python --version  # Should be 3.7+
```

Optional: Install clipboard support
```bash
pip install pyperclip
```

## Usage

### File-Based Analysis

#### Interactive Mode
```bash
python main.py
```

#### Command-Line Mode
```bash
python main.py /path/to/your/logfile.log
```

#### Export Results to JSON
```bash
python main.py /path/to/logfile.log --export-json
```

#### Custom JSON Output Path
```bash
python main.py /path/to/logfile.log --export-json --json-output results.json
```

#### Create Sample Log File
```bash
python main.py --create-sample
```

### Text-Based Analysis (No Files Required!)

#### Direct Text Input
```bash
python text_main.py --text "ERROR: Database connection failed
WARNING: High memory usage: 85%
INFO: User login successful
ERROR: File not found
DEBUG: Cache cleared"
```

#### Sample Content
```bash
python text_main.py --sample
```

#### Interactive Text Input
```bash
python text_main.py
# Then type/paste your log content line by line
# Press Enter on empty line to finish
```

#### Clipboard Analysis (requires pyperclip)
```bash
python text_main.py --clipboard
```

#### JSON Export from Text
```bash
python text_main.py --text "ERROR: Database failed" --export-json
```

## Supported Log Formats

The analyzer is flexible and can handle various log formats, including:

```
[2023-01-01 10:00:00] ERROR: Database connection failed
2023-01-01 10:00:00 ERROR Database connection failed
ERROR: Database connection failed
[10:00:00] WARNING: High memory usage detected
INFO: Application started successfully
DEBUG: Cache cleared successfully
```

## Output Examples

### Console Report (File-Based)
```
============================================================
LOG ANALYSIS SUMMARY REPORT
============================================================

File: /path/to/logfile.log
Size: 2.5 MB
Total Lines: 1500

LOG STATISTICS:
  Total Entries: 1450
  ERROR Entries: 45
  WARNING Entries: 120
  INFO Entries: 1250
  DEBUG Entries: 30
  UNKNOWN Entries: 5

DISTRIBUTION PERCENTAGES:
  Error_count: 3.1%
  Warning_count: 8.28%
  Info_count: 86.21%
  Debug_count: 2.07%
  Unknown_count: 0.34%

HEALTH METRICS:
  Error Rate: 3.1%
  Health Score: WARNING

TOP ERROR MESSAGES:
  1. (15 occurrences) Database connection failed
  2. (8 occurrences) File not found: /tmp/data.csv
  3. (5 occurrences) Authentication failed for user: test
============================================================
```

### Console Report (Text-Based)
```
============================================================
LOG ANALYSIS SUMMARY REPORT (TEXT INPUT)
============================================================

Content Information:
  Total Characters: 136
  Total Lines: 5

LOG STATISTICS:
  Total Entries: 5
  ERROR Entries: 2
  WARNING Entries: 1
  INFO Entries: 1
  DEBUG Entries: 1
  UNKNOWN Entries: 0

HEALTH METRICS:
  Error Rate: 40.0%
  Health Score: CRITICAL
```

## Architecture

### 1. Parser Module (`parser.py`)
- **File Validation**: Checks existence, permissions, and readability
- **Efficient Reading**: Memory-efficient line-by-line processing using generators
- **Log Entry Parsing**: Flexible parsing supporting multiple log formats
- **Error Handling**: Comprehensive handling of file-related errors

### 2. Analyzer Module (`analyzer.py`)
- **Statistics Generation**: Real-time counting of log levels
- **Frequency Analysis**: Uses `collections.Counter` for efficient message frequency counting
- **Health Metrics**: Calculates error rates and health scores
- **Export Capabilities**: JSON export with structured data format

### 3. Text Analyzer Module (`text_analyzer.py`)
- **Direct Text Processing**: Analyzes log content without files
- **Same Analysis Power**: Identical capabilities to file-based version
- **Multiple Input Methods**: Supports direct text, interactive input, clipboard
- **Memory Efficient**: Processes text content line by line

### 4. Main Modules (`main.py` & `text_main.py`)
- **CLI Interface**: Both interactive and command-line modes
- **Argument Parsing**: Full argparse implementation with help and version support
- **Sample Generation**: Built-in sample log file/content creation for testing
- **Error Presentation**: User-friendly error messages and guidance

## Log Parsing Logic

The parser uses a sophisticated approach:

1. **Case-Insensitive Detection**: Searches for ERROR, WARNING, INFO, DEBUG patterns
2. **Format Flexibility**: Handles various formats with different separators
3. **Message Extraction**: Intelligently extracts content after log level markers
4. **Fallback Handling**: Processes non-standard formats as UNKNOWN level

## Frequency Counting

Uses Python's `collections.Counter` for optimal performance:

1. **Message Normalization**: Truncates to first 100 characters for effective grouping
2. **Level-Specific Counters**: Separate counters for each log level
3. **Top-N Selection**: Configurable number of most frequent messages
4. **Memory Efficiency**: Counter's optimized storage for large datasets

## Edge Cases Handled

### File Operations
- ✅ **Non-existent files**: Clear error messages with guidance
- ✅ **Permission errors**: Informative permission-related messages
- ✅ **Directory paths**: Handles directory vs file confusion
- ✅ **Empty files**: Graceful handling with warnings

### Content Processing
- ✅ **Empty lines**: Automatically skipped
- ✅ **Malformed entries**: Classified as UNKNOWN level
- ✅ **Encoding issues**: Unicode decode error handling
- ✅ **Large files**: Memory-efficient streaming prevents crashes

### Text Input
- ✅ **Empty content**: Proper validation and user feedback
- ✅ **Keyboard interrupts**: Clean exit during interactive mode
- ✅ **Clipboard errors**: Graceful handling when pyperclip unavailable

## Command-Line Options

### File-Based Analyzer (`main.py`)
```
usage: main.py [-h] [--export-json] [--json-output JSON_OUTPUT] [--create-sample] [--version] [file_path]

Examples:
  python main.py                           # Interactive mode
  python main.py /path/to/logfile.log     # Analyze specific file
  python main.py /path/to/logfile.log --export-json    # Export results to JSON
  python main.py /path/to/logfile.log --json-output results.json  # Custom JSON output
  python main.py --create-sample          # Create sample log file for testing
```

### Text-Based Analyzer (`text_main.py`)
```
usage: text_main.py [-h] [--text TEXT] [--sample] [--clipboard] [--export-json] [--json-output JSON_OUTPUT] [--version]

Examples:
  python text_main.py                           # Interactive text input mode
  python text_main.py --sample                  # Analyze sample log content
  python text_main.py --clipboard               # Analyze content from clipboard
  python text_main.py --text "ERROR: Database failed"  # Analyze specific text
  python text_main.py --text "ERROR: Database failed" --export-json  # Export to JSON
```

## Testing

### Test File-Based Analysis
```bash
# Create sample file
python main.py --create-sample

# Analyze the sample
python main.py sample_log.txt

# Export to JSON
python main.py sample_log.txt --export-json
```

### Test Text-Based Analysis
```bash
# Test with sample content
python text_main.py --sample

# Test with direct text
python text_main.py --text "ERROR: Database failed
WARNING: High memory usage
INFO: User login successful"

# Test interactive mode
python text_main.py
# Then paste your log content
```

## Performance Considerations

- **Memory Usage**: Processes files/text line-by-line to handle large logs efficiently
- **Processing Speed**: Optimized parsing with minimal string operations
- **Scalability**: Suitable for files up to several GB in size
- **Resource Usage**: Low CPU and memory footprint

## Troubleshooting

### Common Issues

1. **Unicode Decode Error**:
   ```
   Solution: Check file encoding or specify different encoding
   ```

2. **Permission Denied**:
   ```
   Solution: Check file permissions or run with appropriate privileges
   ```

3. **Path Issues**:
   ```
   Solution: Use absolute paths or ensure relative paths are correct
   ```

4. **Empty Content**:
   ```
   Solution: Ensure log content has valid log entries with level keywords
   ```

5. **Clipboard Not Working**:
   ```
   Solution: Install pyperclip: pip install pyperclip
   ```

## Enterprise-Level Improvements

For production environments, consider:

### Performance Optimizations
- **Parallel Processing**: Multi-threaded analysis for large files
- **Caching**: Cache analysis results for repeated runs
- **Incremental Analysis**: Process only new log entries
- **Memory Mapping**: Use memory-mapped files for very large logs

### Advanced Features
- **Pattern Recognition**: Regex-based custom pattern matching
- **Time Series Analysis**: Temporal pattern detection and trends
- **Anomaly Detection**: Machine learning-based anomaly identification
- **Correlation Analysis**: Cross-log dependency mapping

### Monitoring & Alerting
- **Real-time Processing**: Tail-mode for live log monitoring
- **Threshold Alerts**: Configurable alert triggers
- **Integration APIs**: REST API for integration with monitoring systems
- **Dashboard Integration**: Grafana/Kibana compatibility

## Contributing

1. Follow PEP8 coding standards
2. Add comprehensive error handling
3. Include docstrings for all functions
4. Test with various log formats
5. Maintain backward compatibility

## License

This project is open source and available under the MIT License.

## Version History

- **v1.0.0**: Initial release with dual-mode functionality
  - File-based log analysis
  - Text-based log analysis (no files required)
  - CLI interface for both modes
  - JSON export
  - Sample content generation
  - Comprehensive error handling
