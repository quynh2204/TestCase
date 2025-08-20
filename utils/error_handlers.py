"""
Error handling utilities for test automation
"""

import logging
import traceback
from datetime import datetime
from typing import Dict, Any
import os

class ErrorHandlers:
    """Error handling utilities"""
    
    @staticmethod
    def setup_logging(log_level=logging.INFO):
        """
        Setup logging configuration
        
        Args:
            log_level: Logging level
        """
        log_dir = "reports/logs"
        os.makedirs(log_dir, exist_ok=True)
        
        log_filename = f"{log_dir}/test_execution_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        
        logging.basicConfig(
            level=log_level,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_filename, encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        
        return log_filename
    
    @staticmethod
    def handle_selenium_error(error: Exception, driver=None, test_name: str = "") -> Dict[str, Any]:
        """
        Handle Selenium-specific errors
        
        Args:
            error: Exception object
            driver: WebDriver instance
            test_name: Name of the test
            
        Returns:
            dict: Error information
        """
        error_info = {
            "error_type": type(error).__name__,
            "error_message": str(error),
            "test_name": test_name,
            "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "traceback": traceback.format_exc()
        }
        
        # Take screenshot if driver is available
        if driver:
            try:
                screenshot_path = f"reports/screenshots/error_{test_name}_{int(datetime.now().timestamp())}.png"
                driver.save_screenshot(screenshot_path)
                error_info["screenshot"] = screenshot_path
                logging.info(f"Error screenshot saved: {screenshot_path}")
            except:
                logging.warning("Failed to take error screenshot")
        
        # Log error
        logging.error(f"Selenium error in {test_name}: {error_info['error_message']}")
        logging.debug(f"Full traceback: {error_info['traceback']}")
        
        return error_info
    
    @staticmethod
    def categorize_error(error: Exception) -> str:
        """
        Categorize error type for reporting
        
        Args:
            error: Exception object
            
        Returns:
            str: Error category
        """
        error_type = type(error).__name__
        
        selenium_errors = [
            "NoSuchElementException", "ElementNotInteractableException",
            "TimeoutException", "StaleElementReferenceException",
            "ElementClickInterceptedException"
        ]
        
        if error_type in selenium_errors:
            return "SELENIUM_ERROR"
        elif "Connection" in error_type or "Network" in error_type:
            return "NETWORK_ERROR"
        elif "Permission" in error_type or "Access" in error_type:
            return "PERMISSION_ERROR"
        else:
            return "GENERAL_ERROR"