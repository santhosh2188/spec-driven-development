#!/bin/bash

# Test Automation Execution Script for Expense Tracker
# Unix/Linux/macOS Bash Script

clear

echo "============================================================"
echo "    Expense Tracker - Test Automation Framework"
echo "============================================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed or not in PATH"
    exit 1
fi

# Display menu
echo "[1] Run All Tests"
echo "[2] Run Add Expense Tests"
echo "[3] Run Delete Expense Tests"
echo "[4] Run Clear Expenses Tests"
echo "[5] Run Filter Tests"
echo "[6] Run Smoke Tests Only"
echo "[7] Run Regression Tests Only"
echo "[8] Run All Tests with Allure Report"
echo "[9] View Latest Allure Report"
echo "[10] Run Tests in Parallel (4 workers)"
echo "[11] Generate Allure Report"
echo "[12] Exit"
echo ""

read -p "Enter your choice (1-12): " choice

case $choice in
    1)
        echo "Running all tests..."
        pytest TestAutomation/Tests/ExpenseTest.py -v --alluredir=allure-results
        ;;
    2)
        echo "Running Add Expense tests..."
        pytest TestAutomation/Tests/ExpenseTest.py::TestAddExpense -v --alluredir=allure-results
        ;;
    3)
        echo "Running Delete Expense tests..."
        pytest TestAutomation/Tests/ExpenseTest.py::TestDeleteExpense -v --alluredir=allure-results
        ;;
    4)
        echo "Running Clear Expenses tests..."
        pytest TestAutomation/Tests/ExpenseTest.py::TestClearExpenses -v --alluredir=allure-results
        ;;
    5)
        echo "Running Filter and Navigation tests..."
        pytest TestAutomation/Tests/ExpenseTest.py::TestFilterAndNavigation -v --alluredir=allure-results
        ;;
    6)
        echo "Running Smoke tests..."
        pytest TestAutomation/Tests/ExpenseTest.py -m smoke -v --alluredir=allure-results
        ;;
    7)
        echo "Running Regression tests..."
        pytest TestAutomation/Tests/ExpenseTest.py -m regression -v --alluredir=allure-results
        ;;
    8)
        echo "Running all tests with Allure report..."
        pytest TestAutomation/Tests/ExpenseTest.py -v --alluredir=allure-results
        echo ""
        echo "Generating Allure report..."
        allure generate allure-results --clean -o allure-report
        echo "Report generated in allure-report/ directory"
        ;;
    9)
        echo "Viewing Allure report..."
        allure serve allure-results
        ;;
    10)
        echo "Running tests in parallel (4 workers)..."
        pytest TestAutomation/Tests/ExpenseTest.py -n 4 -v --alluredir=allure-results
        ;;
    11)
        echo "Generating Allure HTML report..."
        allure generate allure-results --clean -o allure-report
        echo ""
        echo "Report generated successfully!"
        if command -v xdg-open &> /dev/null; then
            xdg-open allure-report/index.html
        elif command -v open &> /dev/null; then
            open allure-report/index.html
        fi
        ;;
    12)
        echo "Exiting..."
        exit 0
        ;;
    *)
        echo "Invalid choice. Please enter a number between 1 and 12."
        exit 1
        ;;
esac

echo ""
echo "Test execution completed!"
