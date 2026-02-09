"""
Utility Library for Web Automation Tests
Contains common functions for driver setup, logging, and wait operations.
"""

import logging
import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service


class Logger:
    """Custom logger for test execution."""
    
    @staticmethod
    def get_logger(logger_name):
        """Create and configure logger."""
        log_dir = "Logs"
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        log_file = os.path.join(log_dir, f"automation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
        
        logger = logging.getLogger(logger_name)
        logger.setLevel(logging.DEBUG)
        
        # File handler
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # Add handlers
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        
        return logger


class DriverFactory:
    """Factory class for creating WebDriver instances."""
    
    @staticmethod
    def get_chrome_driver(headless=False):
        """
        Create and return a Chrome WebDriver instance.
        
        Args:
            headless (bool): Run browser in headless mode
            
        Returns:
            WebDriver: Configured Chrome driver instance
        """
        logger = Logger.get_logger(__name__)
        
        options = webdriver.ChromeOptions()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-plugins")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)
        
        if headless:
            options.add_argument("--headless")
        
        # Set window size
        options.add_argument("--window-size=1920,1080")
        
        driver = webdriver.Chrome(options=options)
        # Set implicit wait for all elements
        driver.implicitly_wait(10)
        logger.info("Chrome WebDriver initialized successfully")
        
        return driver


class WaitMethods:
    """Common wait methods for element interactions."""
    
    def __init__(self, driver, timeout=10):
        """
        Initialize wait methods.
        
        Args:
            driver: WebDriver instance
            timeout (int): Default timeout in seconds
        """
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)
        self.logger = Logger.get_logger(__name__)
    
    def wait_for_element_visible(self, locator, timeout=None):
        """Wait for element to be visible."""
        timeout = timeout or self.wait._timeout
        self.logger.info(f"Waiting for element {locator} to be visible")
        return self.wait.until(EC.visibility_of_element_located(locator))
    
    def wait_for_element_clickable(self, locator, timeout=None):
        """Wait for element to be clickable."""
        timeout = timeout or self.wait._timeout
        self.logger.info(f"Waiting for element {locator} to be clickable")
        return self.wait.until(EC.element_to_be_clickable(locator))
    
    def wait_for_element_presence(self, locator, timeout=None):
        """Wait for element to be present in DOM."""
        timeout = timeout or self.wait._timeout
        self.logger.info(f"Waiting for element {locator} to be present")
        return self.wait.until(EC.presence_of_all_elements_located(locator))
    
    def wait_for_text_in_element(self, locator, text, timeout=None):
        """Wait for specific text in element."""
        timeout = timeout or self.wait._timeout
        self.logger.info(f"Waiting for text '{text}' in element {locator}")
        return self.wait.until(EC.text_to_be_present_in_element(locator, text))
    
    def wait_for_element_to_disappear(self, locator, timeout=None):
        """Wait for element to disappear from DOM."""
        timeout = timeout or self.wait._timeout
        self.logger.info(f"Waiting for element {locator} to disappear")
        return self.wait.until(EC.invisibility_of_element_located(locator))


class Actions:
    """Common action methods for element interactions."""
    
    def __init__(self, driver):
        """
        Initialize actions.
        
        Args:
            driver: WebDriver instance
        """
        self.driver = driver
        self.wait_methods = WaitMethods(driver)
        self.logger = Logger.get_logger(__name__)
    
    def click_element(self, locator):
        """Click on an element."""
        import time
        self.logger.info(f"Clicking element {locator}")
        element = self.wait_methods.wait_for_element_clickable(locator)
        element.click()
        time.sleep(0.5)  # Wait for page to update after click
    
    def enter_text(self, locator, text):
        """Enter text in an input field."""
        import time
        self.logger.info(f"Entering text '{text}' in element {locator}")
        element = self.wait_methods.wait_for_element_visible(locator)
        element.clear()
        element.send_keys(text)
        time.sleep(0.2)  # Allow text to process
    
    def get_text(self, locator):
        """Get text from an element."""
        self.logger.info(f"Getting text from element {locator}")
        element = self.wait_methods.wait_for_element_visible(locator)
        return element.text
    
    def get_element_count(self, locator):
        """Get count of elements matching locator."""
        self.logger.info(f"Getting count of elements {locator}")
        elements = self.driver.find_elements(*locator)
        return len(elements)
    
    def is_element_visible(self, locator, timeout=5):
        """Check if element is visible."""
        self.logger.info(f"Checking if element {locator} is visible")
        try:
            self.wait_methods.wait_for_element_visible(locator, timeout)
            return True
        except:
            return False
    
    def select_from_dropdown(self, locator, value):
        """Select value from dropdown by value."""
        self.logger.info(f"Selecting '{value}' from dropdown {locator}")
        element = self.wait_methods.wait_for_element_clickable(locator)
        element.click()
        
        # Wait for dropdown to open and select option
        option_locator = (By.XPATH, f"/option[contains(text(), '{value}')]")
        option = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(option_locator)
        )
        option.click()
    
    def select_from_html_select(self, locator, value):
        """Select value from HTML select using value attribute."""
        self.logger.info(f"Selecting '{value}' from select element {locator}")
        from selenium.webdriver.support.select import Select
        element = self.wait_methods.wait_for_element_visible(locator)
        select = Select(element)
        select.select_by_value(value)
    
    def accept_alert(self, text=None):
        """Accept browser alert."""
        self.logger.info("Accepting browser alert")
        alert = WebDriverWait(self.driver, 10).until(EC.alert_is_present())
        if text:
            self.logger.info(f"Alert text: {alert.text}")
        alert.accept()
    
    def dismiss_alert(self):
        """Dismiss browser alert."""
        self.logger.info("Dismissing browser alert")
        alert = WebDriverWait(self.driver, 10).until(EC.alert_is_present())
        alert.dismiss()


class CommonMethods:
    """Common methods for test setup and navigation."""
    
    def __init__(self, driver, base_url="http://127.0.0.1:5000"):
        """
        Initialize common methods.
        
        Args:
            driver: WebDriver instance
            base_url (str): Base URL of application
        """
        self.driver = driver
        self.base_url = base_url
        self.logger = Logger.get_logger(__name__)
    
    def navigate_to_url(self, url=None):
        """Navigate to URL."""
        target_url = url or self.base_url
        self.logger.info(f"Navigating to URL: {target_url}")
        self.driver.get(target_url)
    
    def refresh_page(self):
        """Refresh the current page."""
        self.logger.info("Refreshing page")
        self.driver.refresh()
    
    def get_current_url(self):
        """Get current URL."""
        return self.driver.current_url
    
    def get_page_title(self):
        """Get page title."""
        return self.driver.title
    
    def maximize_window(self):
        """Maximize browser window."""
        self.logger.info("Maximizing window")
        self.driver.maximize_window()
    
    def close_driver(self):
        """Close WebDriver."""
        self.logger.info("Closing WebDriver")
        self.driver.quit()
    
    def take_screenshot(self, filename=None):
        """Take screenshot."""
        if not filename:
            filename = f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        
        screenshot_dir = "Screenshots"
        if not os.path.exists(screenshot_dir):
            os.makedirs(screenshot_dir)
        
        filepath = os.path.join(screenshot_dir, filename)
        self.driver.save_screenshot(filepath)
        self.logger.info(f"Screenshot saved: {filepath}")
        return filepath
