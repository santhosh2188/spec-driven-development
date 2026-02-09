"""
Test Suite for Expense Tracker Application (using unittest)
Tests all CRUD operations, validation, and API endpoints.
Run with: python test_app_unittest.py
"""

import unittest
import json
from datetime import datetime
import sys

# Import the Flask app
from app import app, expenses, Expense, CATEGORIES


class TestExpenseClass(unittest.TestCase):
    """Test the Expense class."""
    
    def setUp(self):
        """Set up test fixtures."""
        expenses.clear()
    
    def test_expense_creation(self):
        """Test creating a new expense."""
        expense = Expense(100.50, 'Shopping', 'New shoes')
        
        self.assertEqual(expense.amount, 100.50)
        self.assertEqual(expense.category, 'Shopping')
        self.assertEqual(expense.description, 'New shoes')
        self.assertIsNotNone(expense.id)
    
    def test_expense_with_date(self):
        """Test creating expense with specific date."""
        expense = Expense(25.00, 'Transportation', 'Uber ride', date='2024-01-15')
        
        self.assertEqual(expense.date, '2024-01-15')
    
    def test_expense_default_date(self):
        """Test that expense gets today's date by default."""
        expense = Expense(10.00, 'Other', 'Test')
        today = datetime.now().strftime('%Y-%m-%d')
        
        self.assertEqual(expense.date, today)
    
    def test_expense_to_dict(self):
        """Test converting expense to dictionary."""
        expense = Expense(75.25, 'Entertainment', 'Movie tickets', date='2024-02-01')
        expense_dict = expense.to_dict()
        
        self.assertEqual(expense_dict['amount'], 75.25)
        self.assertEqual(expense_dict['category'], 'Entertainment')
        self.assertEqual(expense_dict['description'], 'Movie tickets')
        self.assertEqual(expense_dict['date'], '2024-02-01')
        self.assertIn('id', expense_dict)
    
    def test_expense_unique_ids(self):
        """Test that each expense gets a unique ID."""
        expense1 = Expense(10.00, 'Food & Dining', 'Coffee')
        expense2 = Expense(20.00, 'Transportation', 'Bus fare')
        
        self.assertNotEqual(expense1.id, expense2.id)


class TestRoutes(unittest.TestCase):
    """Test Flask routes and views."""
    
    def setUp(self):
        """Set up test client and clear expenses."""
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        self.client = app.test_client()
        expenses.clear()
    
    def test_index_route(self):
        """Test the index page loads."""
        response = self.client.get('/')
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Expense Tracker', response.data)
    
    def test_index_shows_categories(self):
        """Test that categories are displayed on index."""
        response = self.client.get('/')
        
        # Categories are HTML-encoded in the response
        for category in CATEGORIES:
            # Handle HTML encoding (& becomes &amp;)
            html_encoded = category.replace('&', '&amp;')
            self.assertIn(html_encoded.encode(), response.data)
    
    def test_add_expense_success(self):
        """Test adding a valid expense."""
        response = self.client.post('/add', data={
            'amount': '42.50',
            'category': 'Food & Dining',
            'description': 'Dinner',
            'date': '2024-02-09'
        }, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'added successfully', response.data)
        self.assertEqual(len(expenses), 1)
        self.assertEqual(expenses[0].amount, 42.50)
    
    def test_add_expense_missing_fields(self):
        """Test adding expense with missing fields."""
        response = self.client.post('/add', data={
            'amount': '50.00',
            'category': 'Food & Dining'
            # Missing description
        }, follow_redirects=True)
        
        self.assertIn(b'All fields are required', response.data)
        self.assertEqual(len(expenses), 0)
    
    def test_add_expense_invalid_amount(self):
        """Test adding expense with invalid amount."""
        response = self.client.post('/add', data={
            'amount': 'not-a-number',
            'category': 'Food & Dining',
            'description': 'Test',
            'date': '2024-02-09'
        }, follow_redirects=True)
        
        self.assertIn(b'Invalid amount', response.data)
        self.assertEqual(len(expenses), 0)
    
    def test_add_expense_negative_amount(self):
        """Test adding expense with negative amount."""
        response = self.client.post('/add', data={
            'amount': '-10.00',
            'category': 'Food & Dining',
            'description': 'Test',
            'date': '2024-02-09'
        }, follow_redirects=True)
        
        self.assertIn(b'must be greater than zero', response.data)
        self.assertEqual(len(expenses), 0)
    
    def test_add_expense_zero_amount(self):
        """Test adding expense with zero amount."""
        response = self.client.post('/add', data={
            'amount': '0',
            'category': 'Food & Dining',
            'description': 'Test',
            'date': '2024-02-09'
        }, follow_redirects=True)
        
        self.assertIn(b'must be greater than zero', response.data)
        self.assertEqual(len(expenses), 0)
    
    def test_delete_expense_success(self):
        """Test deleting an existing expense."""
        sample_expense = Expense(50.00, 'Food & Dining', 'Lunch at restaurant', date='2024-02-09')
        expenses.append(sample_expense)
        expense_id = sample_expense.id
        
        response = self.client.post(f'/delete/{expense_id}', follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'deleted successfully', response.data)
        self.assertEqual(len(expenses), 0)
    
    def test_delete_expense_not_found(self):
        """Test deleting a non-existent expense."""
        response = self.client.post('/delete/9999', follow_redirects=True)
        
        self.assertIn(b'not found', response.data)
    
    def test_filter_by_category(self):
        """Test filtering expenses by category."""
        # Add multiple expenses
        expenses.append(Expense(10.00, 'Food & Dining', 'Coffee'))
        expenses.append(Expense(50.00, 'Shopping', 'Clothes'))
        expenses.append(Expense(15.00, 'Food & Dining', 'Lunch'))
        
        response = self.client.get('/?category=Food+%26+Dining')
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Coffee', response.data)
        self.assertIn(b'Lunch', response.data)
        self.assertNotIn(b'Clothes', response.data)
    
    def test_clear_expenses(self):
        """Test clearing all expenses."""
        # Add some expenses
        expenses.append(Expense(10.00, 'Food & Dining', 'Test 1'))
        expenses.append(Expense(20.00, 'Shopping', 'Test 2'))
        
        response = self.client.post('/clear', follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'All expenses cleared', response.data)
        self.assertEqual(len(expenses), 0)


class TestAPI(unittest.TestCase):
    """Test API endpoints."""
    
    def setUp(self):
        """Set up test client and clear expenses."""
        app.config['TESTING'] = True
        self.client = app.test_client()
        expenses.clear()
    
    def test_get_expenses_api_empty(self):
        """Test API returns empty list when no expenses."""
        response = self.client.get('/api/expenses')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data, [])
    
    def test_get_expenses_api_with_data(self):
        """Test API returns expenses as JSON."""
        expenses.append(Expense(25.00, 'Food & Dining', 'Breakfast'))
        expenses.append(Expense(100.00, 'Shopping', 'Groceries'))
        
        response = self.client.get('/api/expenses')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]['amount'], 25.00)
        self.assertEqual(data[1]['amount'], 100.00)
    
    def test_get_summary_api_empty(self):
        """Test summary API with no expenses."""
        response = self.client.get('/api/summary')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['total'], 0)
        self.assertEqual(data['count'], 0)
        self.assertEqual(data['by_category'], {})
    
    def test_get_summary_api_with_data(self):
        """Test summary API with expenses."""
        expenses.append(Expense(25.00, 'Food & Dining', 'Breakfast'))
        expenses.append(Expense(30.00, 'Food & Dining', 'Lunch'))
        expenses.append(Expense(100.00, 'Shopping', 'Groceries'))
        
        response = self.client.get('/api/summary')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['total'], 155.00)
        self.assertEqual(data['count'], 3)
        self.assertEqual(data['by_category']['Food & Dining'], 55.00)
        self.assertEqual(data['by_category']['Shopping'], 100.00)
    
    def test_api_content_type(self):
        """Test API returns JSON content type."""
        response = self.client.get('/api/expenses')
        
        self.assertIn('application/json', response.content_type)


class TestIntegration(unittest.TestCase):
    """Integration tests for complete workflows."""
    
    def setUp(self):
        """Set up test client and clear expenses."""
        app.config['TESTING'] = True
        self.client = app.test_client()
        expenses.clear()
    
    def test_complete_workflow(self):
        """Test complete add, view, filter, delete workflow."""
        # Add expenses
        self.client.post('/add', data={
            'amount': '50.00',
            'category': 'Food & Dining',
            'description': 'Dinner',
            'date': '2024-02-09'
        })
        
        self.client.post('/add', data={
            'amount': '30.00',
            'category': 'Transportation',
            'description': 'Taxi',
            'date': '2024-02-09'
        })
        
        # Verify they appear on index
        response = self.client.get('/')
        self.assertIn(b'Dinner', response.data)
        self.assertIn(b'Taxi', response.data)
        
        # Filter by category
        response = self.client.get('/?category=Food+%26+Dining')
        self.assertIn(b'Dinner', response.data)
        self.assertNotIn(b'Taxi', response.data)
        
        # Delete one expense
        expense_id = expenses[0].id
        self.client.post(f'/delete/{expense_id}')
        
        # Verify it's gone
        self.assertEqual(len(expenses), 1)
        response = self.client.get('/')
        self.assertIn(b'Taxi', response.data)
    
    def test_total_calculation(self):
        """Test that totals are calculated correctly."""
        expenses.append(Expense(10.50, 'Food & Dining', 'Coffee'))
        expenses.append(Expense(25.75, 'Food & Dining', 'Lunch'))
        expenses.append(Expense(100.00, 'Shopping', 'Clothes'))
        
        # Test total for all expenses
        response = self.client.get('/')
        self.assertIn(b'136.25', response.data)
        
        # Test total for filtered category
        response = self.client.get('/?category=Food+%26+Dining')
        self.assertIn(b'36.25', response.data)


def run_tests():
    """Run all tests with verbose output."""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestExpenseClass))
    suite.addTests(loader.loadTestsFromTestCase(TestRoutes))
    suite.addTests(loader.loadTestsFromTestCase(TestAPI))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))
    
    # Run tests with verbose output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print("="*70)
    
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
