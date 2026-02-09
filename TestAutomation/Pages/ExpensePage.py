"""
Page Object Model for Expense Tracker Application
Contains all locators and page methods for the Expense Tracker page.
"""

import allure
from selenium.webdriver.common.by import By
from TestAutomation.Utils.UtilLib import Actions, WaitMethods, Logger


class ExpensePage:
    """Page Object for Expense Tracker application."""
    
    # Locators
    PAGE_TITLE = (By.TAG_NAME, "h1")
    
    # Form Elements
    AMOUNT_INPUT = (By.ID, "amount")
    CATEGORY_DROPDOWN = (By.ID, "category")
    DESCRIPTION_INPUT = (By.ID, "description")
    DATE_INPUT = (By.ID, "date")
    ADD_EXPENSE_BUTTON = (By.XPATH, "//button[@type='submit'][contains(text(), 'Add Expense')]")
    
    # Expense Table
    EXPENSES_TABLE = (By.CLASS_NAME, "expenses-table")
    TABLE_ROWS = (By.XPATH, "//table[@class='expenses-table']//tbody//tr")
    TABLE_CELLS = (By.XPATH, "//table[@class='expenses-table']//tbody//tr//td")
    DELETE_BUTTONS = (By.XPATH, "//button[@class='btn btn-danger btn-small']")
    
    # Summary Section
    TOTAL_AMOUNT = (By.CLASS_NAME, "total-amount")
    EXPENSE_COUNT = (By.CLASS_NAME, "count")
    
    # Filter Section
    FILTER_DROPDOWN = (By.ID, "category-filter")
    
    # Clear All Button
    CLEAR_ALL_BUTTON = (By.XPATH, "//button[contains(text(), 'Clear All Expenses')]")
    
    # Flash Messages
    FLASH_MESSAGE = (By.CLASS_NAME, "flash")
    FLASH_SUCCESS = (By.CLASS_NAME, "flash-success")
    FLASH_ERROR = (By.CLASS_NAME, "flash-error")
    
    # Empty State
    EMPTY_STATE = (By.CLASS_NAME, "empty-state")
    
    def __init__(self, driver):
        """
        Initialize ExpensePage.
        
        Args:
            driver: WebDriver instance
        """
        self.driver = driver
        self.actions = Actions(driver)
        self.wait_methods = WaitMethods(driver)
        self.logger = Logger.get_logger(__name__)
    
    @allure.step("Verify Expense Tracker page is loaded")
    def verify_page_loaded(self):
        """Verify that the Expense Tracker page is loaded."""
        self.logger.info("Verifying Expense Tracker page is loaded")
        assert self.actions.is_element_visible(self.PAGE_TITLE), "Page title not found"
        page_title = self.actions.get_text(self.PAGE_TITLE)
        assert "Expense Tracker" in page_title, f"Expected 'Expense Tracker' in title, got '{page_title}'"
        self.logger.info("Expense Tracker page is successfully loaded")
        return True
    
    @allure.step("Add expense with amount: {amount}, category: {category}, description: {description}")
    def add_expense(self, amount, category, description, date=None):
        """
        Add a new expense.
        
        Args:
            amount (str): Expense amount
            category (str): Expense category
            description (str): Expense description
            date (str, optional): Expense date (YYYY-MM-DD format)
        """
        import time
        self.logger.info(f"Adding expense: amount={amount}, category={category}, description={description}")
        
        try:
            # Enter amount
            self.actions.enter_text(self.AMOUNT_INPUT, amount)
            self.logger.info(f"Entered amount: {amount}")
            time.sleep(0.3)
            
            # Select category
            self.actions.select_from_html_select(self.CATEGORY_DROPDOWN, category)
            self.logger.info(f"Selected category: {category}")
            time.sleep(0.3)
            
            # Enter description
            self.actions.enter_text(self.DESCRIPTION_INPUT, description)
            self.logger.info(f"Entered description: {description}")
            time.sleep(0.3)
            
            # Enter date if provided
            if date:
                self.actions.enter_text(self.DATE_INPUT, date)
                self.logger.info(f"Entered date: {date}")
                time.sleep(0.3)
            
            # Click Add button
            self.actions.click_element(self.ADD_EXPENSE_BUTTON)
            self.logger.info("Clicked Add Expense button")
            time.sleep(1)  # Wait for form submission and page update
        except Exception as e:
            self.logger.error(f"Error adding expense: {e}")
            raise
    
    @allure.step("Verify expense added successfully")
    def verify_expense_added(self, description):
        """
        Verify that an expense was added successfully.
        
        Args:
            description (str): Expense description to verify
            
        Returns:
            bool: True if expense is found
        """
        import time
        self.logger.info(f"Verifying expense '{description}' was added")
        
        try:
            # Wait for success message
            time.sleep(0.5)
            assert self.actions.is_element_visible(self.FLASH_SUCCESS, timeout=5), "Success message not found"
            
            # Verify expense appears in table
            time.sleep(0.5)
            assert self.actions.is_element_visible(self.EXPENSES_TABLE), "Expenses table not found"
            
            # Get all table rows and check if description exists
            time.sleep(1)  # Wait for table to fully render
            rows = self.driver.find_elements(*self.TABLE_ROWS)
            expense_found = False
            for row in rows:
                try:
                    row_text = row.text
                    if description in row_text:
                        expense_found = True
                        self.logger.info(f"Expense '{description}' found in table")
                        break
                except Exception as e:
                    self.logger.debug(f"Error reading row: {e}")
                    continue
            
            assert expense_found, f"Expense '{description}' not found in table"
        except Exception as e:
            self.logger.error(f"Error verifying expense: {e}")
            raise
        return True
    
    @allure.step("Get total expenses amount")
    def get_total_amount(self):
        """
        Get the total expenses amount.
        
        Returns:
            float: Total amount
        """
        self.logger.info("Getting total expenses amount")
        try:
            total_text = self.actions.get_text(self.TOTAL_AMOUNT)
            # Extract numeric value from '$XXX.XX' format
            total_value = float(total_text.replace("$", "").strip())
            self.logger.info(f"Total amount: ${total_value}")
            return total_value
        except Exception as e:
            self.logger.warning(f"Could not retrieve total amount: {str(e)}")
            # Return 0 if unable to get total
            return 0.0
    
    @allure.step("Get expenses count")
    def get_expense_count(self):
        """
        Get the number of expenses.
        
        Returns:
            int: Expense count
        """
        import time
        self.logger.info("Getting expenses count")
        time.sleep(0.5)  # Wait for DOM to stabilize
        try:
            count_text = self.actions.get_text(self.EXPENSE_COUNT)
            count = int(count_text.strip())
            self.logger.info(f"Expense count: {count}")
            return count
        except Exception as e:
            self.logger.warning(f"Could not retrieve expense count: {str(e)}")
            # Fall back to counting table rows
            try:
                rows = self.driver.find_elements(*self.TABLE_ROWS)
                count = len(rows)
                self.logger.info(f"Expense count (from table rows): {count}")
                return count
            except:
                self.logger.error("Could not get expense count from either method")
                return 0
    
    @allure.step("Delete expense with description: {description}")
    def delete_expense(self, description):
        """
        Delete an expense by its description.
        
        Args:
            description (str): Description of expense to delete
        """
        import time
        self.logger.info(f"Deleting expense with description: {description}")
        
        try:
            # Find the row with the matching description
            time.sleep(0.5)
            rows = self.driver.find_elements(*self.TABLE_ROWS)
            deleted = False
            
            for row in rows:
                try:
                    if description in row.text:
                        # Find delete button in this row
                        delete_button = row.find_element(By.XPATH, ".//button[@class='btn btn-danger btn-small']")
                        delete_button.click()
                        self.logger.info(f"Clicked delete button for expense '{description}'")
                        time.sleep(0.5)
                        
                        # Accept confirmation alert
                        self.actions.accept_alert()
                        self.logger.info("Accepted delete confirmation")
                        time.sleep(1)  # Wait for page update
                        deleted = True
                        break
                except Exception as e:
                    self.logger.debug(f"Error processing row: {e}")
                    continue
            
            assert deleted, f"Expense with description '{description}' not found"
        except Exception as e:
            self.logger.error(f"Error deleting expense: {e}")
            raise
    
    @allure.step("Verify expense deleted successfully")
    def verify_expense_deleted(self, description):
        """
        Verify that an expense was deleted successfully.
        
        Args:
            description (str): Description of deleted expense
            
        Returns:
            bool: True if expense is not found
        """
        self.logger.info(f"Verifying expense '{description}' was deleted")
        
        # Wait for success message
        assert self.actions.is_element_visible(self.FLASH_SUCCESS), "Success message not found"
        
        # Verify expense is no longer in table
        rows = self.driver.find_elements(*self.TABLE_ROWS)
        for row in rows:
            assert description not in row.text, f"Expense '{description}' still found in table after deletion"
        
        self.logger.info(f"Expense '{description}' successfully deleted")
        return True
    
    @allure.step("Filter expenses by category: {category}")
    def filter_by_category(self, category):
        """
        Filter expenses by category.
        
        Args:
            category (str): Category to filter by
        """
        self.logger.info(f"Filtering expenses by category: {category}")
        self.actions.select_from_html_select(self.FILTER_DROPDOWN, category)
        self.logger.info(f"Applied filter for category: {category}")
    
    @allure.step("Get all expenses in current table")
    def get_all_expenses(self):
        """
        Get all expenses from the table.
        
        Returns:
            list: List of dictionaries containing expense details
        """
        import time
        self.logger.info("Retrieving all expenses from table")
        expenses = []
        
        time.sleep(0.5)  # Wait for DOM to stabilize
        try:
            # Refresh elements to avoid stale element references
            rows = self.driver.find_elements(*self.TABLE_ROWS)
            
            for row in rows:
                try:
                    cells = row.find_elements(By.TAG_NAME, "td")
                    if len(cells) >= 4:
                        # Get text from cells and handle stale elements
                        try:
                            date_text = cells[0].text
                            category_text = cells[1].text
                            description_text = cells[2].text
                            amount_text = cells[3].text
                            
                            expense = {
                                'date': date_text,
                                'category': category_text,
                                'description': description_text,
                                'amount': amount_text
                            }
                            expenses.append(expense)
                            self.logger.info(f"Found expense: {expense}")
                        except Exception as e:
                            self.logger.warning(f"Error reading row cells: {str(e)}")
                            continue
                except Exception as e:
                    self.logger.warning(f"Error processing row: {str(e)}")
                    continue
            
        except Exception as e:
            self.logger.warning(f"Error retrieving expenses: {str(e)}")
        
        self.logger.info(f"Total expenses retrieved: {len(expenses)}")
        return expenses
    
    @allure.step("Clear all expenses")
    def clear_all_expenses(self):
        """Clear all expenses from the tracker."""
        import time
        self.logger.info("Clearing all expenses")
        
        try:
            # Wait for button to be available
            time.sleep(0.5)
            # Click clear all button
            self.actions.click_element(self.CLEAR_ALL_BUTTON)
            self.logger.info("Clicked Clear All Expenses button")
            time.sleep(0.5)
            
            # Accept confirmation alert
            self.actions.accept_alert()
            self.logger.info("Accepted clear confirmation")
            time.sleep(1)  # Wait for page to update
        except Exception as e:
            self.logger.warning(f"Error clearing expenses: {e}")
            raise
    
    @allure.step("Verify all expenses cleared successfully")
    def verify_expenses_cleared(self):
        """
        Verify that all expenses have been cleared.
        
        Returns:
            bool: True if no expenses remain
        """
        self.logger.info("Verifying all expenses were cleared")
        
        # Wait for success message
        assert self.actions.is_element_visible(self.FLASH_SUCCESS), "Success message not found"
        
        # Check for empty state or zero expense count
        try:
            count = self.get_expense_count()
            assert count == 0, f"Expected 0 expenses, but found {count}"
        except:
            # If count element not found, check for empty state
            assert self.actions.is_element_visible(self.EMPTY_STATE), "Expected empty state or zero count"
        
        self.logger.info("All expenses successfully cleared")
        return True
    
    @allure.step("Verify error message displayed")
    def verify_error_message(self, expected_text=None):
        """
        Verify that an error message is displayed.
        
        Args:
            expected_text (str, optional): Expected error message text
            
        Returns:
            bool: True if error message is found
        """
        self.logger.info("Verifying error message")
        assert self.actions.is_element_visible(self.FLASH_ERROR), "Error message not found"
        
        error_text = self.actions.get_text(self.FLASH_MESSAGE)
        if expected_text:
            assert expected_text in error_text, f"Expected '{expected_text}' in error, got '{error_text}'"
        
        self.logger.info(f"Error message verified: {error_text}")
        return True
    
    @allure.step("Verify success message displayed")
    def verify_success_message(self, expected_text=None):
        """
        Verify that a success message is displayed.
        
        Args:
            expected_text (str, optional): Expected success message text
            
        Returns:
            bool: True if success message is found
        """
        self.logger.info("Verifying success message")
        assert self.actions.is_element_visible(self.FLASH_SUCCESS), "Success message not found"
        
        success_text = self.actions.get_text(self.FLASH_MESSAGE)
        if expected_text:
            assert expected_text in success_text, f"Expected '{expected_text}' in success, got '{success_text}'"
        
        self.logger.info(f"Success message verified: {success_text}")
        return True
