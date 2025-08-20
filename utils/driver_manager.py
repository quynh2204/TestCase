"""
Quản lý WebDriver với các tính năng nâng cao
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from config.settings import *
import logging

class DriverManager:
    """Quản lý WebDriver instance"""
    
    @staticmethod
    def get_driver():
        """
        Tạo và cấu hình WebDriver
        
        Returns:
            WebDriver: Configured driver instance
        """
        try:
            if BROWSER.lower() == "chrome":
                options = Options()
                
                # Basic options
                if HEADLESS:
                    options.add_argument("--headless")
                
                # Performance and stability options
                options.add_argument("--no-sandbox")
                options.add_argument("--disable-dev-shm-usage")
                options.add_argument("--disable-gpu")
                options.add_argument(f"--window-size={WINDOW_SIZE}")
                options.add_argument("--disable-web-security")
                options.add_argument("--allow-running-insecure-content")
                
                # Auto-download ChromeDriver
                service = Service(ChromeDriverManager().install())
                driver = webdriver.Chrome(service=service, options=options)
                
            else:
                raise ValueError(f"Browser '{BROWSER}' not supported yet")
            
            # Configure timeouts
            driver.implicitly_wait(IMPLICIT_WAIT)
            driver.set_page_load_timeout(PAGE_LOAD_TIMEOUT)
            
            if not HEADLESS:
                driver.maximize_window()
            
            logging.info(f"WebDriver initialized successfully: {BROWSER}")
            return driver
            
        except Exception as e:
            logging.error(f"Failed to initialize WebDriver: {str(e)}")
            raise