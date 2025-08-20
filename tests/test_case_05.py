"""
Test Case #5: Thêm giỏ hàng không thành công khi không chọn phân loại đối tượng

Technique: Input Validation, Decision Table
Tool: Selenium
Execution: Automated
Dynamic Testing: Input Validation
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import logging

from config.settings import *
from config.locators import ProductPageLocators
from config.test_data import TestData
from utils.driver_manager import DriverManager
from utils.test_helpers import TestHelpers

class TestCase05:
    """Test Case 5: Input Validation - Không chọn phân loại"""
    
    def __init__(self):
        self.driver = None
        self.wait = None
        self.test_helpers = TestHelpers()
        self.test_data = TestData.TC5_DATA
        
    def setup(self):
        """Thiết lập test environment"""
        print("🔧 Setting up Test Case #5: Input Validation")
        self.driver = DriverManager.get_driver()
        self.wait = WebDriverWait(self.driver, EXPLICIT_WAIT)
        
    def teardown(self):
        """Dọn dẹp sau test"""
        if SCREENSHOT_ON_FAILURE:
            self.test_helpers.take_screenshot(self.driver, "TC05_final_state")
        
        if self.driver:
            time.sleep(3)  # Pause để quan sát
            self.driver.quit()
        print("🧹 Test Case #5 cleanup completed")
        
    def execute_input_validation_test(self):
        """
        Thực hiện Input Validation Testing
        
        Kiểm tra xem hệ thống có validate input đúng cách không
        """
        try:
            print("\n📋 INPUT VALIDATION TESTING")
            print("-" * 40)
            
            # Bước 1: Truy cập trang
            self.driver.get(PRODUCT_URL)
            print(f"✓ Accessed: {PRODUCT_URL}")
            
            # Bước 2: Kiểm tra form validation
            print("\n🔍 Testing form validation...")
            
            # Không chọn phân loại (theo test data)
            print("- Không chọn phân loại đối tượng")
            print("- Số lượng mặc định: 1")
            
            # Bước 3: Thử submit form mà không chọn required field
            add_to_cart_btn = self.test_helpers.find_element_by_multiple_selectors(
                self.driver, self.wait, ProductPageLocators.ADD_TO_CART_BUTTON
            )
            
            if not add_to_cart_btn:
                return {"status": "FAILED", "message": "Không tìm thấy button 'Thêm vào giỏ hàng'"}
            
            # Click button để trigger validation
            success = self.test_helpers.safe_click(self.driver, add_to_cart_btn)
            if not success:
                return {"status": "FAILED", "message": "Không thể click button"}
            
            print("✓ Đã click 'Thêm vào giỏ hàng' mà không chọn phân loại")
            
            # Bước 4: Kiểm tra validation message
            print("\n🔍 Checking validation result...")
            
            error_element = self.test_helpers.find_element_by_multiple_selectors(
                self.driver, self.wait, ProductPageLocators.ERROR_MESSAGE, timeout=5
            )
            
            if not error_element:
                # Thử tìm bằng text content
                try:
                    error_element = self.wait.until(
                        EC.presence_of_element_located((By.XPATH, 
                            f"//*[contains(text(), '{self.test_data['expected_message']}')]"))
                    )
                except:
                    return {
                        "status": "FAILED", 
                        "message": "Không có validation message nào xuất hiện"
                    }
            
            actual_message = error_element.text
            expected_message = self.test_data['expected_message']
            
            print(f"Expected: '{expected_message}'")
            print(f"Actual: '{actual_message}'")
            
            # Validation
            if expected_message in actual_message:
                return {
                    "status": "PASSED",
                    "message": f"Input validation hoạt động đúng: '{actual_message}'"
                }
            else:
                return {
                    "status": "FAILED",
                    "message": f"Validation message không đúng. Expected: '{expected_message}', Actual: '{actual_message}'"
                }
                
        except Exception as e:
            return {"status": "ERROR", "message": f"Lỗi trong input validation test: {str(e)}"}
    
    def execute_decision_table_test(self):
        """
        Thực hiện Decision Table Testing
        
        Test các quyết định của hệ thống dựa trên input combinations
        """
        print("\n📊 DECISION TABLE TESTING")
        print("-" * 40)
        
        # Decision table cho test case này:
        # Category Selected | Quantity | Expected Result
        # No               | 1        | Show error message
        # Yes              | 1        | Add to cart (not tested here)
        
        decision_table = [
            {
                "category_selected": False,
                "quantity": 1,
                "expected_result": "error_message",
                "description": "Không chọn phân loại, số lượng hợp lệ"
            }
        ]
        
        for scenario in decision_table:
            print(f"\n🧪 Testing scenario: {scenario['description']}")
            print(f"   Category: {'Selected' if scenario['category_selected'] else 'Not Selected'}")
            print(f"   Quantity: {scenario['quantity']}")
            print(f"   Expected: {scenario['expected_result']}")
            
            # Đây là scenario chính của test case này
            result = self.execute_input_validation_test()
            return result
    
    def run_test(self):
        """Chạy full test case với cả hai techniques"""
        try:
            self.setup()
            
            print("=" * 60)
            print("TEST CASE #5: Input Validation + Decision Table Testing")
            print("=" * 60)
            print(f"User: {CURRENT_USER}")
            print(f"Date: {TEST_DATE}")
            print(f"Technique: Input Validation, Decision Table")
            print(f"Tool: Selenium")
            print(f"Dynamic Testing: Input Validation")
            
            # Thực hiện decision table test (bao gồm input validation)
            result = self.execute_decision_table_test()
            
            print(f"\n🏁 FINAL RESULT: {result['status']}")
            print(f"📝 Message: {result['message']}")
            
            return result
            
        except Exception as e:
            error_msg = f"Test execution error: {str(e)}"
            print(f"💥 ERROR: {error_msg}")
            return {"status": "ERROR", "message": error_msg}
        finally:
            self.teardown()

def run_test_case_05():
    """Entry point cho Test Case 5"""
    test = TestCase05()
    return test.run_test()

if __name__ == "__main__":
    result = run_test_case_05()
    print(f"\n🎯 Test Case #5 Result: {result['status']}")