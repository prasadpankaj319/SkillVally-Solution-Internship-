"""
Log Parser Module

This module handles file validation and log reading operations.
It provides efficient file reading capabilities with proper error handling.
"""

import os
from typing import Iterator, List, Optional


class LogParser:
    """
    A class for parsing and reading log files efficiently.
    
    Attributes:
        file_path (str): Path to the log file
        encoding (str): File encoding (default: utf-8)
    """
    
    def __init__(self, file_path: str, encoding: str = 'utf-8'):
        """
        Initialize the LogParser with file path and encoding.
        
        Args:
            file_path (str): Path to the log file
            encoding (str): File encoding (default: utf-8)
        """
        self.file_path = file_path
        self.encoding = encoding
    
    def validate_file(self) -> bool:
        """
        Validate if the file exists and is readable.
        
        Returns:
            bool: True if file is valid, False otherwise
            
        Raises:
            FileNotFoundError: If file doesn't exist
            PermissionError: If file is not readable
            IsADirectoryError: If path is a directory
        """
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"Log file not found: {self.file_path}")
        
        if not os.path.isfile(self.file_path):
            raise IsADirectoryError(f"Path is a directory, not a file: {self.file_path}")
        
        if not os.access(self.file_path, os.R_OK):
            raise PermissionError(f"No read permission for file: {self.file_path}")
        
        # Check if file is empty
        if os.path.getsize(self.file_path) == 0:
            print(f"Warning: File is empty - {self.file_path}")
        
        return True
    
    def read_lines(self) -> Iterator[str]:
        """
        Read log file line by line efficiently.
        
        Yields:
            str: Each line from the log file
            
        Raises:
            UnicodeDecodeError: If file encoding is incorrect
            IOError: If there's an error reading the file
        """
        try:
            with open(self.file_path, 'r', encoding=self.encoding) as file:
                for line in file:
                    yield line.strip()
        except UnicodeDecodeError:
            raise UnicodeDecodeError(
                f"Unable to decode file {self.file_path} with encoding {self.encoding}"
            )
        except IOError as e:
            raise IOError(f"Error reading file {self.file_path}: {e}")
    
    def get_file_info(self) -> dict:
        """
        Get basic information about the log file.
        
        Returns:
            dict: File information including size and line count
        """
        if not self.validate_file():
            return {}
        
        file_size = os.path.getsize(self.file_path)
        line_count = 0
        
        try:
            for _ in self.read_lines():
                line_count += 1
        except Exception:
            # If we can't read lines, just return what we have
            pass
        
        return {
            'path': self.file_path,
            'size_bytes': file_size,
            'size_mb': round(file_size / (1024 * 1024), 2),
            'line_count': line_count
        }
    
    def parse_log_entry(self, line: str) -> Optional[dict]:
        """
        Parse a single log entry into structured format.
        
        Args:
            line (str): A single line from the log file
            
        Returns:
            Optional[dict]: Parsed log entry or None if line is empty/invalid
        """
        if not line.strip():
            return None
        
        # Basic log format detection
        # Supports formats like: [2023-01-01 10:00:00] ERROR: Message here
        # Or: 2023-01-01 10:00:00 ERROR Message here
        # Or: ERROR: Message here
        
        log_entry = {
            'raw_line': line,
            'level': None,
            'message': None,
            'timestamp': None
        }
        
        # Convert to uppercase for case-insensitive matching
        upper_line = line.upper()
        
        # Detect log level
        if 'ERROR' in upper_line:
            log_entry['level'] = 'ERROR'
        elif 'WARNING' in upper_line or 'WARN' in upper_line:
            log_entry['level'] = 'WARNING'
        elif 'INFO' in upper_line:
            log_entry['level'] = 'INFO'
        elif 'DEBUG' in upper_line:
            log_entry['level'] = 'DEBUG'
        else:
            log_entry['level'] = 'UNKNOWN'
        
        # Extract message (everything after the log level)
        level_pos = upper_line.find(log_entry['level'])
        if level_pos != -1:
            # Find the message after the level
            message_start = level_pos + len(log_entry['level'])
            # Skip common separators like ':', '-', '|'
            message = line[message_start:].strip()
            if message.startswith((':', '-', '|')):
                message = message[1:].strip()
            log_entry['message'] = message
        
        return log_entry
