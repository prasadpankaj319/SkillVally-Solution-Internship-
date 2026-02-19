"""
Utility functions for file organizer.

This module contains helper functions for file categorization,
validation, and common operations.
"""

import os
from typing import Dict, List, Optional


def get_file_categories() -> Dict[str, str]:
    """
    Returns a dictionary mapping file extensions to categories.
    
    Returns:
        Dict[str, str]: Mapping of file extensions to category names
    """
    return {
        # Images
        '.jpg': 'Images',
        '.jpeg': 'Images',
        '.png': 'Images',
        '.gif': 'Images',
        '.bmp': 'Images',
        '.tiff': 'Images',
        '.webp': 'Images',
        '.svg': 'Images',
        '.ico': 'Images',
        
        # Documents
        '.pdf': 'Documents',
        '.doc': 'Documents',
        '.docx': 'Documents',
        '.txt': 'Documents',
        '.rtf': 'Documents',
        '.odt': 'Documents',
        '.xls': 'Documents',
        '.xlsx': 'Documents',
        '.ppt': 'Documents',
        '.pptx': 'Documents',
        '.csv': 'Documents',
        
        # Videos
        '.mp4': 'Videos',
        '.avi': 'Videos',
        '.mkv': 'Videos',
        '.mov': 'Videos',
        '.wmv': 'Videos',
        '.flv': 'Videos',
        '.webm': 'Videos',
        '.m4v': 'Videos',
        
        # Audio
        '.mp3': 'Audio',
        '.wav': 'Audio',
        '.flac': 'Audio',
        '.aac': 'Audio',
        '.ogg': 'Audio',
        '.wma': 'Audio',
        
        # Archives
        '.zip': 'Archives',
        '.rar': 'Archives',
        '.7z': 'Archives',
        '.tar': 'Archives',
        '.gz': 'Archives',
        
        # Code
        '.py': 'Code',
        '.js': 'Code',
        '.html': 'Code',
        '.css': 'Code',
        '.java': 'Code',
        '.cpp': 'Code',
        '.c': 'Code',
        '.php': 'Code',
        '.rb': 'Code',
        '.go': 'Code',
        '.rs': 'Code',
        
        # Executables
        '.exe': 'Executables',
        '.msi': 'Executables',
        '.deb': 'Executables',
        '.dmg': 'Executables',
        '.app': 'Executables',
    }


def get_file_category(file_extension: str) -> str:
    """
    Determines the category for a given file extension.
    
    Args:
        file_extension (str): File extension (e.g., '.jpg', '.pdf')
        
    Returns:
        str: Category name or 'Others' if not found
    """
    categories = get_file_categories()
    return categories.get(file_extension.lower(), 'Others')


def validate_directory_path(path: str) -> bool:
    """
    Validates if the given path exists and is a directory.
    
    Args:
        path (str): Directory path to validate
        
    Returns:
        bool: True if path exists and is a directory, False otherwise
    """
    return os.path.exists(path) and os.path.isdir(path)


def get_files_in_directory(directory_path: str) -> List[str]:
    """
    Gets all files in the specified directory (excluding subdirectories).
    
    Args:
        directory_path (str): Path to the directory
        
    Returns:
        List[str]: List of file names in the directory
        
    Raises:
        OSError: If there's an error reading the directory
    """
    try:
        files = []
        for item in os.listdir(directory_path):
            item_path = os.path.join(directory_path, item)
            if os.path.isfile(item_path):
                files.append(item)
        return files
    except OSError as e:
        raise OSError(f"Error reading directory {directory_path}: {e}")


def get_unique_filename(destination_path: str) -> str:
    """
    Generates a unique filename if the original already exists.
    
    Args:
        destination_path (str): Full path where file should be moved
        
    Returns:
        str: Unique filename path
    """
    if not os.path.exists(destination_path):
        return destination_path
    
    base, extension = os.path.splitext(destination_path)
    counter = 1
    
    while True:
        new_path = f"{base}_{counter}{extension}"
        if not os.path.exists(new_path):
            return new_path
        counter += 1


def format_file_size(size_bytes: int) -> str:
    """
    Formats file size in human-readable format.
    
    Args:
        size_bytes (int): File size in bytes
        
    Returns:
        str: Formatted file size string
    """
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    
    return f"{size_bytes:.1f} {size_names[i]}"


def is_hidden_file(file_path: str) -> bool:
    """
    Checks if a file is hidden (starts with dot on Unix systems).
    
    Args:
        file_path (str): Path to the file
        
    Returns:
        bool: True if file is hidden, False otherwise
    """
    filename = os.path.basename(file_path)
    return filename.startswith('.')
