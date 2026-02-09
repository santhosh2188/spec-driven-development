"""
Test Cases for Expense Tracker Application
Tests for Add Expense, Delete Expense, and Clear Expenses functionality.
Using pytest and Allure reports framework.

Run tests with: pytest TestAutomation/Tests/ExpenseTest.py -v --alluredir=allure-results
Generate report: allure serve allure-results
"""

import pytest
import allure
import time
from datetime import datetime, timedelta
from TestAutomation.Utils.UtilLib import Logger


@allure.feature("Expense Tracker")
@allure.suite("Add Expense Tests")
class TestAddExpense:
    """Test cases for adding expenses."""
    
    @pytest.mark.smoke
    @pytest.mark.add_expense
    @pytest.mark.regression
    @allure.title("Add single expense successfully")
    @allure.description("Verify that a single expense can be added with valid data")
    def test_add_single_expense(self, navigate_to_app, expense_page):
        """Test adding a single expense."""
        logger = Logger.get_logger(__name__)
        
        with allure.step("Clear existing expenses for clean state"):
            try:
                expense_page.clear_all_expenses()
                logger.info("Cleared existing expenses")
            except:
                logger.info("No expenses to clear")
        
        with allure.step("Verify page is loaded"):
            expense_page.verify_page_loaded()
        
        with allure.step("Get initial expense count"):
            initial_count = expense_page.get_expense_count()
            logger.info(f"Initial expense count: {initial_count}")
        
        with allure.step("Add new expense"):
            expense_page.add_expense(
                amount="50.00",
                category="Food & Dining",
                description="Lunch at restaurant"
            )
        
        with allure.step("Verify expense was added"):
            expense_page.verify_expense_added("Lunch at restaurant")
        
        with allure.step("Verify success message"):
            expense_page.verify_success_message("added successfully")
        
        with allure.step("Verify expense count increased"):
            new_count = expense_page.get_expense_count()
            assert new_count == initial_count + 1, \
                f"Expected count {initial_count + 1}, got {new_count}"
            logger.info(f"New expense count: {new_count}")
    
    @pytest.mark.smoke
    @pytest.mark.add_expense
    @pytest.mark.regression
    @allure.title("Add multiple expenses")
    @allure.description("Verify that multiple expenses can be added sequentially")
    def test_add_multiple_expenses(self, navigate_to_app, expense_page):
        """Test adding multiple expenses."""
        logger = Logger.get_logger(__name__)
        
        with allure.step("Clear existing expenses for clean state"):
            try:
                expense_page.clear_all_expenses()
                logger.info("Cleared existing expenses")
            except:
                logger.info("No expenses to clear")
        
        expenses = [
            {"amount": "25.50", "category": "Food & Dining", "description": "Coffee"},
            {"amount": "100.00", "category": "Shopping", "description": "New shoes"},
            {"amount": "15.00", "category": "Transportation", "description": "Taxi fare"},
            {"amount": "45.99", "category": "Entertainment", "description": "Movie tickets"}
        ]
        
        expense_page.verify_page_loaded()
        
        with allure.step(f"Add {len(expenses)} expenses"):
            for i, expense in enumerate(expenses, 1):
                with allure.step(f"Add expense {i}: {expense['description']}"):
                    expense_page.add_expense(
                        amount=expense['amount'],
                        category=expense['category'],
                        description=expense['description']
                    )
                    expense_page.verify_expense_added(expense['description'])
                    logger.info(f"Added expense {i}: {expense['description']}")
        
        with allure.step("Verify all expenses are in list"):
            all_expenses = expense_page.get_all_expenses()
            assert len(all_expenses) == len(expenses), \
                f"Expected {len(expenses)} expenses, got {len(all_expenses)}"
            
            for expense in expenses:
                found = any(exp['description'] == expense['description'] 
                           for exp in all_expenses)
                assert found, f"Expense '{expense['description']}' not found"
                logger.info(f"Verified expense: {expense['description']}")
    
    @pytest.mark.add_expense
    @pytest.mark.regression
    @allure.title("Add expense with custom date")
    @allure.description("Verify that an expense can be added with a custom date")
    def test_add_expense_with_custom_date(self, navigate_to_app, expense_page):
        """Test adding expense with custom date."""
        logger = Logger.get_logger(__name__)
        
        with allure.step("Clear existing expenses for clean state"):
            try:
                expense_page.clear_all_expenses()
                logger.info("Cleared existing expenses")
            except:
                logger.info("No expenses to clear")
        
        expense_page.verify_page_loaded()
        
        with allure.step("Add expense with custom date"):
            from datetime import datetime, timedelta
            custom_date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
            expense_page.add_expense(
                amount="75.00",
                category="Bills & Utilities",
                description="Electricity bill",
                date=custom_date
            )
        
        with allure.step("Verify expense with date was added"):
            expense_page.verify_expense_added("Electricity bill")
            logger.info("Expense with custom date verified")
    
    @pytest.mark.add_expense
    @pytest.mark.smoke
    @allure.title("Add expense with all categories")
    @allure.description("Verify expenses can be added in all available categories")
    def test_add_expense_all_categories(self, navigate_to_app, expense_page):
        """Test adding expenses in all categories."""
        logger = Logger.get_logger(__name__)
        
        categories = [
            "Food & Dining",
            "Transportation",
            "Shopping",
            "Entertainment",
            "Bills & Utilities",
            "Healthcare",
            "Other"
        ]
        
        expense_page.verify_page_loaded()
        
        with allure.step(f"Add expenses for all {len(categories)} categories"):
            for i, category in enumerate(categories, 1):
                with allure.step(f"Add expense in category: {category}"):
                    expense_page.add_expense(
                        amount=f"{10 * i}.00",
                        category=category,
                        description=f"Test expense in {category}"
                    )
                    expense_page.verify_expense_added(f"Test expense in {category}")
                    logger.info(f"Added expense in category: {category}")
    
    @pytest.mark.add_expense
    @pytest.mark.regression
    @allure.title("Verify total amount calculation")
    @allure.description("Verify that total amount is calculated correctly after adding expenses")
    def test_total_amount_calculation(self, navigate_to_app, expense_page):
        """Test total amount calculation."""
        logger = Logger.get_logger(__name__)
        
        expense_page.verify_page_loaded()
        
        with allure.step("Get initial total"):
            initial_total = expense_page.get_total_amount()
            logger.info(f"Initial total: ${initial_total}")
        
        test_amounts = [50.00, 25.50, 100.00]
        
        with allure.step("Add expenses and verify total"):
            for amount in test_amounts:
                expense_page.add_expense(
                    amount=str(amount),
                    category="Shopping",
                    description=f"Purchase ${amount}"
                )
                expense_page.verify_expense_added(f"Purchase ${amount}")
        
        with allure.step("Verify final total"):
            final_total = expense_page.get_total_amount()
            expected_total = initial_total + sum(test_amounts)
            assert abs(final_total - expected_total) < 0.01, \
                f"Expected total ${expected_total}, got ${final_total}"
            logger.info(f"Final total verified: ${final_total}")


@allure.feature("Expense Tracker")
@allure.suite("Delete Expense Tests")
class TestDeleteExpense:
    """Test cases for deleting expenses."""
    
    @pytest.mark.smoke
    @pytest.mark.delete_expense
    @pytest.mark.regression
    @allure.title("Delete single expense successfully")
    @allure.description("Verify that a single expense can be deleted")
    def test_delete_single_expense(self, navigate_to_app, expense_page):
        """Test deleting a single expense."""
        logger = Logger.get_logger(__name__)
        
        expense_page.verify_page_loaded()
        
        with allure.step("Add an expense"):
            expense_page.add_expense(
                amount="50.00",
                category="Shopping",
                description="Item to delete"
            )
            expense_page.verify_expense_added("Item to delete")
        
        with allure.step("Get expense count before deletion"):
            count_before = expense_page.get_expense_count()
            logger.info(f"Expense count before deletion: {count_before}")
        
        with allure.step("Delete the expense"):
            expense_page.delete_expense("Item to delete")
        
        with allure.step("Verify expense was deleted"):
            expense_page.verify_expense_deleted("Item to delete")
        
        with allure.step("Verify success message"):
            expense_page.verify_success_message("deleted successfully")
        
        with allure.step("Verify expense count decreased"):
            count_after = expense_page.get_expense_count()
            assert count_after == count_before - 1, \
                f"Expected count {count_before - 1}, got {count_after}"
            logger.info(f"Expense count after deletion: {count_after}")
    
    
    @pytest.mark.delete_expense
    @pytest.mark.smoke
    @allure.title("Verify total updates after deletion")
    @allure.description("Verify that total amount is updated correctly after deleting an expense")
    def test_total_updates_after_deletion(self, navigate_to_app, expense_page):
        """Test total amount updates after deletion."""
        logger = Logger.get_logger(__name__)
        
        with allure.step("Clear existing expenses for clean state"):
            try:
                expense_page.clear_all_expenses()
                logger.info("Cleared existing expenses")
            except:
                logger.info("No expenses to clear")
        
        expense_page.verify_page_loaded()
        
        with allure.step("Add expense"):
            expense_page.add_expense(
                amount="100.00",
                category="Shopping",
                description="Expensive item"
            )
            expense_page.verify_expense_added("Expensive item")
        
        with allure.step("Get total before deletion"):
            # Refresh page to ensure fresh elements
            import time
            time.sleep(1)
            expense_page.actions.driver.refresh()
            time.sleep(1)
            total_before = expense_page.get_total_amount()
            logger.info(f"Total before deletion: ${total_before}")
        
        with allure.step("Delete expense"):
            expense_page.delete_expense("Expensive item")
            expense_page.verify_expense_deleted("Expensive item")
        
        with allure.step("Verify total was updated"):
            import time
            time.sleep(1)
            total_after = expense_page.get_total_amount()
            assert total_after == total_before - 100.00, \
                f"Expected total ${total_before - 100.00}, got ${total_after}"
            logger.info(f"Total after deletion: ${total_after}")


@allure.feature("Expense Tracker")
@allure.suite("Clear Expenses Tests")
class TestClearExpenses:
    """Test cases for clearing all expenses."""
    
    @pytest.mark.smoke
    @pytest.mark.clear_expenses
    @pytest.mark.regression
    @allure.title("Clear all expenses")
    @allure.description("Verify that all expenses can be cleared at once")
    def test_clear_all_expenses(self, navigate_to_app, expense_page):
        """Test clearing all expenses."""
        logger = Logger.get_logger(__name__)
        
        with allure.step("Clear any existing expenses first"):
            try:
                expense_page.clear_all_expenses()
                logger.info("Cleared any existing expenses")
            except:
                logger.info("No expenses to clear")
        
        import time
        time.sleep(1)
        expense_page.actions.driver.refresh()
        time.sleep(1)
        
        expense_page.verify_page_loaded()
        
        with allure.step("Add multiple expenses"):
            expenses = [
                ("Expense 1", "25.00", "Food & Dining"),
                ("Expense 2", "50.00", "Shopping"),
                ("Expense 3", "75.00", "Transportation")
            ]
            for desc, amount, category in expenses:
                expense_page.add_expense(
                    amount=amount,
                    category=category,
                    description=desc
                )
                logger.info(f"Added: {desc}")
        
        with allure.step("Verify expenses were added"):
            count_before = expense_page.get_expense_count()
            assert count_before == len(expenses), \
                f"Expected {len(expenses)} expenses, got {count_before}"
            logger.info(f"Verified {count_before} expenses added")
        
        with allure.step("Clear all expenses"):
            expense_page.clear_all_expenses()
        
        with allure.step("Verify all expenses were cleared"):
            expense_page.verify_expenses_cleared()
        
        with allure.step("Verify success message"):
            expense_page.verify_success_message("All expenses cleared")
        
        with allure.step("Verify empty state"):
            count_after = expense_page.get_expense_count()
            assert count_after == 0, f"Expected 0 expenses, got {count_after}"
            logger.info("Expense list is now empty")
    
    @pytest.mark.clear_expenses
    @pytest.mark.regression
    @allure.title("Verify total is zero after clearing")
    @allure.description("Verify that total amount becomes zero after clearing all expenses")
    def test_total_zero_after_clear(self, navigate_to_app, expense_page):
        """Test total amount is zero after clearing."""
        logger = Logger.get_logger(__name__)
        
        with allure.step("Clear any existing expenses first"):
            try:
                expense_page.clear_all_expenses()
                logger.info("Cleared any existing expenses")
            except:
                logger.info("No expenses to clear")
        
        import time
        time.sleep(1)
        expense_page.actions.driver.refresh()
        time.sleep(1)
        
        expense_page.verify_page_loaded()
        
        with allure.step("Add multiple expenses"):
            amounts = ["50.00", "100.00", "75.50"]
            for i, amount in enumerate(amounts, 1):
                expense_page.add_expense(
                    amount=amount,
                    category="Shopping",
                    description=f"Item {i}"
                )
        
        with allure.step("Get total before clearing"):
            total_before = expense_page.get_total_amount()
            logger.info(f"Total before clearing: ${total_before}")
            assert total_before > 0, "Total should be greater than zero"
        
        with allure.step("Clear all expenses"):
            expense_page.clear_all_expenses()
        
        with allure.step("Verify total is zero"):
            import time
            time.sleep(1)
            total_after = expense_page.get_total_amount()
            assert total_after == 0.00, \
                f"Expected total $0.00, got ${total_after}"
            logger.info(f"Total after clearing: ${total_after}")
    
    @pytest.mark.clear_expenses
    @allure.title("Clear and add expenses again")
    @allure.description("Verify that expenses can be added after clearing all expenses")
    def test_add_after_clear(self, navigate_to_app, expense_page):
        """Test adding expenses after clearing."""
        logger = Logger.get_logger(__name__)
        
        expense_page.verify_page_loaded()
        
        with allure.step("Add and clear expenses"):
            expense_page.add_expense(
                amount="100.00",
                category="Shopping",
                description="First expense"
            )
            expense_page.verify_expense_added("First expense")
            
            expense_page.clear_all_expenses()
            expense_page.verify_expenses_cleared()
            logger.info("Expenses cleared")
        
        with allure.step("Add new expense after clearing"):
            expense_page.add_expense(
                amount="50.00",
                category="Food & Dining",
                description="New expense"
            )
            expense_page.verify_expense_added("New expense")
            logger.info("New expense added after clearing")
        
        with allure.step("Verify only new expense exists"):
            all_expenses = expense_page.get_all_expenses()
            assert len(all_expenses) == 1, \
                f"Expected 1 expense, got {len(all_expenses)}"
            assert all_expenses[0]['description'] == "New expense"
            logger.info("Verified new expense is the only expense")


@allure.feature("Expense Tracker")
@allure.suite("Filter & Navigation Tests")
class TestFilterAndNavigation:
    """Test cases for filtering and navigation functionality."""
    
    @pytest.mark.regression
    @allure.title("Filter expenses by category")
    @allure.description("Verify that expenses can be filtered by category")
    def test_filter_by_category(self, navigate_to_app, expense_page):
        """Test filtering expenses by category."""
        logger = Logger.get_logger(__name__)
        
        with allure.step("Clear any existing expenses first"):
            try:
                expense_page.clear_all_expenses()
                logger.info("Cleared any existing expenses")
            except:
                logger.info("No expenses to clear")
        
        import time
        time.sleep(1)
        expense_page.actions.driver.refresh()
        time.sleep(1)
        
        expense_page.verify_page_loaded()
        
        with allure.step("Add expenses in different categories"):
            expenses = [
                ("Burger", "15.00", "Food & Dining"),
                ("Taxi", "20.00", "Transportation"),
                ("Pizza", "12.00", "Food & Dining"),
                ("Bus", "2.50", "Transportation")
            ]
            for desc, amount, category in expenses:
                expense_page.add_expense(
                    amount=amount,
                    category=category,
                    description=desc
                )
                logger.info(f"Added: {desc}")
        
        with allure.step("Filter by 'Food & Dining' category"):
            expense_page.filter_by_category("Food & Dining")
        
        with allure.step("Verify only Food & Dining expenses are shown"):
            import time
            time.sleep(1)
            filtered_expenses = expense_page.get_all_expenses()
            
            # Check that we only see Food & Dining items (Burger, Pizza)
            for expense in filtered_expenses:
                description = expense['description']
                assert description in ["Burger", "Pizza"], \
                    f"Unexpected expense found: {description}"
            logger.info("Filter verified")
    
    @pytest.mark.regression
    @allure.title("Get all expenses from table")
    @allure.description("Verify that all expenses can be retrieved from the table")
    def test_get_all_expenses(self, navigate_to_app, expense_page):
        """Test retrieving all expenses."""
        logger = Logger.get_logger(__name__)
        
        with allure.step("Clear any existing expenses first"):
            try:
                expense_page.clear_all_expenses()
                logger.info("Cleared any existing expenses")
            except:
                logger.info("No expenses to clear")
        
        import time
        time.sleep(1)
        expense_page.actions.driver.refresh()
        time.sleep(1)
        
        expense_page.verify_page_loaded()
        
        expense_data = [
            ("Lunch", "45.00", "Food & Dining"),
            ("Gas", "60.00", "Transportation"),
            ("Book", "25.00", "Shopping")
        ]
        
        with allure.step("Add multiple expenses"):
            for desc, amount, category in expense_data:
                expense_page.add_expense(
                    amount=amount,
                    category=category,
                    description=desc
                )
        
        with allure.step("Retrieve all expenses"):
            import time
            time.sleep(1)
            all_expenses = expense_page.get_all_expenses()
        
        with allure.step("Verify all expenses are retrieved"):
            assert len(all_expenses) == len(expense_data), \
                f"Expected {len(expense_data)} expenses, got {len(all_expenses)}"
            
            for expense in all_expenses:
                assert 'date' in expense
                assert 'category' in expense
                assert 'description' in expense
                assert 'amount' in expense
                logger.info(f"Expense data: {expense}")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--alluredir=allure-results"])
