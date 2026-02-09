#!/usr/bin/env python
"""
Quick Start Script for Test Automation Framework Setup
This script helps set up and run tests with Allure reports.
"""

import subprocess
import sys
import os


def print_header(text):
    """Print formatted header."""
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60 + "\n")


def run_command(cmd, description):
    """Run a shell command."""
    print(f"▶ {description}...")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✓ {description} - SUCCESS\n")
            return True
        else:
            print(f"✗ {description} - FAILED")
            if result.stderr:
                print(f"Error: {result.stderr}\n")
            return False
    except Exception as e:
        print(f"✗ Error: {str(e)}\n")
        return False


def main():
    """Main setup function."""
    print_header("Test Automation Framework - Quick Start")
    
    # Check Python version
    print("Checking Python version...")
    version = sys.version_info
    print(f"Python {version.major}.{version.minor}.{version.micro}")
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 or higher is required")
        sys.exit(1)
    print("✓ Python version OK\n")
    
    # Install dependencies
    print_header("Installing Dependencies")
    if not run_command(
        "pip install -r requirements-test.txt",
        "Installing test dependencies"
    ):
        print("⚠ Some dependencies may not have installed correctly")
    
    # Check Chrome and ChromeDriver
    print_header("Checking Browser Setup")
    run_command("chrome --version", "Checking Chrome version")
    run_command("chromedriver --version", "Checking ChromeDriver version")
    
    print_header("Setup Complete!")
    print("""
🎯 Next Steps:

1. START THE FLASK APPLICATION:
   python app.py
   
   (Keep it running in a separate terminal)

2. RUN ALL TESTS:
   pytest TestAutomation/Tests/ExpenseTest.py -v --alluredir=allure-results

3. RUN SPECIFIC TEST SUITE:
   pytest TestAutomation/Tests/ExpenseTest.py::TestAddExpense -v --alluredir=allure-results
   pytest TestAutomation/Tests/ExpenseTest.py::TestDeleteExpense -v --alluredir=allure-results
   pytest TestAutomation/Tests/ExpenseTest.py::TestClearExpenses -v --alluredir=allure-results

4. RUN SMOKE TESTS ONLY:
   pytest TestAutomation/Tests/ExpenseTest.py -m smoke -v --alluredir=allure-results

5. GENERATE ALLURE REPORT:
   allure serve allure-results

📊 Test Results:
   - Logs: Logs/automation_YYYYMMDD_HHMMSS.log
   - Screenshots: Screenshots/ (on failures)
   - Allure Reports: allure-results/

📖 Documentation:
   Read README_AUTOMATION.md for detailed information and examples.

✨ Quick Command Reference:
   
   # Run all tests with Allure
   pytest TestAutomation/Tests/ExpenseTest.py -v --alluredir=allure-results
   
   # View test report
   allure serve allure-results
   
   # Run tests in parallel (4 workers)
   pytest TestAutomation/Tests/ExpenseTest.py -v -n 4 --alluredir=allure-results
   
   # Run with custom marker
   pytest TestAutomation/Tests/ExpenseTest.py -m add_expense -v --alluredir=allure-results

💡 Tips:
   - Keep the Flask application running on http://127.0.0.1:5000
   - Check logs in Logs/ directory for debugging
   - Screenshots are saved on test failures
   - Use allure serve to view interactive reports
    """)


if __name__ == "__main__":
    main()
