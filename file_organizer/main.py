"""
Main CLI interface for the File Organizer.

This module provides a command-line interface for organizing files
into category-based folders.
"""

import os
import sys
from typing import Optional
from organizer import FileOrganizer


def get_user_input() -> Optional[str]:
    """
    Get directory path from user input.
    
    Returns:
        Optional[str]: Directory path or None if user wants to exit
    """
    print("=== FILE ORGANIZER ===")
    print("Organize your files into category-based folders automatically.\n")
    
    while True:
        directory_path = input("Enter the directory path to organize (or 'exit' to quit): ").strip()
        
        if directory_path.lower() in ['exit', 'quit', 'q']:
            return None
        
        if not directory_path:
            print("Error: Please enter a valid directory path.")
            continue
        
        # Handle relative paths
        if not os.path.isabs(directory_path):
            directory_path = os.path.abspath(directory_path)
        
        return directory_path


def display_menu() -> str:
    """
    Display action menu and get user choice.
    
    Returns:
        str: User's choice
    """
    print("\n=== ACTIONS ===")
    print("1. Organize files")
    print("2. Dry run (preview organization without moving files)")
    print("3. Exit")
    
    while True:
        choice = input("\nEnter your choice (1-3): ").strip()
        if choice in ['1', '2', '3']:
            return choice
        print("Invalid choice. Please enter 1, 2, or 3.")


def confirm_action(action: str) -> bool:
    """
    Get user confirmation before performing action.
    
    Args:
        action (str): Description of the action
        
    Returns:
        bool: True if user confirms, False otherwise
    """
    print(f"\nYou are about to: {action}")
    confirmation = input("Do you want to continue? (y/n): ").strip().lower()
    return confirmation in ['y', 'yes']


def handle_organization(organizer: FileOrganizer, dry_run: bool = False) -> None:
    """
    Handle file organization process.
    
    Args:
        organizer (FileOrganizer): FileOrganizer instance
        dry_run (bool): Whether to perform dry run
    """
    try:
        if dry_run:
            print("\nPerforming dry run...")
            dry_run_results = organizer.dry_run()
            summary = organizer.get_dry_run_summary(dry_run_results)
            print(summary)
        else:
            print("\nOrganizing files...")
            stats = organizer.organize_files()
            summary = organizer.get_organization_summary()
            print(summary)
            
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
    except Exception as e:
        print(f"\nUnexpected error: {e}")


def main():
    """
    Main function to run the File Organizer CLI.
    """
    try:
        # Get directory path from user
        directory_path = get_user_input()
        if directory_path is None:
            print("Goodbye!")
            return
        
        # Create FileOrganizer instance
        try:
            organizer = FileOrganizer(directory_path)
        except ValueError as e:
            print(f"Error: {e}")
            return
        
        print(f"\nSelected directory: {directory_path}")
        
        # Main loop
        while True:
            choice = display_menu()
            
            if choice == '1':  # Organize files
                if confirm_action(f"organize all files in '{directory_path}'"):
                    handle_organization(organizer, dry_run=False)
                else:
                    print("Operation cancelled.")
            
            elif choice == '2':  # Dry run
                handle_organization(organizer, dry_run=True)
            
            elif choice == '3':  # Exit
                print("Goodbye!")
                break
            
            # Ask if user wants to continue
            if choice in ['1', '2']:
                continue_choice = input("\nDo you want to perform another action? (y/n): ").strip().lower()
                if continue_choice not in ['y', 'yes']:
                    print("Goodbye!")
                    break
    
    except KeyboardInterrupt:
        print("\n\nGoodbye!")
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)


def run_with_path(directory_path: str, dry_run: bool = False) -> None:
    """
    Run the organizer with a specific directory path (for scripting).
    
    Args:
        directory_path (str): Directory path to organize
        dry_run (bool): Whether to perform dry run
    """
    try:
        organizer = FileOrganizer(directory_path)
        
        if dry_run:
            print(f"Dry run for directory: {directory_path}")
            dry_run_results = organizer.dry_run()
            summary = organizer.get_dry_run_summary(dry_run_results)
            print(summary)
        else:
            print(f"Organizing directory: {directory_path}")
            stats = organizer.organize_files()
            summary = organizer.get_organization_summary()
            print(summary)
    
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    # Check if command line arguments are provided
    if len(sys.argv) > 1:
        if len(sys.argv) == 2:
            # Run with provided directory path
            run_with_path(sys.argv[1])
        elif len(sys.argv) == 3 and sys.argv[2] in ['--dry-run', '-d']:
            # Run with dry run
            run_with_path(sys.argv[1], dry_run=True)
        else:
            print("Usage:")
            print("  python main.py <directory_path>           # Organize files")
            print("  python main.py <directory_path> --dry-run  # Preview organization")
            sys.exit(1)
    else:
        # Run interactive CLI
        main()
