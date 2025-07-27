"""
Income Manager Class
Core business logic for Income Recording Client System
"""

import re
import os
from datetime import datetime
from income_item import IncomeItem
from file_handler import FileHandler

class IncomeManager:
    def __init__(self):
        """Initialize income manager"""
        self.income_items = {}  # Dictionary to store income items by code
        self.file_handler = FileHandler()
        self.data_file = "data/income_data.txt"
        self.csv_file = "output/income_sheet.csv"
        
        # Ensure directories exist
        self.ensure_directories()
    
    def ensure_directories(self):
        """Ensure required directories exist"""
        directories = ['data', 'output']
        for directory in directories:
            if not os.path.exists(directory):
                os.makedirs(directory)
                print(f"Created directory: {directory}")
    
    def validate_income_code(self, code):
        """
        Validate income code format
        
        Args:
            code (str): Income code to validate
            
        Returns:
            bool: True if valid, False otherwise
        """
        if not isinstance(code, str):
            return False
        
        code = code.strip().upper()
        pattern = r'^[A-Z]{2}\d{3}$'
        return bool(re.match(pattern, code))
    
    def validate_date(self, date_str):
        """
        Validate date format and values
        
        Args:
            date_str (str): Date string to validate
            
        Returns:
            bool: True if valid, False otherwise
        """
        if not isinstance(date_str, str):
            return False
        
        date_str = date_str.strip()
        
        # Check format DD/MM/YYYY
        pattern = r'^\d{2}/\d{2}/\d{4}$'
        if not re.match(pattern, date_str):
            return False
        
        # Validate actual date
        try:
            day, month, year = map(int, date_str.split('/'))
            datetime(year, month, day)
            return True
        except ValueError:
            return False
    
    def code_exists(self, code):
        """
        Check if income code already exists
        
        Args:
            code (str): Income code to check
            
        Returns:
            bool: True if exists, False otherwise
        """
        return code.upper() in self.income_items
    
    def add_income(self, code, description, date, income_amount, wht_amount):
        """
        Add new income item
        
        Args:
            code (str): Income code
            description (str): Description
            date (str): Date
            income_amount (float): Income amount
            wht_amount (float): WHT amount
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Create new income item (validation happens in constructor)
            income_item = IncomeItem(code, description, date, income_amount, wht_amount)
            
            # Check for duplicate codes
            if self.code_exists(income_item.code):
                print(f"Error: Income code {income_item.code} already exists!")
                return False
            
            # Add to collection
            self.income_items[income_item.code] = income_item
            
            print(f"Income item {income_item.code} added successfully.")
            return True
            
        except ValueError as e:
            print(f"Validation error: {str(e)}")
            return False
        except Exception as e:
            print(f"Error adding income item: {str(e)}")
            return False
    
    def delete_income(self, code):
        """
        Delete income item by code
        
        Args:
            code (str): Income code to delete
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            code = code.upper()
            
            if code in self.income_items:
                del self.income_items[code]
                print(f"Income item {code} deleted successfully.")
                return True
            else:
                print(f"Income item {code} not found.")
                return False
                
        except Exception as e:
            print(f"Error deleting income item: {str(e)}")
            return False
    
    def update_income(self, code, description, date, income_amount, wht_amount):
        """
        Update existing income item
        
        Args:
            code (str): Income code to update
            description (str): New description
            date (str): New date
            income_amount (float): New income amount
            wht_amount (float): New WHT amount
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            code = code.upper()
            
            if code not in self.income_items:
                print(f"Income item {code} not found.")
                return False
            
            # Update the existing item
            self.income_items[code].update(description, date, income_amount, wht_amount)
            
            print(f"Income item {code} updated successfully.")
            return True
            
        except ValueError as e:
            print(f"Validation error: {str(e)}")
            return False
        except Exception as e:
            print(f"Error updating income item: {str(e)}")
            return False
    
    def search_income(self, code):
        """
        Search for income item by code
        
        Args:
            code (str): Income code to search
            
        Returns:
            dict or None: Income item data if found, None otherwise
        """
        try:
            code = code.upper()
            
            if code in self.income_items:
                return self.income_items[code].to_dict()
            else:
                return None
                
        except Exception as e:
            print(f"Error searching income item: {str(e)}")
            return None
    
    def get_all_items(self):
        """
        Get all income items
        
        Returns:
            list: List of all income item dictionaries
        """
        try:
            return [item.to_dict() for item in self.income_items.values()]
        except Exception as e:
            print(f"Error getting all items: {str(e)}")
            return []
    
    def generate_income_sheet(self):
        """
        Generate CSV income sheet with checksums
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if not self.income_items:
                print("No income items to export!")
                return False
            
            # Prepare CSV content
            csv_lines = []
            csv_lines.append("Income_Code,Description,Date,Income_Amount,WHT_Amount,Checksum")
            
            for item in self.income_items.values():
                csv_lines.append(item.to_csv_line())
            
            # Write to file
            success = self.file_handler.write_csv_file(self.csv_file, csv_lines)
            
            if success:
                print(f"Income sheet generated successfully: {self.csv_file}")
                print(f"Total records exported: {len(self.income_items)}")
                return True
            else:
                print("Failed to generate income sheet!")
                return False
                
        except Exception as e:
            print(f"Error generating income sheet: {str(e)}")
            return False
    
    def calculate_total_income(self):
        """Calculate total income amount"""
        return sum(item.income_amount for item in self.income_items.values())
    
    def calculate_total_wht(self):
        """Calculate total WHT amount"""
        return sum(item.wht_amount for item in self.income_items.values())
    
    def calculate_total_net(self):
        """Calculate total net amount"""
        return sum(item.get_net_amount() for item in self.income_items.values())
    
    def get_statistics(self):
        """
        Get income statistics
        
        Returns:
            dict: Statistics dictionary
        """
        try:
            total_items = len(self.income_items)
            total_income = self.calculate_total_income()
            total_wht = self.calculate_total_wht()
            total_net = self.calculate_total_net()
            
            return {
                'total_items': total_items,
                'total_income': round(total_income, 2),
                'total_wht': round(total_wht, 2),
                'total_net': round(total_net, 2),
                'average_income': round(total_income / total_items if total_items > 0 else 0, 2),
                'average_wht': round(total_wht / total_items if total_items > 0 else 0, 2)
            }
        except Exception as e:
            print(f"Error calculating statistics: {str(e)}")
            return {}
    
    def load_data(self):
        """
        Load income data from file
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if not os.path.exists(self.data_file):
                print("No existing data file found. Starting with empty data.")
                return True
            
            lines = self.file_handler.read_data_file(self.data_file)
            
            if lines is None:
                print("Error reading data file!")
                return False
            
            loaded_count = 0
            error_count = 0
            
            for line_num, line in enumerate(lines, 1):
                try:
                    if line.strip():  # Skip empty lines
                        item = IncomeItem.from_file_line(line)
                        self.income_items[item.code] = item
                        loaded_count += 1
                except Exception as e:
                    print(f"Error loading line {line_num}: {str(e)}")
                    error_count += 1
            
            print(f"Data loaded successfully: {loaded_count} items loaded")
            if error_count > 0:
                print(f"Warning: {error_count} lines had errors and were skipped")
            
            return True
            
        except Exception as e:
            print(f"Error loading data: {str(e)}")
            return False
    
    def save_data(self):
        """
        Save income data to file
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Prepare data lines
            data_lines = []
            for item in self.income_items.values():
                data_lines.append(item.to_file_line())
            
            # Write to file
            success = self.file_handler.write_data_file(self.data_file, data_lines)
            
            if success:
                print(f"Data saved successfully: {len(self.income_items)} items saved")
                return True
            else:
                print("Failed to save data!")
                return False
                
        except Exception as e:
            print(f"Error saving data: {str(e)}")
            return False
    
    def backup_data(self, backup_file=None):
        """
        Create backup of current data
        
        Args:
            backup_file (str): Backup file path (optional)
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if backup_file is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                backup_file = f"data/backup_income_data_{timestamp}.txt"
            
            # Prepare data lines
            data_lines = []
            for item in self.income_items.values():
                data_lines.append(item.to_file_line())
            
            # Write backup
            success = self.file_handler.write_data_file(backup_file, data_lines)
            
            if success:
                print(f"Backup created successfully: {backup_file}")
                return True
            else:
                print("Failed to create backup!")
                return False
                
        except Exception as e:
            print(f"Error creating backup: {str(e)}")
            return False
    
    def clear_all_data(self):
        """Clear all income data"""
        try:
            self.income_items.clear()
            print("All income data cleared.")
            return True
        except Exception as e:
            print(f"Error clearing data: {str(e)}")
            return False