# Expense Tracker Test Automation Framework

Complete test automation framework for the Expense Tracker application using **Selenium**, **Pytest**, and **Allure Reports**.

## 📋 Table of Contents
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running Tests](#running-tests)
- [Generating Allure Reports](#generating-allure-reports)
- [Test Coverage](#test-coverage)
- [Page Object Model](#page-object-model)

---

## 📁 Project Structure

```
TestAutomation/
├── Pages/
│   ├── __init__.py
│   └── ExpensePage.py          # Page Object Model for Expense Tracker page
├── Tests/
│   ├── __init__.py
│   └── ExpenseTest.py          # All test cases
├── Utils/
│   ├── __init__.py
│   └── UtilLib.py              # Utility functions and helpers
├── __init__.py
└── conftest.py                 # Pytest fixtures and configuration

├── pytest.ini                  # Pytest configuration
├── requirements-test.txt       # Python dependencies
└── README_AUTOMATION.md        # This file
```

---

## 🔧 Prerequisites

- **Python**: 3.8 or higher
- **Chrome Browser**: Latest version
- **ChromeDriver**: Compatible with your Chrome version
- **pip**: Python package manager

### Required Software

1. **Python 3.8+** - [Download Python](https://www.python.org/downloads/)
2. **Chrome Browser** - [Download Chrome](https://www.google.com/chrome/)
3. **ChromeDriver** - [Download ChromeDriver](https://chromedriver.chromium.org/)
   - Ensure ChromeDriver version matches your Chrome browser version
   - Add ChromeDriver to your PATH or place it in the project directory

---

## 📦 Installation

### 1. Clone or Navigate to Project Directory

```bash
cd c:\Automation\Assess
```

### 2. Create Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements-test.txt
```

### 4. Verify Chrome and ChromeDriver

```bash
# Check Chrome version
chrome --version

# Verify chromedriver is accessible
chromedriver --version
```

---

## ⚙️ Configuration

### Application URL

The base URL is configured in `conftest.py`:

```python
base_url="http://127.0.0.1:5000"
```

To change the URL, edit the `navigate_to_app` fixture in `TestAutomation/conftest.py`:

```python
@pytest.fixture(scope="function")
def navigate_to_app(common_methods):
    common_methods.navigate_to_url("http://your-new-url:port")
    yield common_methods
```

### WebDriver Configuration

Edit `TestAutomation/Utils/UtilLib.py` in the `DriverFactory.get_chrome_driver()` method:

```python
@staticmethod
def get_chrome_driver(headless=False):
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    # Add more options as needed
    driver = webdriver.Chrome(options=options)
    return driver
```

### Logging Configuration

Logs are automatically generated in the `Logs/` directory with timestamp:
- File format: `automation_YYYYMMDD_HHMMSS.log`
- Log level: DEBUG (file) and INFO (console)

---

## 🧪 Running Tests

### Run All Tests

```bash
pytest TestAutomation/Tests/ExpenseTest.py -v --alluredir=allure-results
```

### Run Specific Test Class

```bash
# Run Add Expense tests
pytest TestAutomation/Tests/ExpenseTest.py::TestAddExpense -v --alluredir=allure-results

# Run Delete Expense tests
pytest TestAutomation/Tests/ExpenseTest.py::TestDeleteExpense -v --alluredir=allure-results

# Run Clear Expenses tests
pytest TestAutomation/Tests/ExpenseTest.py::TestClearExpenses -v --alluredir=allure-results

# Run Filter & Navigation tests
pytest TestAutomation/Tests/ExpenseTest.py::TestFilterAndNavigation -v --alluredir=allure-results
```

### Run Specific Test Case

```bash
pytest TestAutomation/Tests/ExpenseTest.py::TestAddExpense::test_add_single_expense -v --alluredir=allure-results
```

### Run Tests by Marker

```bash
# Run only smoke tests
pytest TestAutomation/Tests/ExpenseTest.py -m smoke -v --alluredir=allure-results

# Run only regression tests
pytest TestAutomation/Tests/ExpenseTest.py -m regression -v --alluredir=allure-results

# Run add expense tests
pytest TestAutomation/Tests/ExpenseTest.py -m add_expense -v --alluredir=allure-results

# Run delete expense tests
pytest TestAutomation/Tests/ExpenseTest.py -m delete_expense -v --alluredir=allure-results

# Run clear expenses tests
pytest TestAutomation/Tests/ExpenseTest.py -m clear_expenses -v --alluredir=allure-results
```

### Run Tests in Parallel

```bash
# Run tests using 4 workers
pytest TestAutomation/Tests/ExpenseTest.py -v -n 4 --alluredir=allure-results
```

### Run with Timeout

```bash
# Each test has a 300 second timeout
pytest TestAutomation/Tests/ExpenseTest.py -v --timeout=300 --alluredir=allure-results
```

### Headless Mode

To run tests in headless mode (no browser window):

Edit `conftest.py` and change:
```python
@pytest.fixture(scope="function")
def driver():
    browser_driver = DriverFactory.get_chrome_driver(headless=True)  # Change to True
```

---

## 📊 Generating Allure Reports

### Prerequisites

Install Allure:
```bash
# On Windows
choco install allure
# or download from: https://github.com/allure-framework/allure2/releases

# On macOS
brew install allure

# On Linux
sudo apt-add-repository ppa:qameta/allure
sudo apt-get update
sudo apt-get install allure
```

### Generate and View Report

```bash
# Run tests with allure results
pytest TestAutomation/Tests/ExpenseTest.py -v --alluredir=allure-results

# Generate HTML report from results
allure generate allure-results --clean -o allure-report

# Serve the report (opens in browser)
allure serve allure-results
```

### View Generated Report

Open the generated report:
```bash
# Navigate to report directory
cd allure-report

# Open index.html in browser
start index.html  # Windows
open index.html   # macOS
xdg-open index.html  # Linux
```

---

## 🧾 Test Coverage

### Add Expense Tests (TestAddExpense)

| Test Case | Description |
|-----------|-------------|
| `test_add_single_expense` | Add a single expense with valid data |
| `test_add_multiple_expenses` | Add multiple expenses sequentially |
| `test_add_expense_with_custom_date` | Add expense with custom date |
| `test_add_expense_all_categories` | Add expenses in all categories |
| `test_total_amount_calculation` | Verify total calculation after adding |

### Delete Expense Tests (TestDeleteExpense)

| Test Case | Description |
|-----------|-------------|
| `test_delete_single_expense` | Delete a single expense |
| `test_delete_multiple_expenses` | Delete multiple expenses |
| `test_total_updates_after_deletion` | Verify total updates after deletion |

### Clear Expenses Tests (TestClearExpenses)

| Test Case | Description |
|-----------|-------------|
| `test_clear_all_expenses` | Clear all expenses at once |
| `test_total_zero_after_clear` | Verify total becomes zero after clearing |
| `test_add_after_clear` | Add expenses after clearing |

### Filter & Navigation Tests (TestFilterAndNavigation)

| Test Case | Description |
|-----------|-------------|
| `test_filter_by_category` | Filter expenses by category |
| `test_get_all_expenses` | Retrieve all expenses from table |

---

## 📄 Page Object Model (POM)

### ExpensePage Class

The `ExpensePage` class encapsulates all interactions with the Expense Tracker page:

#### Key Methods

**Navigation & Verification:**
- `verify_page_loaded()` - Verify page is loaded
- `verify_expense_added(description)` - Verify expense was added
- `verify_expense_deleted(description)` - Verify expense was deleted
- `verify_expenses_cleared()` - Verify all expenses cleared
- `verify_error_message(expected_text)` - Verify error message
- `verify_success_message(expected_text)` - Verify success message

**Add Expense:**
- `add_expense(amount, category, description, date=None)` - Add new expense

**Delete Expense:**
- `delete_expense(description)` - Delete expense by description

**Clear Expenses:**
- `clear_all_expenses()` - Clear all expenses

**Filtering & Retrieval:**
- `filter_by_category(category)` - Filter by category
- `get_all_expenses()` - Get all expenses from table
- `get_total_amount()` - Get total amount
- `get_expense_count()` - Get expense count

#### Locators

All UI element locators are defined as class variables using various strategies (ID, CLASS_NAME, XPATH, etc.):

```python
AMOUNT_INPUT = (By.ID, "amount")
CATEGORY_DROPDOWN = (By.ID, "category")
EXPENSES_TABLE = (By.CLASS_NAME, "expenses-table")
# ... more locators
```

---

## 🛠️ Utility Functions (UtilLib)

### Logger Class
- `get_logger(logger_name)` - Create configured logger instance

### DriverFactory Class
- `get_chrome_driver(headless=False)` - Create Chrome WebDriver

### WaitMethods Class
- `wait_for_element_visible(locator, timeout)` - Wait for element visibility
- `wait_for_element_clickable(locator, timeout)` - Wait for element clickability
- `wait_for_element_presence(locator, timeout)` - Wait for element presence
- `wait_for_text_in_element(locator, text, timeout)` - Wait for text

### Actions Class
- `click_element(locator)` - Click element
- `enter_text(locator, text)` - Enter text
- `get_text(locator)` - Get element text
- `select_from_html_select(locator, value)` - Select dropdown value
- `accept_alert()` - Accept alert
- `dismiss_alert()` - Dismiss alert

### CommonMethods Class
- `navigate_to_url(url)` - Navigate to URL
- `refresh_page()` - Refresh page
- `maximize_window()` - Maximize window
- `close_driver()` - Close WebDriver
- `take_screenshot(filename)` - Take screenshot

---

## 🔍 Test Markers

```bash
# Smoke tests - Quick validation tests
@pytest.mark.smoke

# Regression tests - Full test suite
@pytest.mark.regression

# Feature-specific markers
@pytest.mark.add_expense
@pytest.mark.delete_expense
@pytest.mark.clear_expenses
```

---

## 📝 Pytest Configuration (pytest.ini)

Key configurations:
- Test discovery patterns
- Allure report directory: `allure-results`
- Timeout: 300 seconds per test
- Logging enabled with file output
- Custom markers defined

---

## 🐛 Troubleshooting

### ChromeDriver Issues

```bash
# Download correct ChromeDriver version
# Match your Chrome version from:
# chrome://version/

# Add to PATH or specify in code:
options.add_argument(f"webdriver.chrome.driver=/path/to/chromedriver")
```

### Port Already in Use

If port 5000 is already in use:
1. Update the base URL in conftest.py
2. Or stop the Flask app: Press Ctrl+C in Flask terminal

### Tests Timeout

Increase timeout in pytest.ini:
```ini
timeout = 600  # 10 minutes
```

### Selenium Not Found

```bash
pip install --upgrade selenium
```

### Allure Not Found

```bash
pip install allure-pytest
# And install Allure CLI from: https://github.com/allure-framework/allure2/releases
```

---

## 📋 CI/CD Integration

### GitHub Actions Example

```yaml
name: Test Automation

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.10'
      - run: pip install -r requirements-test.txt
      - run: pytest TestAutomation/Tests/ExpenseTest.py --alluredir=allure-results
      - uses: actions/upload-artifact@v2
        with:
          name: allure-results
          path: allure-results/
```

---

## ✅ Best Practices

1. **Use Page Object Model** - Encapsulate UI interactions
2. **Meaningful Test Names** - Self-documenting test cases
3. **Setup & Teardown** - Use fixtures for initialization
4. **Logging** - Enable detailed logging for debugging
5. **Screenshots** - Automatic on failure
6. **Markers** - Organize tests by type and feature
7. **Assertions** - Use meaningful assertion messages
8. **Waits** - Use explicit waits instead of sleep()
9. **Data Isolation** - Clear data between tests
10. **Parallel Execution** - Use pytest-xdist for speed

---

## 📞 Support

For issues or questions:
1. Check the logs in `Logs/` directory
2. Review Allure reports for detailed test information
3. Enable debug logging for more details
4. Check screenshots in `Screenshots/` directory on failures

---

## 📄 License

This test automation framework is provided for testing the Expense Tracker application.

---

**Version**: 1.0.0  
**Last Updated**: February 2026  
**Framework**: Selenium + Pytest + Allure
