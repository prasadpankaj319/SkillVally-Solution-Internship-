"""
Log Analyzer CLI Application

This is the main entry point for the Log Analyzer CLI application.
It provides a command-line interface for analyzing log files.
"""

import sys
import argparse
import json
from pathlib import Path
from parser import LogParser
from analyzer import LogAnalyzer


def get_user_input() -> str:
    """
    Get log file path from user input.
    
    Returns:
        str: Path to the log file
    """
    print("Log Analyzer - Professional Log Analysis Tool")
    print("=" * 50)
    
    while True:
        file_path = input("Enter the path to your log file (or 'quit' to exit): ").strip()
        
        if file_path.lower() in ['quit', 'exit', 'q']:
            print("Goodbye!")
            sys.exit(0)
        
        if not file_path:
            print("Error: Please enter a valid file path.")
            continue
        
        # Handle different path formats
        try:
            # Convert to absolute path but handle errors gracefully
            path_obj = Path(file_path)
            if not path_obj.is_absolute():
                # If relative, make it absolute relative to current directory
                file_path = str(Path.cwd() / file_path)
            else:
                file_path = str(path_obj)
            
            # Test if file exists
            if Path(file_path).exists():
                return file_path
            else:
                print(f"Error: File not found at '{file_path}'")
                print("Please check the path and try again.")
                
        except Exception as e:
            print(f"Error processing path '{file_path}': {e}")
            print("Please enter a valid file path.")


def analyze_log_file(file_path: str, export_json: bool = False, json_output: str = None) -> None:
    """
    Analyze a log file and display results.
    
    Args:
        file_path (str): Path to the log file
        export_json (bool): Whether to export results to JSON
        json_output (str): Path for JSON output file
    """
    try:
        # Initialize parser and analyzer
        parser = LogParser(file_path)
        analyzer = LogAnalyzer(parser)
        
        print(f"\nAnalyzing log file: {file_path}")
        print("Please wait...")
        
        # Perform analysis
        analysis_results = analyzer.analyze_logs()
        
        # Display summary report
        summary_report = analyzer.generate_summary_report(analysis_results)
        print(summary_report)
        
        # Export to JSON if requested
        if export_json:
            export_data = analyzer.export_to_dict(analysis_results)
            
            if json_output:
                # Handle custom JSON output path
                output_path_obj = Path(json_output)
                if not output_path_obj.is_absolute():
                    output_path = str(Path.cwd() / json_output)
                else:
                    output_path = str(output_path_obj)
            else:
                # Generate default output filename in current directory
                input_path = Path(file_path)
                output_path = str(Path.cwd() / f"{input_path.stem}_analysis.json")
            
            try:
                with open(output_path, 'w', encoding='utf-8') as f:
                    json.dump(export_data, f, indent=2, ensure_ascii=False)
                print(f"\nAnalysis results exported to: {output_path}")
            except Exception as e:
                print(f"Error exporting to JSON: {e}")
        
        return analysis_results
        
    except FileNotFoundError as e:
        print(f"Error: {e}")
        print("Please check if the file path is correct and the file exists.")
    except PermissionError as e:
        print(f"Error: {e}")
        print("Please check if you have read permissions for the file.")
    except UnicodeDecodeError as e:
        print(f"Error: {e}")
        print("The file might be encoded in a different format. Try specifying encoding.")
    except Exception as e:
        print(f"Unexpected error: {e}")
        print("Please check the file format and try again.")


def create_sample_log_file() -> None:
    """
    Create a sample log file for testing purposes.
    """
    sample_content = """2023-01-01 10:00:00 INFO: Application started successfully
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
2023-01-01 10:19:45 WARNING: High memory usage detected: 87%
"""
    
    try:
        with open('sample_log.txt', 'w', encoding='utf-8') as f:
            f.write(sample_content)
        print("Sample log file 'sample_log.txt' created successfully!")
        print("You can now analyze this file to test the application.")
    except Exception as e:
        print(f"Error creating sample file: {e}")


def main():
    """
    Main function to handle command-line arguments and run the application.
    """
    parser = argparse.ArgumentParser(
        description='Professional Log Analyzer - Analyze log files and generate reports',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py                           # Interactive mode
  python main.py /path/to/logfile.log     # Analyze specific file
  python main.py /path/to/logfile.log --export-json    # Export results to JSON
  python main.py /path/to/logfile.log --json-output results.json  # Custom JSON output
  python main.py --create-sample          # Create sample log file for testing
        """
    )
    
    parser.add_argument(
        'file_path',
        nargs='?',
        help='Path to the log file to analyze'
    )
    
    parser.add_argument(
        '--export-json',
        action='store_true',
        help='Export analysis results to JSON format'
    )
    
    parser.add_argument(
        '--json-output',
        type=str,
        help='Custom path for JSON output file (default: auto-generated)'
    )
    
    parser.add_argument(
        '--create-sample',
        action='store_true',
        help='Create a sample log file for testing'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version='Log Analyzer v1.0.0'
    )
    
    args = parser.parse_args()
    
    # Handle sample file creation
    if args.create_sample:
        create_sample_log_file()
        return
    
    # Interactive mode if no file path provided
    if not args.file_path:
        try:
            file_path = get_user_input()
        except KeyboardInterrupt:
            print("\n\nOperation cancelled by user.")
            sys.exit(0)
        
        analyze_log_file(file_path, args.export_json, args.json_output)
    else:
        # Command-line mode
        try:
            path_obj = Path(args.file_path)
            if not path_obj.is_absolute():
                # If relative, make it absolute relative to current directory
                file_path = str(Path.cwd() / args.file_path)
            else:
                file_path = str(path_obj)
            
            analyze_log_file(file_path, args.export_json, args.json_output)
        except Exception as e:
            print(f"Error processing file path '{args.file_path}': {e}")
            sys.exit(1)


if __name__ == "__main__":
    main()
