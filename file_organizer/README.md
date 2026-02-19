# File Organizer

A professional CLI-based File Organizer that automatically organizes files in a directory into category-based folders.

## Features

- **Automatic File Categorization**: Files are organized into folders based on their extensions
- **Duplicate File Handling**: Safely handles duplicate filenames by appending numbers
- **Dry Run Mode**: Preview organization before actually moving files
- **Error Handling**: Comprehensive error handling with detailed error messages
- **Hidden File Support**: Option to skip or include hidden files
- **Interactive CLI**: User-friendly command-line interface
- **Scriptable**: Can be used in scripts with command-line arguments

## Project Structure

```
file_organizer/
├── main.py          # Main CLI interface
├── organizer.py     # Core file organization logic
├── utils.py         # Utility functions and helpers
└── README.md        # This file
```

## Installation

No external dependencies required. The organizer uses only Python standard library modules:
- `os` - File system operations
- `shutil` - High-level file operations
- `sys` - System-specific parameters and functions

## Usage

### Interactive Mode

Run the organizer in interactive mode:

```bash
python main.py
```

Follow the prompts to:
1. Enter the directory path to organize
2. Choose an action (organize files, dry run, or exit)
3. Confirm the action

### Command Line Mode

Organize files directly:

```bash
python main.py /path/to/directory
```

Preview organization without moving files:

```bash
python main.py /path/to/directory --dry-run
# or
python main.py /path/to/directory -d
```

## File Categories

The organizer automatically creates the following category folders:

| Category | File Extensions |
|----------|-----------------|
| **Images** | .jpg, .jpeg, .png, .gif, .bmp, .tiff, .webp, .svg, .ico |
| **Documents** | .pdf, .doc, .docx, .txt, .rtf, .odt, .xls, .xlsx, .ppt, .pptx, .csv |
| **Videos** | .mp4, .avi, .mkv, .mov, .wmv, .flv, .webm, .m4v |
| **Audio** | .mp3, .wav, .flac, .aac, .ogg, .wma |
| **Archives** | .zip, .rar, .7z, .tar, .gz |
| **Code** | .py, .js, .html, .css, .java, .cpp, .c, .php, .rb, .go, .rs |
| **Executables** | .exe, .msi, .deb, .dmg, .app |
| **Others** | All other file extensions |

## Example Output

### Dry Run
```
=== DRY RUN SUMMARY ===
Directory: /Users/username/Downloads

Audio (2 files):
  - song1.mp3
  - podcast.wav

Images (5 files):
  - photo1.jpg
  - screenshot.png
  - ... and 3 more files

Total files to be organized: 7

Note: This is a dry run. No files were actually moved.
```

### Organization
```
Created folder: Images
Created folder: Audio
Moved: photo1.jpg -> Images/
Moved: screenshot.png -> Images/
Moved: song1.mp3 -> Audio/
Moved: podcast.wav -> Audio/

=== ORGANIZATION SUMMARY ===
Directory: /Users/username/Downloads

Audio: 2 files
Images: 5 files

Total files organized: 7
```

## Architecture

### 1. **utils.py** - Utility Functions
- `get_file_categories()`: Returns mapping of file extensions to categories
- `get_file_category()`: Determines category for a given file extension
- `validate_directory_path()`: Validates directory path existence
- `get_files_in_directory()`: Lists all files in a directory
- `get_unique_filename()`: Handles duplicate filenames
- `format_file_size()`: Formats file sizes in human-readable format
- `is_hidden_file()`: Checks if a file is hidden

### 2. **organizer.py** - Core Logic
- `FileOrganizer` class: Main organizer implementation
- `organize_files()`: Main method to organize files
- `dry_run()`: Preview mode without moving files
- `create_category_folders()`: Creates necessary category folders
- `_move_file_to_category()`: Handles individual file moves
- `get_organization_summary()`: Generates operation summary

### 3. **main.py** - CLI Interface
- Interactive menu system
- Command-line argument parsing
- User input validation
- Error handling and user feedback

## File Categorization Logic

The categorization works as follows:

1. **Extension Extraction**: Extract file extension using `os.path.splitext()`
2. **Case Normalization**: Convert extension to lowercase for consistent matching
3. **Category Lookup**: Use dictionary mapping to find category
4. **Default Category**: Files with unknown extensions go to "Others" folder

## Duplicate File Handling

When duplicate filenames are encountered:

1. **Check Existence**: Verify if target filename already exists
2. **Generate Unique Name**: Append counter number to base filename
3. **Increment Counter**: Continue incrementing until unique name found
4. **Example**: `document.pdf` → `document_1.pdf` → `document_2.pdf`

## Edge Cases Handled

- **Invalid Directory Path**: Validates path exists and is a directory
- **Empty Directory**: Handles gracefully with appropriate message
- **Permission Errors**: Catches and reports file system permission issues
- **Hidden Files**: Option to skip hidden files (starting with '.')
- **File Locks**: Handles cases where files are in use
- **Disk Space**: Reports errors when disk is full
- **Network Paths**: Works with network drives (if accessible)
- **Special Characters**: Handles filenames with special characters

## Error Handling

The organizer implements comprehensive error handling:

- **Input Validation**: Validates user inputs and directory paths
- **File System Errors**: Catches OS-level errors during file operations
- **Graceful Degradation**: Continues processing other files if one fails
- **Error Reporting**: Provides detailed error messages and summaries
- **User Feedback**: Keeps users informed of progress and issues

## Enterprise-Level Improvements

To scale this for enterprise usage:

### 1. **Configuration Management**
- External configuration files for custom categories
- User-defined file type mappings
- Organization rule templates

### 2. **Logging and Monitoring**
- Structured logging with different levels
- Audit trails for file movements
- Performance metrics and monitoring

### 3. **Multi-threading**
- Parallel file processing for large directories
- Progress tracking with threading
- Resource management and limits

### 4. **Database Integration**
- Store file metadata in database
- Track file history and movements
- Enable search and reporting features

### 5. **Network Support**
- Handle network file systems
- Remote directory organization
- Cloud storage integration (AWS S3, Azure Blob)

### 6. **Security Features**
- File permissions handling
- Access control integration
- File integrity verification

### 7. **Advanced Features**
- File content analysis (not just extension)
- Duplicate file detection by content
- Automated cleanup rules
- Scheduled organization tasks

## GUI Conversion

To convert this CLI tool into a GUI application:

### 1. **GUI Framework Options**
- **Tkinter**: Built-in Python GUI library
- **PyQt/PySide**: Professional GUI framework
- **Kivy**: Cross-platform GUI
- **Electron + Python**: Web-based GUI

### 2. **Key GUI Components**
- Directory selection dialog
- File preview panel
- Progress bar for operations
- Category configuration interface
- Real-time status updates

### 3. **Implementation Steps**
```python
# Example using Tkinter
import tkinter as tk
from tkinter import filedialog, messagebox
from organizer import FileOrganizer

class FileOrganizerGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.setup_ui()
    
    def setup_ui(self):
        # Create GUI elements
        # Directory selector
        # Category configuration
        # Progress tracking
        # Results display
        pass
    
    def organize_files(self):
        # Handle file organization with GUI updates
        pass
```

## Automation Script Integration

### 1. **Scheduled Tasks**
- Windows Task Scheduler
- Linux cron jobs
- macOS launchd

### 2. **Script Integration**
```python
# Example automation script
from organizer import FileOrganizer
import schedule
import time

def organize_downloads():
    organizer = FileOrganizer("/Users/username/Downloads")
    organizer.organize_files()

# Schedule daily organization
schedule.every().day.at("02:00").do(organize_downloads)

while True:
    schedule.run_pending()
    time.sleep(60)
```

### 3. **System Service**
- Create Windows Service
- Linux systemd service
- macOS launch agent

## Contributing

1. Follow PEP8 coding standards
2. Add comprehensive tests
3. Update documentation
4. Handle edge cases
5. Maintain backward compatibility

## License

This project is open source and available under the MIT License.

## Support

For issues and questions:
1. Check the error messages carefully
2. Verify directory permissions
3. Ensure sufficient disk space
4. Test with dry run mode first

---

**Note**: Always test with the dry run mode first to ensure the organizer will behave as expected before performing actual file movements.
