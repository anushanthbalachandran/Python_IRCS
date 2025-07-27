"""
Income Item Class
Represents a single income record with validation
"""

import re
from datetime import datetime

class IncomeItem:
    def __init__(self, code, description, date, income_amount, wht_amount):
        """
        Initialize an income item with validation
        
        Args:
            code (str): Income code (2 letters + 3 digits)
            description (str): Description (max 20 chars)
            date (str): Date in DD/MM/YYYY format
            income_amount (float): Income amount (positive)
            wht_amount (float): Withholding tax amount (non-negative)
        """
        self.code = self.validate_and_set_code(code)
        self.description = self.validate_and_set_description(description)
        self.date = self.validate_and_set_date(date)
        self.income_amount = self.validate_and_set_income_amount(income_amount)
        self.wht_amount = self.validate_and_set_wht_amount(wht_amount)
    
    def validate_and_set_code(self, code):
        """Validate and set income code"""
        if not isinstance(code, str):
            raise ValueError("Income code must be a string")
        
        code = code.strip().upper()
        
        # Check format: 2 letters + 3 digits
        pattern = r'^[A-Z]{2}\d{3}$'
        if not re.match(pattern, code):
            raise ValueError("Income code must be 2 letters followed by 3 digits (e.g., IN001)")
        
        return code
    
    def validate_and_set_description(self, description):
        """Validate and set description"""
        if not isinstance(description, str):
            raise ValueError("Description must be a string")
        
        description = description.strip()
        
        if len(description) == 0:
            raise ValueError("Description cannot be empty")
        
        if len(description) > 20:
            raise ValueError("Description cannot exceed 20 characters")
        
        return description
    
    def validate_and_set_date(self, date):
        """Validate and set date"""
        if not isinstance(date, str):
            raise ValueError("Date must be a string")
        
        date = date.strip()
        
        # Check format DD/MM/YYYY
        pattern = r'^\d{2}/\d{2}/\d{4}$'
        if not re.match(pattern, date):
            raise ValueError("Date must be in DD/MM/YYYY format")
        
        # Validate actual date
        try:
            day, month, year = map(int, date.split('/'))
            datetime(year, month, day)
        except ValueError:
            raise ValueError("Invalid date values")
        
        return date
    
    def validate_and_set_income_amount(self, amount):
        """Validate and set income amount"""
        try:
            amount = float(amount)
        except (ValueError, TypeError):
            raise ValueError("Income amount must be a valid number")
        
        if amount <= 0:
            raise ValueError("Income amount must be positive")
        
        return round(amount, 2)
    
    def validate_and_set_wht_amount(self, amount):
        """Validate and set withholding tax amount"""
        try:
            amount = float(amount)
        except (ValueError, TypeError):
            raise ValueError("WHT amount must be a valid number")
        
        if amount < 0:
            raise ValueError("WHT amount cannot be negative")
        
        return round(amount, 2)
    
    def get_net_amount(self):
        """Calculate net amount after WHT"""
        return round(self.income_amount - self.wht_amount, 2)
    
    def to_dict(self):
        """Convert to dictionary representation"""
        return {
            'code': self.code,
            'description': self.description,
            'date': self.date,
            'income_amount': self.income_amount,
            'wht_amount': self.wht_amount,
            'net_amount': self.get_net_amount()
        }
    
    def to_csv_line(self):
        """Convert to CSV line format with checksum"""
        # Create CSV line without checksum first
        csv_line = f"{self.code},{self.description},{self.date},{self.income_amount:.2f},{self.wht_amount:.2f}"
        
        # Calculate checksum
        checksum = self.calculate_checksum(csv_line)
        
        # Return complete CSV line with checksum
        return f"{csv_line},{checksum}"
    
    def calculate_checksum(self, line):
        """
        Calculate checksum for a transaction line
        
        Algorithm:
        1. Count all capital letters only
        2. Count all numbers and decimals
        3. Sum the two counts
        
        Args:
            line (str): The transaction line
            
        Returns:
            int: Checksum value
        """
        capital_count = sum(1 for char in line if char.isupper())
        number_decimal_count = sum(1 for char in line if char.isdigit() or char == '.')
        
        return capital_count + number_decimal_count
    
    def to_file_line(self):
        """Convert to file storage format (pipe-delimited)"""
        return f"{self.code}|{self.description}|{self.date}|{self.income_amount:.2f}|{self.wht_amount:.2f}"
    
    @classmethod
    def from_file_line(cls, line):
        """Create IncomeItem from file line"""
        try:
            parts = line.strip().split('|')
            if len(parts) != 5:
                raise ValueError("Invalid file line format")
            
            code, description, date, income_str, wht_str = parts
            income_amount = float(income_str)
            wht_amount = float(wht_str)
            
            return cls(code, description, date, income_amount, wht_amount)
            
        except (ValueError, IndexError) as e:
            raise ValueError(f"Error parsing file line: {str(e)}")
    
    @classmethod
    def from_csv_line(cls, line):
        """Create IncomeItem from CSV line (with or without checksum)"""
        try:
            parts = line.strip().split(',')
            if len(parts) < 5:
                raise ValueError("Invalid CSV line format")
            
            code = parts[0]
            description = parts[1]
            date = parts[2]
            income_amount = float(parts[3])
            wht_amount = float(parts[4])
            
            return cls(code, description, date, income_amount, wht_amount)
            
        except (ValueError, IndexError) as e:
            raise ValueError(f"Error parsing CSV line: {str(e)}")
    
    def update(self, description=None, date=None, income_amount=None, wht_amount=None):
        """Update income item fields"""
        if description is not None:
            self.description = self.validate_and_set_description(description)
        
        if date is not None:
            self.date = self.validate_and_set_date(date)
        
        if income_amount is not None:
            self.income_amount = self.validate_and_set_income_amount(income_amount)
        
        if wht_amount is not None:
            self.wht_amount = self.validate_and_set_wht_amount(wht_amount)
    
    def __str__(self):
        """String representation"""
        return (f"IncomeItem(code={self.code}, description={self.description}, "
                f"date={self.date}, income={self.income_amount:.2f}, "
                f"wht={self.wht_amount:.2f}, net={self.get_net_amount():.2f})")
    
    def __repr__(self):
        """Detailed representation"""
        return self.__str__()
    
    def __eq__(self, other):
        """Equality comparison based on code"""
        if not isinstance(other, IncomeItem):
            return False
        return self.code == other.code
    
    def __hash__(self):
        """Hash based on code"""
        return hash(self.code)