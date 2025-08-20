"""
Helper functions cho automation testing
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException
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
                elif selector.startswith(".") or selector.startswith("#") or "[" in selector:
                    # CSS selector
                    element = WebDriverWait(driver, timeout).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                    )
                else:
                    # Try as CSS first, then as tag name
                    try:
                        element = WebDriverWait(driver, timeout).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                        )
                    except:
                        element = WebDriverWait(driver, timeout).until(
                            EC.presence_of_element_located((By.TAG_NAME, selector))
                        )
                
                logging.info(f"Element found with selector: {selector}")
                return element
            except TimeoutException:
                logging.debug(f"Selector failed: {selector}")
                continue
        
        logging.warning(f"Element not found with any of the selectors: {selectors}")
        return None
    
    @staticmethod
    def find_clickable_element_by_multiple_selectors(driver, wait, selectors, timeout=10):
        """
        Tìm clickable element bằng nhiều selectors
        """
        for selector in selectors:
            try:
                if selector.startswith("//"):
                    element = WebDriverWait(driver, timeout).until(
                        EC.element_to_be_clickable((By.XPATH, selector))
                    )
                else:
                    element = WebDriverWait(driver, timeout).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                    )
                
                logging.info(f"Clickable element found with selector: {selector}")
                return element
            except TimeoutException:
                continue
        
        logging.warning(f"Clickable element not found with any selectors: {selectors}")
        return None
    
    @staticmethod
    def safe_click(driver, element, use_javascript=False, max_retries=3):
        """
        An toàn click element với xử lý click interception
        
        Args:
            driver: WebDriver instance
            element: WebElement to click
            use_javascript: Use JavaScript click if True
            max_retries: Maximum number of retries
            
        Returns:
            bool: Success status
        """
        for attempt in range(max_retries):
            try:
                # Scroll to element
                driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
                time.sleep(0.5)
                
                # Wait for element to be stable
                WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable(element)
                )
                
                if use_javascript or attempt > 0:
                    # Use JavaScript click for reliability
                    driver.execute_script("arguments[0].click();", element)
                    logging.info(f"Element clicked successfully using JavaScript (attempt {attempt + 1})")
                else:
                    # Try normal click first
                    element.click()
                    logging.info(f"Element clicked successfully (attempt {attempt + 1})")
                
                return True
                
            except ElementClickInterceptedException as e:
                logging.warning(f"Click intercepted on attempt {attempt + 1}: {str(e)}")
                if attempt < max_retries - 1:
                    # Try to remove any overlay elements that might be blocking
                    driver.execute_script("""
                        var overlays = document.querySelectorAll('[class*="overlay"], [class*="modal"], [class*="popup"]');
                        for (var i = 0; i < overlays.length; i++) {
                            if (overlays[i].style.display !== 'none') {
                                overlays[i].style.display = 'none';
                            }
                        }
                    """)
                    time.sleep(0.5)
                    # Force JavaScript click on next attempt
                    use_javascript = True
                else:
                    logging.error(f"Failed to click element after {max_retries} attempts: Click intercepted")
                    return False
                    
            except Exception as e:
                logging.error(f"Failed to click element on attempt {attempt + 1}: {str(e)}")
                if attempt == max_retries - 1:
                    return False
                time.sleep(0.5)
        
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
            driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
            time.sleep(0.5)
            
            # Click to focus
            TestHelpers.safe_click(driver, element, use_javascript=True)
            
            if clear_first:
                # Clear using multiple methods
                element.clear()
                element.send_keys(Keys.CTRL + "a")
                element.send_keys(Keys.DELETE)
                time.sleep(0.2)
            
            element.send_keys(str(text))
            logging.info(f"Text '{text}' sent to element successfully")
            return True
            
        except Exception as e:
            logging.error(f"Failed to send keys to element: {str(e)}")
            return False
    
    @staticmethod
    def safe_input_quantity(driver, element, value):
        """
        An toàn nhập quantity với kiểm tra validation
        
        Args:
            driver: WebDriver instance
            element: Quantity input element
            value: Value to input
            
        Returns:
            dict: Result with success status and final value
        """
        try:
            # Scroll to element
            driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
            time.sleep(0.5)
            
            # Get initial value
            initial_value = element.get_attribute("value")
            
            # Click to focus using safe_click
            TestHelpers.safe_click(driver, element, use_javascript=True)
            
            # Clear field using multiple methods
            element.clear()
            time.sleep(0.2)
            
            # Select all and delete
            element.send_keys(Keys.CTRL + "a")
            element.send_keys(Keys.DELETE)
            time.sleep(0.2)
            
            # Input new value
            element.send_keys(str(value))
            time.sleep(0.5)
            
            # Trigger change event
            driver.execute_script("arguments[0].dispatchEvent(new Event('change'));", element)
            driver.execute_script("arguments[0].dispatchEvent(new Event('input'));", element)
            
            # Get final value to check if input was accepted
            final_value = element.get_attribute("value")
            
            return {
                "success": True,
                "initial_value": initial_value,
                "input_value": str(value),
                "final_value": final_value,
                "was_modified": final_value != str(value)
            }
            
        except Exception as e:
            logging.error(f"Failed to input quantity: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "initial_value": None,
                "input_value": str(value),
                "final_value": None
            }
    
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
    
    @staticmethod
    def wait_for_page_load(driver, timeout=30):
        """
        Chờ page load hoàn tất
        """
        try:
            WebDriverWait(driver, timeout).until(
                lambda driver: driver.execute_script("return document.readyState") == "complete"
            )
            time.sleep(1)  # Additional buffer
            return True
        except TimeoutException:
            logging.warning("Page load timeout")
            return False

    @staticmethod
    def select_category_option(driver, option_key="khac"):
        """
        Select category option using radio buttons
        
        Args:
            driver: WebDriver instance
            option_key: Key for category option (default: "khac")
            
        Returns:
            bool: Success status
        """
        try:
            from config.locators import ProductPageLocators
            
            # First try to find the specific label for the option
            if option_key in ProductPageLocators.CATEGORY_LABELS:
                selector = ProductPageLocators.CATEGORY_LABELS[option_key]
                try:
                    label_element = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                    )
                    return TestHelpers.safe_click(driver, label_element, use_javascript=True)
                except TimeoutException:
                    logging.warning(f"Specific label not found for {option_key}")
            
            # Fallback: try to find any category selection element
            for selector in ProductPageLocators.CATEGORY_SELECTION[:5]:  # Try first 5 selectors
                try:
                    if selector.startswith("//"):
                        elements = driver.find_elements(By.XPATH, selector)
                    else:
                        elements = driver.find_elements(By.CSS_SELECTOR, selector)
                    
                    if elements:
                        # Click the first available option
                        element = elements[0]
                        if TestHelpers.safe_click(driver, element, use_javascript=True):
                            logging.info(f"Category selected using selector: {selector}")
                            return True
                except Exception as e:
                    logging.debug(f"Selector failed: {selector} - {str(e)}")
                    continue
            
            logging.warning("No category selection element found")
            return False
            
        except Exception as e:
            logging.error(f"Failed to select category: {str(e)}")
            return False