"""
Unit Tests for Income Recording Client System
Tests core functionality of IncomeItem and IncomeManager classes
"""

import unittest
import os
import sys
import tempfile
import shutil

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from income_item import IncomeItem
from income_manager import IncomeManager
from file_handler import FileHandler

class TestIncomeItem(unittest.TestCase):
    """Test cases for IncomeItem class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.valid_code = "IN001"
        self.valid_description = "Freelance Work"
        self.valid_date = "25/07/2025"
        self.valid_income = 10000.00
        self.valid_wht = 1000.00
    
    def test_valid_income_item_creation(self):
        """Test creating a valid income item"""
        item = IncomeItem(
            self.valid_code,
            self.valid_description,
            self.valid_date,
            self.valid_income,
            self.valid_wht
        )
        
        self.assertEqual(item.code, self.valid_code)
        self.assertEqual(item.description, self.valid_description)
        self.assertEqual(item.date, self.valid_date)
        self.assertEqual(item.income_amount, self.valid_income)
        self.assertEqual(item.wht_amount, self.valid_wht)
        self.assertEqual(item.get_net_amount(), 9000.00)
    
    def test_invalid_income_code_format(self):
        """Test invalid income code formats"""
        invalid_codes = ["IN1", "ABC123", "1N001", "IN01", "INA01", "123AB"]
        
        for code in invalid_codes:
            with self.assertRaises(ValueError):
                IncomeItem(code, self.valid_description, self.valid_date, 
                          self.valid_income, self.valid_wht)
    
    def test_invalid_description_length(self):
        """Test invalid description lengths"""
        # Empty description
        with self.assertRaises(ValueError):
            IncomeItem(self.valid_code, "", self.valid_date, 
                      self.valid_income, self.valid_wht)
        
        # Too long description
        long_description = "This is a very long description that exceeds twenty characters"
        with self.assertRaises(ValueError):
            IncomeItem(self.valid_code, long_description, self.valid_date, 
                      self.valid_income, self.valid_wht)
    
    def test_invalid_date_formats(self):
        """Test invalid date formats"""
        invalid_dates = ["25-07-2025", "2025/07/25", "25/7/2025", "abc", "32/12/2025"]
        
        for date in invalid_dates:
            with self.assertRaises(ValueError):
                IncomeItem(self.valid_code, self.valid_description, date, 
                          self.valid_income, self.valid_wht)
    
    def test_invalid_amounts(self):
        """Test invalid income and WHT amounts"""
        # Negative income
        with self.assertRaises(ValueError):
            IncomeItem(self.valid_code, self.valid_description, self.valid_date, 
                      -1000, self.valid_wht)
        
        # Zero income
        with self.assertRaises(ValueError):
            IncomeItem(self.valid_code, self.valid_description, self.valid_date, 
                      0, self.valid_wht)
        
        # Negative WHT
        with self.assertRaises(ValueError):
            IncomeItem(self.valid_code, self.valid_description, self.valid_date, 
                      self.valid_income, -100)
    
    def test_checksum_calculation(self):
        """Test checksum calculation algorithm"""
        item = IncomeItem(self.valid_code, self.valid_description, self.valid_date, 
                         self.valid_income, self.valid_wht)
        
        # Test checksum for known string
        test_line = "IN001,Freelance Work,25/07/2025,10000.00,1000.00"
        checksum = item.calculate_checksum(test_line)
        
        # Count capitals: I, N, F, W = 4
        # Count numbers/decimals: 0,0,1,2,5,0,7,2,0,2,5,1,0,0,0,0,.,0,0,1,0,0,0,.,0,0 = 26
        # Total should be 4 + 26 = 30
        expected_checksum = 30
        self.assertEqual(checksum, expected_checksum)
    
    def test_csv_line_generation(self):
        """Test CSV line generation with checksum"""
        item = IncomeItem(self.valid_code, self.valid_description, self.valid_date, 
                         self.valid_income, self.valid_wht)
        
        csv_line = item.to_csv_line()
        parts = csv_line.split(',')
        
        self.assertEqual(len(parts), 6)  # Should have 6 parts including checksum
        self.assertEqual(parts[0], self.valid_code)
        self.assertEqual(parts[1], self.valid_description)
        self.assertEqual(parts[2], self.valid_date)
        self.assertEqual(float(parts[3]), self.valid_income)
        self.assertEqual(float(parts[4]), self.valid_wht)
        self.assertTrue(parts[5].isdigit())  # Checksum should be numeric
    
    def test_file_line_conversion(self):
        """Test file line conversion (pipe-delimited)"""
        item = IncomeItem(self.valid_code, self.valid_description, self.valid_date, 
                         self.valid_income, self.valid_wht)
        
        file_line = item.to_file_line()
        expected = f"{self.valid_code}|{self.valid_description}|{self.valid_date}|{self.valid_income:.2f}|{self.valid_wht:.2f}"
        self.assertEqual(file_line, expected)
    
    def test_from_file_line_creation(self):
        """Test creating IncomeItem from file line"""
        file_line = f"{self.valid_code}|{self.valid_description}|{self.valid_date}|{self.valid_income:.2f}|{self.valid_wht:.2f}"
        item = IncomeItem.from_file_line(file_line)
        
        self.assertEqual(item.code, self.valid_code)
        self.assertEqual(item.description, self.valid_description)
        self.assertEqual(item.date, self.valid_date)
        self.assertEqual(item.income_amount, self.valid_income)
        self.assertEqual(item.wht_amount, self.valid_wht)

class TestIncomeManager(unittest.TestCase):
    """Test cases for IncomeManager class"""
    
    def setUp(self):
        """Set up test fixtures"""
        # Create temporary directory for testing
        self.test_dir = tempfile.mkdtemp()
        self.original_cwd = os.getcwd()
        os.chdir(self.test_dir)
        
        # Create manager instance
        self.manager = IncomeManager()
        
        # Test data
        self.test_items = [
            ("IN001", "Freelance Work", "25/07/2025", 10000.00, 1000.00),
            ("SA002", "Consulting", "26/07/2025", 15000.00, 1500.00),
            ("WK003", "Part-time Job", "27/07/2025", 8000.00, 0.00)
        ]
    
    def tearDown(self):
        """Clean up test fixtures"""
        os.chdir(self.original_cwd)
        shutil.rmtree(self.test_dir)
    
    def test_add_income_items(self):
        """Test adding income items"""
        for code, desc, date, income, wht in self.test_items:
            result = self.manager.add_income(code, desc, date, income, wht)
            self.assertTrue(result)
            self.assertTrue(self.manager.code_exists(code))
    
    def test_duplicate_code_prevention(self):
        """Test prevention of duplicate codes"""
        code, desc, date, income, wht = self.test_items[0]
        
        # Add first item
        result1 = self.manager.add_income(code, desc, date, income, wht)
        self.assertTrue(result1)
        
        # Try to add duplicate
        result2 = self.manager.add_income(code, "Different Desc", date, income, wht)
        self.assertFalse(result2)
    
    def test_search_income(self):
        """Test searching for income items"""
        # Add test item
        code, desc, date, income, wht = self.test_items[0]
        self.manager.add_income(code, desc, date, income, wht)
        
        # Search for existing item
        result = self.manager.search_income(code)
        self.assertIsNotNone(result)
        self.assertEqual(result['code'], code)
        self.assertEqual(result['description'], desc)
        
        # Search for non-existing item
        result_none = self.manager.search_income("XX999")
        self.assertIsNone(result_none)
    
    def test_update_income(self):
        """Test updating income items"""
        # Add test item
        code, desc, date, income, wht = self.test_items[0]
        self.manager.add_income(code, desc, date, income, wht)
        
        # Update item
        new_desc = "Updated Description"
        new_income = 12000.00
        result = self.manager.update_income(code, new_desc, date, new_income, wht)
        self.assertTrue(result)
        
        # Verify update
        updated_item = self.manager.search_income(code)
        self.assertEqual(updated_item['description'], new_desc)
        self.assertEqual(updated_item['income_amount'], new_income)
    
    def test_delete_income(self):
        """Test deleting income items"""
        # Add test item
        code, desc, date, income, wht = self.test_items[0]
        self.manager.add_income(code, desc, date, income, wht)
        self.assertTrue(self.manager.code_exists(code))
        
        # Delete item
        result = self.manager.delete_income(code)
        self.assertTrue(result)
        self.assertFalse(self.manager.code_exists(code))
        
        # Try to delete non-existing item
        result_false = self.manager.delete_income("XX999")
        self.assertFalse(result_false)
    
    def test_income_code_validation(self):
        """Test income code validation"""
        valid_codes = ["IN001", "AB123", "XY999"]
        invalid_codes = ["123AB", "A1234", "ABC12", "1N001", "INA01"]
        
        for code in valid_codes:
            self.assertTrue(self.manager.validate_income_code(code))
        
        for code in invalid_codes:
            self.assertFalse(self.manager.validate_income_code(code))
    
    def test_date_validation(self):
        """Test date validation"""
        valid_dates = ["01/01/2025", "29/02/2024", "31/12/2025"]  # 2024 is leap year
        invalid_dates = ["1/1/2025", "32/01/2025", "29/02/2025", "01/13/2025", "abc"]
        
        for date in valid_dates:
            self.assertTrue(self.manager.validate_date(date))
        
        for date in invalid_dates:
            self.assertFalse(self.manager.validate_date(date))
    
    def test_statistics_calculation(self):
        """Test statistics calculation"""
        # Add test items
        for code, desc, date, income, wht in self.test_items:
            self.manager.add_income(code, desc, date, income, wht)
        
        stats = self.manager.get_statistics()
        
        expected_total_income = sum(item[3] for item in self.test_items)
        expected_total_wht = sum(item[4] for item in self.test_items)
        expected_total_net = expected_total_income - expected_total_wht
        
        self.assertEqual(stats['total_items'], len(self.test_items))
        self.assertEqual(stats['total_income'], expected_total_income)
        self.assertEqual(stats['total_wht'], expected_total_wht)
        self.assertEqual(stats['total_net'], expected_total_net)
    
    def test_csv_generation(self):
        """Test CSV generation"""
        # Add test items
        for code, desc, date, income, wht in self.test_items:
            self.manager.add_income(code, desc, date, income, wht)
        
        # Generate CSV
        result = self.manager.generate_income_sheet()
        self.assertTrue(result)
        
        # Check if file exists
        self.assertTrue(os.path.exists(self.manager.csv_file))
        
        # Read and verify content
        with open(self.manager.csv_file, 'r') as file:
            lines = file.readlines()
        
        # Should have header + data lines
        self.assertEqual(len(lines), len(self.test_items) + 1)
        
        # Check header
        header = lines[0].strip()
        self.assertIn("Income_Code", header)
        self.assertIn("Checksum", header)

class TestFileHandler(unittest.TestCase):
    """Test cases for FileHandler class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.test_dir = tempfile.mkdtemp()
        self.original_cwd = os.getcwd()
        os.chdir(self.test_dir)
        
        self.file_handler = FileHandler()
        self.test_file = "test_data.txt"
        self.test_csv = "test_data.csv"
    
    def tearDown(self):
        """Clean up test fixtures"""
        os.chdir(self.original_cwd)
        shutil.rmtree(self.test_dir)
    
    def test_write_and_read_data_file(self):
        """Test writing and reading data file"""
        test_data = [
            "IN001|Freelance Work|25/07/2025|10000.00|1000.00",
            "SA002|Consulting|26/07/2025|15000.00|1500.00"
        ]
        
        # Write data
        result_write = self.file_handler.write_data_file(self.test_file, test_data)
        self.assertTrue(result_write)
        
        # Read data
        result_read = self.file_handler.read_data_file(self.test_file)
        self.assertIsNotNone(result_read)
        self.assertEqual(len(result_read), len(test_data))
        self.assertEqual(result_read, test_data)
    
    def test_write_and_read_csv_file(self):
        """Test writing and reading CSV file"""
        csv_data = [
            "Income_Code,Description,Date,Income_Amount,WHT_Amount,Checksum",
            "IN001,Freelance Work,25/07/2025,10000.00,1000.00,30"
        ]
        
        # Write CSV
        result_write = self.file_handler.write_csv_file(self.test_csv, csv_data)
        self.assertTrue(result_write)
        
        # Read CSV
        result_read = self.file_handler.read_csv_file(self.test_csv)
        self.assertIsNotNone(result_read)
        self.assertEqual(len(result_read), len(csv_data))
    
    def test_file_operations(self):
        """Test various file operations"""
        test_data = ["Test line 1", "Test line 2"]
        
        # Write file
        self.file_handler.write_data_file(self.test_file, test_data)
        
        # Check if file exists
        self.assertTrue(self.file_handler.file_exists(self.test_file))
        
        # Get file size
        size = self.file_handler.get_file_size(self.test_file)
        self.assertIsNotNone(size)
        self.assertGreater(size, 0)
        
        # Get modification time
        mod_time = self.file_handler.get_file_modification_time(self.test_file)
        self.assertIsNotNone(mod_time)

if __name__ == '__main__':
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add test cases
    test_suite.addTest(unittest.makeSuite(TestIncomeItem))
    test_suite.addTest(unittest.makeSuite(TestIncomeManager))
    test_suite.addTest(unittest.makeSuite(TestFileHandler))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Print summary
    print(f"\n{'='*50}")
    print(f"UNIT TEST SUMMARY")
    print(f"{'='*50}")
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    if result.failures:
        print(f"\nFAILURES:")
        for test, failure in result.failures:
            print(f"- {test}: {failure}")
    
    if result.errors:
        print(f"\nERRORS:")
        for test, error in result.errors:
            print(f"- {test}: {error}")
    
    if result.wasSuccessful():
        print(f"\n✅ All tests passed successfully!")
    else:
        print(f"\n❌ Some tests failed. Please review the issues above.")
    
    print(f"{'='*50}")