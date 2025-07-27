"""
Income Recording Client System (IRCS)
Main Application Entry Point
"""

import sys

from income_manager import IncomeManager


class IRCSApplication:
    def __init__(self):
        self.manager = IncomeManager()
        self.running = True
    
    def display_menu(self):
        """Display the main menu options"""
        print("\n" + "*"*50)
        print("   INCOME RECORDING CLIENT SYSTEM (IRCS)")
        print("*"*50)
        print("1. Add Income Item")
        print("2. Delete Income Item")
        print("3. Update Income Item")
        print("4. Search Income Item")
        print("5. Generate Income Sheet")
        print("6. View All Income Items")
        print("0. Exit")
        print("*"*50)
    
    def get_user_choice(self):
        """Get and validate user menu choice"""
        try:
            choice = input("Enter your choice (0-6): ").strip()
            if choice in ['0', '1', '2', '3', '4', '5', '6']:
                return choice
            else:
                print("Invalid choice! Please enter a number between 0-6.")
                return None
        except (EOFError, KeyboardInterrupt):
            print("\nExiting application...")
            return '0'
    
    def handle_add_income(self):
        """Handle adding new income item"""
        try:
            print("\n--- Add Income Item ---")
            
            # Get income code
            while True:
                code = input("Enter Income Code (2 letters + 3 digits, e.g., IN001): ").strip().upper()
                if self.manager.validate_income_code(code):
                    if not self.manager.code_exists(code):
                        break
                    else:
                        print("Error: Income code already exists!")
                else:
                    print("Error: Invalid code format! Use 2 letters + 3 digits.")
            
            # Get description
            while True:
                description = input("Enter Description (max 20 characters): ").strip()
                if 1 <= len(description) <= 20:
                    break
                else:
                    print("Error: Description must be 1-20 characters long!")
            
            # Get date
            while True:
                date = input("Enter Date (DD/MM/YYYY): ").strip()
                if self.manager.validate_date(date):
                    break
                else:
                    print("Error: Invalid date format! Use DD/MM/YYYY.")
            
            # Get income amount
            while True:
                try:
                    income_amount = float(input("Enter Income Amount (positive number): ").strip())
                    if income_amount > 0:
                        break
                    else:
                        print("Error: Income amount must be positive!")
                except ValueError:
                    print("Error: Please enter a valid number!")
            
            # Get withholding tax
            while True:
                try:
                    wht_amount = float(input("Enter Withholding Tax Amount (positive or 0): ").strip())
                    if wht_amount >= 0:
                        break
                    else:
                        print("Error: WHT amount cannot be negative!")
                except ValueError:
                    print("Error: Please enter a valid number!")
            
            # Add the income item
            if self.manager.add_income(code, description, date, income_amount, wht_amount):
                print(f"Success: Income item {code} added successfully!")
            else:
                print("Error: Failed to add income item!")
                
        except Exception as e:
            print(f"Error: {str(e)}")
    
    def handle_delete_income(self):
        """Handle deleting income item"""
        try:
            print("\n--- Delete Income Item ---")
            code = input("Enter Income Code to delete: ").strip().upper()
            
            if self.manager.delete_income(code):
                print(f"Success: Income item {code} deleted successfully!")
            else:
                print(f"Error: Income item {code} not found!")
                
        except Exception as e:
            print(f"Error: {str(e)}")
    
    def handle_update_income(self):
        """Handle updating income item"""
        try:
            print("\n--- Update Income Item ---")
            code = input("Enter Income Code to update: ").strip().upper()
            
            if not self.manager.code_exists(code):
                print(f"Error: Income item {code} not found!")
                return
            
            # Show current data
            current_item = self.manager.search_income(code)
            if current_item:
                print(f"Current data: {current_item}")
            
            # Get new description
            while True:
                description = input("Enter new Description (max 20 characters): ").strip()
                if 1 <= len(description) <= 20:
                    break
                else:
                    print("Error: Description must be 1-20 characters long!")
            
            # Get new date
            while True:
                date = input("Enter new Date (DD/MM/YYYY): ").strip()
                if self.manager.validate_date(date):
                    break
                else:
                    print("Error: Invalid date format! Use DD/MM/YYYY.")
            
            # Get new income amount
            while True:
                try:
                    income_amount = float(input("Enter new Income Amount (positive): ").strip())
                    if income_amount > 0:
                        break
                    else:
                        print("Error: Income amount must be positive!")
                except ValueError:
                    print("Error: Please enter a valid number!")
            
            # Get new withholding tax
            while True:
                try:
                    wht_amount = float(input("Enter new WHT Amount (positive or 0): ").strip())
                    if wht_amount >= 0:
                        break
                    else:
                        print("Error: WHT amount cannot be negative!")
                except ValueError:
                    print("Error: Please enter a valid number!")
            
            # Update the income item
            if self.manager.update_income(code, description, date, income_amount, wht_amount):
                print(f"Success: Income item {code} updated successfully!")
            else:
                print("Error: Failed to update income item!")
                
        except Exception as e:
            print(f"Error: {str(e)}")
    
    def handle_search_income(self):
        """Handle searching for income item"""
        try:
            print("\n--- Search Income Item ---")
            code = input("Enter Income Code to search: ").strip().upper()
            
            result = self.manager.search_income(code)
            if result:
                print(f"\nFound Income Item:")
                print(f"Code: {result['code']}")
                print(f"Description: {result['description']}")
                print(f"Date: {result['date']}")
                print(f"Income Amount: Rs {result['income_amount']:.2f}")
                print(f"WHT Amount: Rs {result['wht_amount']:.2f}")
                print(f"Net Amount: Rs {result['income_amount'] - result['wht_amount']:.2f}")
            else:
                print(f"Error: Income item {code} not found!")
                
        except Exception as e:
            print(f"Error: {str(e)}")
    
    def handle_generate_sheet(self):
        """Handle generating income sheet CSV"""
        try:
            print("\n--- Generate Income Sheet ---")
            
            if self.manager.generate_income_sheet():
                print("Success: Income sheet generated successfully!")
                print("File saved as: output/income_sheet.csv")
            else:
                print("Error: Failed to generate income sheet!")
                
        except Exception as e:
            print(f"Error: {str(e)}")
    
    def handle_view_all(self):
        """Handle viewing all income items"""
        try:
            print("\n--- All Income Items ---")
            items = self.manager.get_all_items()
            
            if not items:
                print("No income items found!")
                return
            
            print(f"{'Code':<8} {'Description':<20} {'Date':<12} {'Income':<12} {'WHT':<12}")
            print("-" * 70)
            
            for item in items:
                print(f"{item['code']:<8} {item['description']:<20} {item['date']:<12} "
                      f"Rs {item['income_amount']:<9.2f} Rs {item['wht_amount']:<9.2f}")
                
        except Exception as e:
            print(f"Error: {str(e)}")
    
    def run(self):
        """Main application loop"""
        print("Welcome to Income Recording Client System (IRCS)")
        print("Loading existing data...")
        
        # Load existing data
        self.manager.load_data()
        
        while self.running:
            try:
                self.display_menu()
                choice = self.get_user_choice()
                
                if choice == '0':
                    print("Saving data and exiting...")
                    self.manager.save_data()
                    print("Thank you for using IRCS!")
                    self.running = False
                    
                elif choice == '1':
                    self.handle_add_income()
                    
                elif choice == '2':
                    self.handle_delete_income()
                    
                elif choice == '3':
                    self.handle_update_income()
                    
                elif choice == '4':
                    self.handle_search_income()
                    
                elif choice == '5':
                    self.handle_generate_sheet()
                    
                elif choice == '6':
                    self.handle_view_all()
                    
                # Auto-save after each operation
                if choice in ['1', '2', '3']:
                    self.manager.save_data()
                    
            except KeyboardInterrupt:
                print("\n\nExiting application...")
                self.manager.save_data()
                break
            except Exception as e:
                print(f"Unexpected error: {str(e)}")

def main():
    """Application entry point"""
    try:
        app = IRCSApplication()
        app.run()
    except Exception as e:
        print(f"Fatal error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()