"""
Pytest Configuration and Fixtures
Provides common fixtures for WebDriver initialization and teardown.
"""

import pytest
import allure
from TestAutomation.Utils.UtilLib import DriverFactory, CommonMethods, Logger
from TestAutomation.Pages.ExpensePage import ExpensePage


@pytest.fixture(scope="function")
def driver():
    """
    Fixture to initialize and teardown WebDriver.
    
    Yields:
        WebDriver: Configured Chrome driver instance
    """
    logger = Logger.get_logger(__name__)
    logger.info("=" * 50)
    logger.info("Initializing WebDriver")
    logger.info("=" * 50)
    
    # Initialize driver
    browser_driver = DriverFactory.get_chrome_driver(headless=False)
    browser_driver.maximize_window()
    
    yield browser_driver
    
    # Teardown
    logger.info("=" * 50)
    logger.info("Closing WebDriver")
    logger.info("=" * 50)
    browser_driver.quit()


@pytest.fixture(scope="function")
def common_methods(driver):
    """
    Fixture to initialize CommonMethods.
    
    Args:
        driver: WebDriver fixture
        
    Yields:
        CommonMethods: Instance of CommonMethods class
    """
    return CommonMethods(driver, base_url="http://127.0.0.1:5000")


@pytest.fixture(scope="function")
def expense_page(driver):
    """
    Fixture to initialize ExpensePage.
    
    Args:
        driver: WebDriver fixture
        
    Yields:
        ExpensePage: Instance of ExpensePage class
    """
    return ExpensePage(driver)


@pytest.fixture(scope="function")
def navigate_to_app(common_methods):
    """
    Fixture to navigate to the application.
    
    Args:
        common_methods: CommonMethods fixture
        
    Yields:
        CommonMethods: Instance with navigation completed
    """
    common_methods.navigate_to_url()
    yield common_methods


@pytest.fixture(scope="function", autouse=True)
def setup_teardown(request, driver):
    """
    Setup and teardown for each test.
    
    Args:
        request: Pytest request object
        driver: WebDriver fixture
    """
    logger = Logger.get_logger(__name__)
    
    # Setup
    logger.info(f"\n{'='*50}")
    logger.info(f"TEST STARTED: {request.node.name}")
    logger.info(f"{'='*50}\n")
    
    # Add test name to allure
    allure.dynamic.title(request.node.name)
    
    yield
    
    # Teardown
    logger.info(f"\n{'='*50}")
    logger.info(f"TEST COMPLETED: {request.node.name}")
    logger.info(f"Status: {request.node.rep_call.outcome if hasattr(request.node, 'rep_call') else 'Unknown'}")
    logger.info(f"{'='*50}\n")


def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line(
        "markers", "smoke: mark test as smoke test"
    )
    config.addinivalue_line(
        "markers", "regression: mark test as regression test"
    )
    config.addinivalue_line(
        "markers", "add_expense: mark test as add expense test"
    )
    config.addinivalue_line(
        "markers", "delete_expense: mark test as delete expense test"
    )
    config.addinivalue_line(
        "markers", "clear_expenses: mark test as clear expenses test"
    )


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook to capture test result and take screenshot on failure."""
    outcome = yield
    rep = outcome.get_result()
    
    # Capture screenshot on failure
    if rep.failed and "driver" in item.fixturenames:
        driver = item.funcargs.get("driver")
        if driver:
            logger = Logger.get_logger(__name__)
            screenshot_path = CommonMethods(driver).take_screenshot(
                f"failure_{item.name}.png"
            )
            # Attach screenshot to allure report
            allure.attach.file(
                screenshot_path,
                name=f"failure_{item.name}",
                attachment_type=allure.attachment_type.PNG
            )
            logger.error(f"Test failed. Screenshot saved: {screenshot_path}")
