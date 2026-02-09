@echo off
REM Test Automation Execution Script for Expense Tracker
REM Windows Batch Script

setlocal enabledelayedexpansion

cls
echo ============================================================
echo     Expense Tracker - Test Automation Framework
echo ============================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    pause
    exit /b 1
)

echo [1] Run All Tests
echo [2] Run Add Expense Tests
echo [3] Run Delete Expense Tests
echo [4] Run Clear Expenses Tests
echo [5] Run Filter Tests
echo [6] Run Smoke Tests Only
echo [7] Run Regression Tests Only
echo [8] Run All Tests with Allure Report
echo [9] View Latest Allure Report
echo [10] Run Tests in Headless Mode
echo [11] Generate Allure Report
echo [12] Exit
echo.

set /p choice="Enter your choice (1-12): "

if "%choice%"=="1" (
    echo Running all tests...
    pytest TestAutomation/Tests/ExpenseTest.py -v --alluredir=allure-results
) else if "%choice%"=="2" (
    echo Running Add Expense tests...
    pytest TestAutomation/Tests/ExpenseTest.py::TestAddExpense -v --alluredir=allure-results
) else if "%choice%"=="3" (
    echo Running Delete Expense tests...
    pytest TestAutomation/Tests/ExpenseTest.py::TestDeleteExpense -v --alluredir=allure-results
) else if "%choice%"=="4" (
    echo Running Clear Expenses tests...
    pytest TestAutomation/Tests/ExpenseTest.py::TestClearExpenses -v --alluredir=allure-results
) else if "%choice%"=="5" (
    echo Running Filter and Navigation tests...
    pytest TestAutomation/Tests/ExpenseTest.py::TestFilterAndNavigation -v --alluredir=allure-results
) else if "%choice%"=="6" (
    echo Running Smoke tests...
    pytest TestAutomation/Tests/ExpenseTest.py -m smoke -v --alluredir=allure-results
) else if "%choice%"=="7" (
    echo Running Regression tests...
    pytest TestAutomation/Tests/ExpenseTest.py -m regression -v --alluredir=allure-results
) else if "%choice%"=="8" (
    echo Running all tests with Allure report...
    pytest TestAutomation/Tests/ExpenseTest.py -v --alluredir=allure-results
    echo.
    echo Generating Allure report...
    allure generate allure-results --clean -o allure-report
    echo Report generated in allure-report/ directory
) else if "%choice%"=="9" (
    echo Viewing Allure report...
    allure serve allure-results
) else if "%choice%"=="10" (
    echo Running tests in headless mode...
    REM Edit conftest.py to set headless=True before running this
    echo Note: Please edit conftest.py to set headless=True
    pytest TestAutomation/Tests/ExpenseTest.py -v --alluredir=allure-results
) else if "%choice%"=="11" (
    echo Generating Allure HTML report...
    allure generate allure-results --clean -o allure-report
    echo.
    echo Report generated successfully!
    echo Opening report...
    start allure-report\index.html
) else if "%choice%"=="12" (
    echo Exiting...
    exit /b 0
) else (
    echo Invalid choice. Please enter a number between 1 and 12.
    pause
    goto start
)

echo.
echo Test execution completed!
pause
