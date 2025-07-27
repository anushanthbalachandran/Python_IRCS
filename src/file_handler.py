"""
File Handler Class
Handles all file operations for the Income Recording Client System
"""

import os
import csv
import shutil
from datetime import datetime

class FileHandler:
    def __init__(self):
        """Initialize file handler"""
        self.encoding = 'utf-8'
    
    def ensure_directory_exists(self, file_path):
        """
        Ensure the directory for a file path exists
        
        Args:
            file_path (str): File path
        """
        directory = os.path.dirname(file_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)
            print(f"Created directory: {directory}")
    
    def read_data_file(self, file_path):
        """
        Read data from pipe-delimited text file
        
        Args:
            file_path (str): Path to data file
            
        Returns:
            list or None: List of lines if successful, None if error
        """
        try:
            if not os.path.exists(file_path):
                print(f"File not found: {file_path}")
                return []
            
            with open(file_path, 'r', encoding=self.encoding) as file:
                lines = file.readlines()
            
            # Remove newline characters and filter empty lines
            lines = [line.strip() for line in lines if line.strip()]
            
            print(f"Successfully read {len(lines)} lines from {file_path}")
            return lines
            
        except IOError as e:
            print(f"IO Error reading file {file_path}: {str(e)}")
            return None
        except UnicodeDecodeError as e:
            print(f"Encoding error reading file {file_path}: {str(e)}")
            return None
        except Exception as e:
            print(f"Unexpected error reading file {file_path}: {str(e)}")
            return None
    
    def write_data_file(self, file_path, data_lines):
        """
        Write data to pipe-delimited text file
        
        Args:
            file_path (str): Path to data file
            data_lines (list): List of data lines to write
            
        Returns:
            bool: True if successful, False if error
        """
        try:
            # Ensure directory exists
            self.ensure_directory_exists(file_path)
            
            with open(file_path, 'w', encoding=self.encoding) as file:
                for line in data_lines:
                    file.write(line + '\n')
            
            print(f"Successfully wrote {len(data_lines)} lines to {file_path}")
            return True
            
        except IOError as e:
            print(f"IO Error writing file {file_path}: {str(e)}")
            return False
        except Exception as e:
            print(f"Unexpected error writing file {file_path}: {str(e)}")
            return False
    
    def read_csv_file(self, file_path):
        """
        Read CSV file
        
        Args:
            file_path (str): Path to CSV file
            
        Returns:
            list or None: List of rows if successful, None if error
        """
        try:
            if not os.path.exists(file_path):
                print(f"CSV file not found: {file_path}")
                return None
            
            rows = []
            with open(file_path, 'r', encoding=self.encoding, newline='') as file:
                csv_reader = csv.reader(file)
                for row in csv_reader:
                    rows.append(row)
            
            print(f"Successfully read {len(rows)} rows from CSV: {file_path}")
            return rows
            
        except IOError as e:
            print(f"IO Error reading CSV file {file_path}: {str(e)}")
            return None
        except csv.Error as e:
            print(f"CSV Error reading file {file_path}: {str(e)}")
            return None
        except Exception as e:
            print(f"Unexpected error reading CSV file {file_path}: {str(e)}")
            return None
    
    def write_csv_file(self, file_path, csv_lines):
        """
        Write CSV file
        
        Args:
            file_path (str): Path to CSV file
            csv_lines (list): List of CSV lines to write
            
        Returns:
            bool: True if successful, False if error
        """
        try:
            # Ensure directory exists
            self.ensure_directory_exists(file_path)
            
            with open(file_path, 'w', encoding=self.encoding, newline='') as file:
                for line in csv_lines:
                    file.write(line + '\n')
            
            print(f"Successfully wrote {len(csv_lines)} lines to CSV: {file_path}")
            return True
            
        except IOError as e:
            print(f"IO Error writing CSV file {file_path}: {str(e)}")
            return False
        except Exception as e:
            print(f"Unexpected error writing CSV file {file_path}: {str(e)}")
            return False
    
    def write_csv_with_writer(self, file_path, rows, headers=None):
        """
        Write CSV file using csv.writer
        
        Args:
            file_path (str): Path to CSV file
            rows (list): List of rows to write
            headers (list): Optional headers
            
        Returns:
            bool: True if successful, False if error
        """
        try:
            # Ensure directory exists
            self.ensure_directory_exists(file_path)
            
            with open(file_path, 'w', encoding=self.encoding, newline='') as file:
                csv_writer = csv.writer(file)
                
                # Write headers if provided
                if headers:
                    csv_writer.writerow(headers)
                
                # Write data rows
                for row in rows:
                    csv_writer.writerow(row)
            
            total_rows = len(rows) + (1 if headers else 0)
            print(f"Successfully wrote {total_rows} rows to CSV: {file_path}")
            return True
            
        except IOError as e:
            print(f"IO Error writing CSV file {file_path}: {str(e)}")
            return False
        except csv.Error as e:
            print(f"CSV Error writing file {file_path}: {str(e)}")
            return False
        except Exception as e:
            print(f"Unexpected error writing CSV file {file_path}: {str(e)}")
            return False
    
    def copy_file(self, source_path, destination_path):
        """
        Copy file from source to destination
        
        Args:
            source_path (str): Source file path
            destination_path (str): Destination file path
            
        Returns:
            bool: True if successful, False if error
        """
        try:
            if not os.path.exists(source_path):
                print(f"Source file not found: {source_path}")
                return False
            
            # Ensure destination directory exists
            self.ensure_directory_exists(destination_path)
            
            shutil.copy2(source_path, destination_path)
            print(f"Successfully copied {source_path} to {destination_path}")
            return True
            
        except IOError as e:
            print(f"IO Error copying file: {str(e)}")
            return False
        except Exception as e:
            print(f"Unexpected error copying file: {str(e)}")
            return False
    
    def delete_file(self, file_path):
        """
        Delete file
        
        Args:
            file_path (str): File path to delete
            
        Returns:
            bool: True if successful, False if error
        """
        try:
            if not os.path.exists(file_path):
                print(f"File not found: {file_path}")
                return True  # Consider it successful if file doesn't exist
            
            os.remove(file_path)
            print(f"Successfully deleted file: {file_path}")
            return True
            
        except IOError as e:
            print(f"IO Error deleting file {file_path}: {str(e)}")
            return False
        except Exception as e:
            print(f"Unexpected error deleting file {file_path}: {str(e)}")
            return False
    
    def file_exists(self, file_path):
        """
        Check if file exists
        
        Args:
            file_path (str): File path to check
            
        Returns:
            bool: True if exists, False otherwise
        """
        return os.path.exists(file_path)
    
    def get_file_size(self, file_path):
        """
        Get file size in bytes
        
        Args:
            file_path (str): File path
            
        Returns:
            int or None: File size in bytes if successful, None if error
        """
        try:
            if not os.path.exists(file_path):
                return None
            
            return os.path.getsize(file_path)
            
        except Exception as e:
            print(f"Error getting file size for {file_path}: {str(e)}")
            return None
    
    def get_file_modification_time(self, file_path):
        """
        Get file modification time
        
        Args:
            file_path (str): File path
            
        Returns:
            datetime or None: Modification time if successful, None if error
        """
        try:
            if not os.path.exists(file_path):
                return None
            
            timestamp = os.path.getmtime(file_path)
            return datetime.fromtimestamp(timestamp)
            
        except Exception as e:
            print(f"Error getting modification time for {file_path}: {str(e)}")
            return None
    
    def create_backup(self, file_path, backup_suffix="_backup"):
        """
        Create backup of a file
        
        Args:
            file_path (str): Original file path
            backup_suffix (str): Suffix for backup file
            
        Returns:
            str or None: Backup file path if successful, None if error
        """
        try:
            if not os.path.exists(file_path):
                print(f"Original file not found: {file_path}")
                return None
            
            # Generate backup file path
            name, ext = os.path.splitext(file_path)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = f"{name}{backup_suffix}_{timestamp}{ext}"
            
            # Copy file
            if self.copy_file(file_path, backup_path):
                return backup_path
            else:
                return None
                
        except Exception as e:
            print(f"Error creating backup for {file_path}: {str(e)}")
            return None
    
    def validate_file_format(self, file_path, expected_extension):
        """
        Validate file format by extension
        
        Args:
            file_path (str): File path to validate
            expected_extension (str): Expected extension (e.g., '.csv', '.txt')
            
        Returns:
            bool: True if valid format, False otherwise
        """
        try:
            _, ext = os.path.splitext(file_path.lower())
            return ext == expected_extension.lower()
        except Exception:
            return False
    
    def get_safe_filename(self, filename):
        """
        Create safe filename by removing/replacing invalid characters
        
        Args:
            filename (str): Original filename
            
        Returns:
            str: Safe filename
        """
        try:
            # Remove or replace invalid characters
            invalid_chars = '<>:"/\\|?*'
            safe_filename = filename
            
            for char in invalid_chars:
                safe_filename = safe_filename.replace(char, '_')
            
            # Remove leading/trailing spaces and dots
            safe_filename = safe_filename.strip(' .')
            
            # Ensure filename is not empty
            if not safe_filename:
                safe_filename = "unnamed_file"
            
            return safe_filename
            
        except Exception:
            return "unnamed_file"