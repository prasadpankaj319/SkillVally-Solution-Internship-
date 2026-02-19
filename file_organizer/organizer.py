"""
Core file organizer module.

This module contains the main FileOrganizer class that handles
the logic for organizing files into categories.
"""

import os
import shutil
from typing import Dict, List, Tuple
from utils import (
    get_file_category,
    validate_directory_path,
    get_files_in_directory,
    get_unique_filename,
    is_hidden_file
)


class FileOrganizer:
    """
    A class to organize files in a directory into category-based folders.
    """
    
    def __init__(self, directory_path: str):
        """
        Initialize the FileOrganizer.
        
        Args:
            directory_path (str): Path to the directory to organize
            
        Raises:
            ValueError: If the directory path is invalid
        """
        if not validate_directory_path(directory_path):
            raise ValueError(f"Invalid directory path: {directory_path}")
        
        self.directory_path = directory_path
        self.organization_stats = {}
        self.errors = []
    
    def create_category_folders(self) -> None:
        """
        Create category folders if they don't exist.
        """
        categories = self._get_all_categories()
        
        for category in categories:
            category_path = os.path.join(self.directory_path, category)
            try:
                if not os.path.exists(category_path):
                    os.makedirs(category_path)
                    print(f"Created folder: {category}")
            except OSError as e:
                error_msg = f"Failed to create folder {category}: {e}"
                self.errors.append(error_msg)
                print(f"Warning: {error_msg}")
    
    def organize_files(self, skip_hidden: bool = True) -> Dict[str, int]:
        """
        Organize files into their respective category folders.
        
        Args:
            skip_hidden (bool): Whether to skip hidden files
            
        Returns:
            Dict[str, int]: Statistics of organized files by category
        """
        try:
            files = get_files_in_directory(self.directory_path)
        except OSError as e:
            self.errors.append(str(e))
            print(f"Error: {e}")
            return {}
        
        if not files:
            print("No files found in the directory.")
            return {}
        
        # Create category folders first
        self.create_category_folders()
        
        # Initialize statistics
        self.organization_stats = {}
        files_processed = 0
        
        for filename in files:
            try:
                # Skip hidden files if requested
                if skip_hidden and is_hidden_file(filename):
                    continue
                
                file_path = os.path.join(self.directory_path, filename)
                file_extension = os.path.splitext(filename)[1].lower()
                category = get_file_category(file_extension)
                
                # Move file to category folder
                success = self._move_file_to_category(file_path, filename, category)
                
                if success:
                    # Update statistics
                    self.organization_stats[category] = self.organization_stats.get(category, 0) + 1
                    files_processed += 1
                    print(f"Moved: {filename} -> {category}/")
                
            except Exception as e:
                error_msg = f"Error processing {filename}: {e}"
                self.errors.append(error_msg)
                print(f"Error: {error_msg}")
        
        return self.organization_stats
    
    def _move_file_to_category(self, file_path: str, filename: str, category: str) -> bool:
        """
        Move a file to its category folder.
        
        Args:
            file_path (str): Full path to the source file
            filename (str): Name of the file
            category (str): Target category folder name
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            category_path = os.path.join(self.directory_path, category)
            destination_path = os.path.join(category_path, filename)
            
            # Handle duplicate filenames
            unique_destination = get_unique_filename(destination_path)
            
            # Move the file
            shutil.move(file_path, unique_destination)
            
            # If filename was changed due to duplicate, show the new name
            if unique_destination != destination_path:
                new_filename = os.path.basename(unique_destination)
                print(f"  Renamed to: {new_filename} (duplicate handled)")
            
            return True
            
        except (OSError, shutil.Error) as e:
            error_msg = f"Failed to move {filename} to {category}: {e}"
            self.errors.append(error_msg)
            return False
    
    def _get_all_categories(self) -> List[str]:
        """
        Get all possible categories including 'Others'.
        
        Returns:
            List[str]: List of all category names
        """
        from utils import get_file_categories
        categories = set(get_file_categories().values())
        categories.add('Others')
        return sorted(list(categories))
    
    def get_organization_summary(self) -> str:
        """
        Generate a summary of the organization process.
        
        Returns:
            str: Formatted summary string
        """
        if not self.organization_stats:
            return "No files were organized."
        
        summary_lines = ["\n=== ORGANIZATION SUMMARY ==="]
        summary_lines.append(f"Directory: {self.directory_path}")
        summary_lines.append("")
        
        total_files = 0
        for category, count in sorted(self.organization_stats.items()):
            summary_lines.append(f"{category}: {count} files")
            total_files += count
        
        summary_lines.append(f"\nTotal files organized: {total_files}")
        
        if self.errors:
            summary_lines.append(f"\nErrors encountered: {len(self.errors)}")
            for error in self.errors[:5]:  # Show first 5 errors
                summary_lines.append(f"  - {error}")
            if len(self.errors) > 5:
                summary_lines.append(f"  ... and {len(self.errors) - 5} more errors")
        
        return "\n".join(summary_lines)
    
    def dry_run(self, skip_hidden: bool = True) -> Dict[str, List[str]]:
        """
        Perform a dry run to show what would be organized without actually moving files.
        
        Args:
            skip_hidden (bool): Whether to skip hidden files
            
        Returns:
            Dict[str, List[str]]: Mapping of categories to files that would be moved
        """
        try:
            files = get_files_in_directory(self.directory_path)
        except OSError as e:
            self.errors.append(str(e))
            return {}
        
        dry_run_results = {}
        
        for filename in files:
            if skip_hidden and is_hidden_file(filename):
                continue
            
            file_extension = os.path.splitext(filename)[1].lower()
            category = get_file_category(file_extension)
            
            if category not in dry_run_results:
                dry_run_results[category] = []
            dry_run_results[category].append(filename)
        
        return dry_run_results
    
    def get_dry_run_summary(self, dry_run_results: Dict[str, List[str]]) -> str:
        """
        Generate a summary of the dry run results.
        
        Args:
            dry_run_results (Dict[str, List[str]]): Results from dry_run method
            
        Returns:
            str: Formatted dry run summary
        """
        if not dry_run_results:
            return "No files found to organize."
        
        summary_lines = ["\n=== DRY RUN SUMMARY ==="]
        summary_lines.append(f"Directory: {self.directory_path}")
        summary_lines.append("")
        
        total_files = 0
        for category, files in sorted(dry_run_results.items()):
            summary_lines.append(f"{category} ({len(files)} files):")
            for filename in files[:3]:  # Show first 3 files per category
                summary_lines.append(f"  - {filename}")
            if len(files) > 3:
                summary_lines.append(f"  ... and {len(files) - 3} more files")
            total_files += len(files)
            summary_lines.append("")
        
        summary_lines.append(f"Total files to be organized: {total_files}")
        summary_lines.append("\nNote: This is a dry run. No files were actually moved.")
        
        return "\n".join(summary_lines)
