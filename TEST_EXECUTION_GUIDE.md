# Test Automation Execution Guide

## Overview

This guide provides step-by-step instructions to run the test automation framework for the Expense Tracker application.

---

## Prerequisites Before Running Tests

### 1. Flask Application Must Be Running

The tests require the Expense Tracker Flask app to be running on `http://127.0.0.1:5000`.

**Start the Flask Application:**

```bash
# Terminal 1: Start Flask (keep running)
cd c:\Automation\Assess
python app.py
```

**Expected Output:**
```
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
 * Running on http://10.0.0.136:5000
Press CTRL+C to quit
```

### 2. Chrome Browser Must Be Installed

Verify Chrome is installed:
```bash
chrome --version
# Expected: Google Chrome 121.0.6167.160
```

### 3. ChromeDriver Must Be Compatible

Verify ChromeDriver matches Chrome version:
```bash
chromedriver --version
# Expected: ChromeDriver 121.0.6167.160
```

If versions don't match, download correct ChromeDriver from:
https://chromedriver.chromium.org/

### 4. Python Dependencies Must Be Installed

Verify dependencies:
```bash
pip show selenium pytest allure-pytest
```

If not installed:
```bash
pip install -r requirements-test.txt
```

---

## Running Tests - Quick Start

### Method 1: Windows Batch Script (Recommended for Windows)

```bash
# Double-click or run
run_tests.bat
```

**Interactive Menu:**
```
[1] Run All Tests
[2] Run Add Expense Tests
[3] Run Delete Expense Tests
[4] Run Clear Expenses Tests
[5] Run Filter Tests
[6] Run Smoke Tests Only
[7] Run Regression Tests Only
[8] Run All Tests with Allure Report
[9] View Latest Allure Report
[10] Run Tests in Headless Mode
[11] Generate Allure Report
[12] Exit
```

### Method 2: Bash Script (Recommended for Linux/Mac)

```bash
chmod +x run_tests.sh
./run_tests.sh
```

### Method 3: Direct Pytest Commands (Recommended for CI/CD)

---

## Test Execution Commands

### Run All Tests

```bash
pytest TestAutomation/Tests/ExpenseTest.py -v --alluredir=allure-results
```

**Expected Output:**
```
TestAutomation/Tests/ExpenseTest.py::TestAddExpense::test_add_single_expense PASSED
TestAutomation/Tests/ExpenseTest.py::TestAddExpense::test_add_multiple_expenses PASSED
TestAutomation/Tests/ExpenseTest.py::TestAddExpense::test_add_expense_with_custom_date PASSED
...
======================== 20 passed in 2m 15s ========================
```

### Run Specific Test Suite

```bash
# Add Expense Tests
pytest TestAutomation/Tests/ExpenseTest.py::TestAddExpense -v --alluredir=allure-results

# Delete Expense Tests
pytest TestAutomation/Tests/ExpenseTest.py::TestDeleteExpense -v --alluredir=allure-results

# Clear Expenses Tests
pytest TestAutomation/Tests/ExpenseTest.py::TestClearExpenses -v --alluredir=allure-results

# Filter & Navigation Tests
pytest TestAutomation/Tests/ExpenseTest.py::TestFilterAndNavigation -v --alluredir=allure-results
```

### Run by Test Marker

```bash
# Smoke Tests (Quick validation)
pytest TestAutomation/Tests/ExpenseTest.py -m smoke -v --alluredir=allure-results

# Regression Tests (Full suite)
pytest TestAutomation/Tests/ExpenseTest.py -m regression -v --alluredir=allure-results

# Add Expense Tests
pytest TestAutomation/Tests/ExpenseTest.py -m add_expense -v --alluredir=allure-results

# Delete Expense Tests
pytest TestAutomation/Tests/ExpenseTest.py -m delete_expense -v --alluredir=allure-results

# Clear Expenses Tests
pytest TestAutomation/Tests/ExpenseTest.py -m clear_expenses -v --alluredir=allure-results
```

### Run Single Test Case

```bash
pytest TestAutomation/Tests/ExpenseTest.py::TestAddExpense::test_add_single_expense -v --alluredir=allure-results
```

### Run Tests in Parallel

```bash
# 4 parallel workers
pytest TestAutomation/Tests/ExpenseTest.py -n 4 -v --alluredir=allure-results
```

### Run with Custom Timeout

```bash
# 10 minute timeout per test
pytest TestAutomation/Tests/ExpenseTest.py --timeout=600 -v --alluredir=allure-results
```

### Run Headless Mode (No Browser Window)

```bash
# Edit conftest.py first and change:
# browser_driver = DriverFactory.get_chrome_driver(headless=True)

pytest TestAutomation/Tests/ExpenseTest.py -v --alluredir=allure-results
```

### Generate HTML Report

```bash
pytest TestAutomation/Tests/ExpenseTest.py --html=report.html --self-contained-html -v
```

---

## Expected Test Results

### Successful Test Run

```bash
$ pytest TestAutomation/Tests/ExpenseTest.py -v --alluredir=allure-results

TestAutomation/Tests/ExpenseTest.py::TestAddExpense::test_add_single_expense PASSED
TestAutomation/Tests/ExpenseTest.py::TestAddExpense::test_add_multiple_expenses PASSED
TestAutomation/Tests/ExpenseTest.py::TestAddExpense::test_add_expense_with_custom_date PASSED
TestAutomation/Tests/ExpenseTest.py::TestAddExpense::test_add_expense_all_categories PASSED
TestAutomation/Tests/ExpenseTest.py::TestAddExpense::test_total_amount_calculation PASSED
TestAutomation/Tests/ExpenseTest.py::TestDeleteExpense::test_delete_single_expense PASSED
TestAutomation/Tests/ExpenseTest.py::TestDeleteExpense::test_delete_multiple_expenses PASSED
TestAutomation/Tests/ExpenseTest.py::TestDeleteExpense::test_total_updates_after_deletion PASSED
TestAutomation/Tests/ExpenseTest.py::TestClearExpenses::test_clear_all_expenses PASSED
TestAutomation/Tests/ExpenseTest.py::TestClearExpenses::test_total_zero_after_clear PASSED
TestAutomation/Tests/ExpenseTest.py::TestClearExpenses::test_add_after_clear PASSED
TestAutomation/Tests/ExpenseTest.py::TestFilterAndNavigation::test_filter_by_category PASSED
TestAutomation/Tests/ExpenseTest.py::TestFilterAndNavigation::test_get_all_expenses PASSED

======================== 20 passed in 2m 15s ========================
```

### Failed Test Example

```bash
TestAutomation/Tests/ExpenseTest.py::TestAddExpense::test_add_single_expense FAILED

________________________ test_add_single_expense _________________________

assert found, "Expense 'Lunch at restaurant' not found in table"

E   AssertionError: Expense 'Lunch at restaurant' not found in table

TestAutomation/Tests/ExpenseTest.py:45: AssertionError
```

---

## Generating Allure Reports

### Option 1: Live Report Server (Recommended)

```bash
# Serve reports with live statistics
allure serve allure-results

# This opens browser automatically at http://127.0.0.1:4040
```

### Option 2: Generate Static HTML

```bash
# Generate static HTML report
allure generate allure-results --clean -o allure-report

# Open report
start allure-report/index.html  # Windows
open allure-report/index.html   # macOS
xdg-open allure-report/index.html  # Linux
```

### Report Contents

The Allure report includes:

✓ Overview with total tests, passed, failed, skipped
✓ Behaviors grouped by Feature/Suite
✓ Test steps with timestamps
✓ Screenshots (on failures)
✓ Logs (accessible from each test)
✓ Timing information
✓ Historical trends (if run multiple times)

---

## Test Execution Flow

### What Happens During Test Execution

1. **Fixture Setup**
   - Chrome browser launched
   - WebDriver initialized
   - Window maximized
   - Logger started

2. **Test Execution**
   - Navigate to application
   - Execute test actions
   - Verify results
   - Assert expectations

3. **Verification**
   - Success/error messages checked
   - Data integrity validated
   - UI state confirmed

4. **Cleanup**
   - Browser closed
   - Logs written
   - Report artifact saved

### Test Output Files

**After running tests, you'll have:**

```
Logs/
├── automation_20260209_143022.log      # Detailed execution log
├── automation_20260209_143525.log
└── automation_20260209_144102.log

Screenshots/
├── failure_test_add_expense.png        # Failure screenshots
└── failure_test_delete_expense.png

allure-results/
├── 1234567890-container.json          # Allure results
├── 1234567891-result.json
└── executor.json

allure-report/                          # Generated HTML report
├── index.html
├── data/
├── css/
└── js/
```

---

## Debugging Failed Tests

### 1. Check Logs

```bash
# Most recent log file
type Logs/*.log | tail -20

cat Logs/automation_*.log | grep ERROR
```

### 2. Review Screenshots

```bash
# Open screenshot from failure
start Screenshots/failure_*.png
```

### 3. View Allure Report

```bash
# Click on failed test in Allure report
# Scroll down to see:
# - Test steps
# - Screenshots
# - Logs
# - Timing information
```

### 4. Run Single Test with Maximum Verbosity

```bash
pytest TestAutomation/Tests/ExpenseTest.py::TestAddExpense::test_add_single_expense -vv --tb=short
```

### 5. Common Issues & Solutions

**Issue: "Chrome version mismatch"**
```bash
# Check Chrome version
chrome --version

# Download matching ChromeDriver
# https://chromedriver.chromium.org/
```

**Issue: "Port 5000 already in use"**
```bash
# Stop Flask app and restart
# Or modify base URL in conftest.py
```

**Issue: "Element not found"**
```bash
# Increase wait timeout in UtilLib.py
# Check if application UI changed
# Verify Flask app is running
```

**Issue: "Alert prompt not handled"**
```bash
# Verify dismiss/accept_alert() called
# Check for multiple alerts
```

---

## Performance Optimization

### Run Tests Faster

```bash
# Parallel execution (requires pytest-xdist)
pytest TestAutomation/Tests/ExpenseTest.py -n auto

# Run only smoke tests (faster)
pytest TestAutomation/Tests/ExpenseTest.py -m smoke

# Skip screenshots on failure
# (Edit conftest.py to disable screenshot hook)
```

### Reduce Test Runtime

- Run headless mode (no UI rendering)
- Use parallel execution
- Run critical tests first
- Disable logging if not needed

---

## CI/CD Integration

### GitHub Actions Example

```yaml
name: Test Automation

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      
      - name: Install dependencies
        run: |
          python -m pip install -r requirements-test.txt
      
      - name: Run tests
        run: |
          pytest TestAutomation/Tests/ExpenseTest.py -v --alluredir=allure-results
      
      - name: Generate report
        if: always()
        run: |
          allure generate allure-results --clean -o allure-report
      
      - name: Upload report
        uses: actions/upload-artifact@v3
        if: always()
        with:
          name: allure-report
          path: allure-report/
```

---

## Best Practices

### Before Running Tests

1. ✓ Verify Flask app is running
2. ✓ Verify Chrome browser is installed
3. ✓ Verify ChromeDriver version matches
4. ✓ Check internet connection (for pip if needed)
5. ✓ Clear logs directory (optional)

### During Test Run

1. ✓ Don't close browser or terminal
2. ✓ Don't interfere with mouse/keyboard
3. ✓ Monitor system resources
4. ✓ Check for pop-ups or alerts

### After Test Run

1. ✓ Review test results
2. ✓ Check failed test logs
3. ✓ Generate Allure report
4. ✓ Archive results for future reference

---

## Troubleshooting Guide

### Tests Won't Start

**Check 1:** Is Flask running?
```bash
curl http://127.0.0.1:5000/
```

**Check 2:** Are dependencies installed?
```bash
pip list | grep selenium
```

**Check 3:** Is Python correct version?
```bash
python --version  # Should be 3.8+
```

### Tests Pass Locally but Fail in CI

**Possible Causes:**
- Different Chrome version in CI environment
- Headless mode issues
- Timing/wait issues with CI machines
- Different screen resolution

**Solutions:**
- Use headless: True in CI/CD
- Increase waits in tests
- Use --timeout more generous
- Capture screenshots in CI

### Intermittent Test Failures

**Causes:**
- Element not found (timing)
- Alert not dismissed
- Network latency
- Machine performance

**Solutions:**
- Increase wait timeouts
- Add explicit waits
- Review logs carefully
- Run tests multiple times

---

## Command Cheat Sheet

```bash
# Run all tests
pytest TestAutomation/Tests/ExpenseTest.py -v

# Run with Allure
pytest TestAutomation/Tests/ExpenseTest.py -v --alluredir=allure-results

# View report
allure serve allure-results

# Run by marker
pytest -m smoke -v --alluredir=allure-results

# Run in parallel
pytest -n 4 -v --alluredir=allure-results

# Run specific class
pytest TestAutomation/Tests/ExpenseTest.py::TestAddExpense -v

# Run specific test
pytest TestAutomation/Tests/ExpenseTest.py::TestAddExpense::test_add_single_expense -v

# Generate HTML report
allure generate allure-results -o allure-report

# Clear results
rm -rf allure-results allure-report  # Linux/Mac
rmdir /s allure-results allure-report  # Windows
```

---

## Next Steps

1. **Run first test suite**
   ```bash
   pytest TestAutomation/Tests/ExpenseTest.py::TestAddExpense -v
   ```

2. **View Allure report**
   ```bash
   allure serve allure-results
   ```

3. **Review logs**
   ```bash
   type Logs/*.log
   ```

4. **Extend tests** (optional)
   - Add more scenarios
   - Add negative tests
   - Add edge cases

---

## Support

For issues:
1. Check this guide
2. Review logs in Logs/ directory
3. Check README_AUTOMATION.md
4. Check TEST_AUTOMATION_SUMMARY.md

---

**Happy Testing! 🚀**
