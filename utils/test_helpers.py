"""
Helper functions cho automation testing
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import logging
from config.settings import *

class TestHelpers:
    """Helper methods cho testing"""
    
    @staticmethod
    def find_element_by_multiple_selectors(driver, wait, selectors, timeout=10):
        """
        Tìm element bằng nhiều selectors
        
        Args:
            driver: WebDriver instance
            wait: WebDriverWait instance
            selectors: List of selectors to try
            timeout: Timeout in seconds
            
        Returns:
            WebElement or None
        """
        for selector in selectors:
            try:
                if selector.startswith("//"):
                    # XPath selector
                    element = WebDriverWait(driver, timeout).until(
                        EC.presence_of_element_located((By.XPATH, selector))
                    )
                else:
                    # CSS selector
                    element = WebDriverWait(driver, timeout).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                    )
                logging.info(f"Element found with selector: {selector}")
                return element
            except TimeoutException:
                continue
        
        logging.warning(f"Element not found with any of the selectors: {selectors}")
        return None
    
    @staticmethod
    def safe_click(driver, element, use_javascript=False):
        """
        An toàn click element
        
        Args:
            driver: WebDriver instance
            element: WebElement to click
            use_javascript: Use JavaScript click if True
            
        Returns:
            bool: Success status
        """
        try:
            # Scroll to element
            driver.execute_script("arguments[0].scrollIntoView(true);", element)
            time.sleep(0.5)
            
            if use_javascript:
                driver.execute_script("arguments[0].click();", element)
            else:
                element.click()
            
            logging.info("Element clicked successfully")
            return True
            
        except Exception as e:
            logging.error(f"Failed to click element: {str(e)}")
            return False
    
    @staticmethod
    def safe_send_keys(driver, element, text, clear_first=True):
        """
        An toàn nhập text vào element
        
        Args:
            driver: WebDriver instance
            element: WebElement to send keys to
            text: Text to send
            clear_first: Clear field before sending keys
            
        Returns:
            bool: Success status
        """
        try:
            # Scroll to element
            driver.execute_script("arguments[0].scrollIntoView(true);", element)
            time.sleep(0.5)
            
            if clear_first:
                element.clear()
            
            element.send_keys(str(text))
            logging.info(f"Text '{text}' sent to element successfully")
            return True
            
        except Exception as e:
            logging.error(f"Failed to send keys to element: {str(e)}")
            return False
    
    @staticmethod
    def take_screenshot(driver, filename):
        """
        Chụp ảnh màn hình
        
        Args:
            driver: WebDriver instance
            filename: Filename for screenshot
            
        Returns:
            str: Path to screenshot file
        """
        try:
            screenshot_path = f"{SCREENSHOT_DIR}/{filename}_{int(time.time())}.png"
            driver.save_screenshot(screenshot_path)
            logging.info(f"Screenshot saved: {screenshot_path}")
            return screenshot_path
        except Exception as e:
            logging.error(f"Failed to take screenshot: {str(e)}")
            return None