"""
Text Log Analyzer CLI Application

This is the main entry point for analyzing logs from text input instead of files.
It provides multiple ways to input log content for analysis.
"""

import sys
import argparse
import json
from text_analyzer import TextLogAnalyzer, get_text_input, analyze_text_content


def create_sample_text() -> str:
    """
    Create sample log content for testing.
    
    Returns:
        str: Sample log content
    """
    return """2023-01-01 10:00:00 INFO: Application started successfully
2023-01-01 10:01:15 INFO: User login: admin
2023-01-01 10:02:30 WARNING: High memory usage detected: 85%
2023-01-01 10:03:45 ERROR: Database connection failed
2023-01-01 10:04:00 ERROR: Database connection failed
2023-01-01 10:05:15 INFO: Retrying database connection
2023-01-01 10:06:30 INFO: Database connection restored
2023-01-01 10:07:45 WARNING: Slow query detected: 2.5 seconds
2023-01-01 10:08:00 INFO: User logout: admin
2023-01-01 10:09:15 ERROR: File not found: /tmp/data.csv
2023-01-01 10:10:30 DEBUG: Cache cleared successfully
2023-01-01 10:11:45 WARNING: Disk space low: 10% remaining
2023-01-01 10:12:00 ERROR: File not found: /tmp/data.csv
2023-01-01 10:13:15 INFO: System backup completed
2023-01-01 10:14:30 ERROR: Authentication failed for user: test
2023-01-01 10:15:45 WARNING: High CPU usage: 90%
2023-01-01 10:16:00 INFO: User login: user1
2023-01-01 10:17:15 ERROR: Authentication failed for user: test
2023-01-01 10:18:30 INFO: Processing batch job: 1000 records
2023-01-01 10:19:45 WARNING: High memory usage detected: 87%"""


def analyze_from_clipboard() -> None:
    """
    Analyze log content from clipboard (if available).
    """
    try:
        import pyperclip
        log_content = pyperclip.paste()
        
        if not log_content.strip():
            print("Clipboard is empty or contains no text.")
            return
        
        print(f"Found {len(log_content)} characters in clipboard.")
        print("Analyzing clipboard content...")
        
        analyze_text_content(log_content, export_json=False)
        
    except ImportError:
        print("pyperclip library is not installed.")
        print("To install it, run: pip install pyperclip")
        print("Then you can use clipboard functionality.")
    except Exception as e:
        print(f"Error reading from clipboard: {e}")


def analyze_from_string(log_content: str) -> None:
    """
    Analyze log content from a string.
    
    Args:
        log_content (str): Log content to analyze
    """
    if not log_content.strip():
        print("Error: Log content is empty.")
        return
    
    analyze_text_content(log_content, export_json=False)


def interactive_text_mode() -> None:
    """
    Interactive mode for text input.
    """
    try:
        log_content = get_text_input()
        
        if not log_content.strip():
            print("No log content provided.")
            return
        
        analyze_text_content(log_content, export_json=False)
        
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
        sys.exit(0)


def main():
    """
    Main function to handle command-line arguments and run the text analyzer.
    """
    parser = argparse.ArgumentParser(
        description='Text Log Analyzer - Analyze logs from text input',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python text_main.py                           # Interactive text input mode
  python text_main.py --sample                  # Analyze sample log content
  python text_main.py --clipboard               # Analyze content from clipboard
  python text_main.py --text "ERROR: Database failed"  # Analyze specific text
  python text_main.py --text "ERROR: Database failed" --export-json  # Export to JSON
        """
    )
    
    parser.add_argument(
        '--text',
        type=str,
        help='Log content to analyze directly (as string)'
    )
    
    parser.add_argument(
        '--sample',
        action='store_true',
        help='Analyze sample log content'
    )
    
    parser.add_argument(
        '--clipboard',
        action='store_true',
        help='Analyze log content from clipboard (requires pyperclip)'
    )
    
    parser.add_argument(
        '--export-json',
        action='store_true',
        help='Export analysis results to JSON format'
    )
    
    parser.add_argument(
        '--json-output',
        type=str,
        help='Custom path for JSON output file (default: text_log_analysis.json)'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version='Text Log Analyzer v1.0.0'
    )
    
    args = parser.parse_args()
    
    # Handle different input modes
    if args.text:
        analyze_text_content(args.text, args.export_json, args.json_output)
    elif args.sample:
        sample_content = create_sample_text()
        analyze_text_content(sample_content, args.export_json, args.json_output)
    elif args.clipboard:
        analyze_from_clipboard()
    else:
        # Default to interactive mode
        interactive_text_mode()


if __name__ == "__main__":
    main()
