"""
Test Case #8: Thêm giỏ hàng không thành công khi số lượng nhập chữ

Technique: Equivalence Partitioning, Error Guessing
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
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
import time
import logging

from config.settings import *
from config.locators import ProductPageLocators
from config.test_data import TestData
from utils.driver_manager import DriverManager
from utils.test_helpers import TestHelpers
from utils.validation_helpers import ValidationHelpers
from utils.error_handlers import ErrorHandlers

class TestCase08:
    """Test Case 8: Input Validation - Nhập ký tự chữ"""
    
    def __init__(self):
        self.driver = None
        self.wait = None
        self.test_helpers = TestHelpers()
        self.validation_helpers = ValidationHelpers()
        self.error_handlers = ErrorHandlers()
        self.test_data = TestData.TC8_DATA
        
    def setup(self):
        """Thiết lập test environment"""
        print("🔧 Setting up Test Case #8: Input Validation - Text Input")
        self.driver = DriverManager.get_driver()
        self.wait = WebDriverWait(self.driver, EXPLICIT_WAIT)
        
    def teardown(self):
        """Dọn dẹp sau test"""
        if SCREENSHOT_ON_FAILURE:
            self.test_helpers.take_screenshot(self.driver, "TC08_final_state")
        
        if self.driver:
            time.sleep(3)
            self.driver.quit()
        print("🧹 Test Case #8 cleanup completed")
    
    def execute_equivalence_partitioning(self):
        """
        Thực hiện Equivalence Partitioning cho text input
        
        Chia input thành các partitions:
        - Valid: Positive integers (1, 2, 3...)
        - Invalid: Text characters (a, b, c, abc, e)
        - Invalid: Special characters (!@#, $%^)
        - Invalid: Mixed (1a, a1, 2b)
        """
        try:
            print("\n📊 EQUIVALENCE PARTITIONING - TEXT INPUT")
            print("-" * 50)
            
            # Get equivalence classes
            eq_classes = self.validation_helpers.get_equivalence_classes("quantity")
            
            print("🗂️ Input partitions for quantity field:")
            for partition, values in eq_classes.items():
                print(f"   {partition}: {values}")
            
            # Test với invalid_text partition (chữ "e")
            test_value = self.test_data['quantity']  # "e"
            print(f"\n🎯 Testing invalid_text partition with: '{test_value}'")
            
            # Validate input before testing
            validation_result = self.validation_helpers.validate_numeric_input(test_value)
            print(f"📋 Pre-test validation: {validation_result['message']}")
            
            return self.test_text_input(test_value)
            
        except Exception as e:
            error_info = self.error_handlers.handle_selenium_error(e, self.driver, "TC08_equivalence")
            return {"status": "ERROR", "message": f"Equivalence partitioning error: {str(e)}"}
    
    def test_text_input(self, input_value):
        """
        Test text input trong quantity field
        
        Args:
            input_value: Text value to test
            
        Returns:
            dict: Test result
        """
        print(f"\n🧪 Testing text input: '{input_value}'")
        
        # Bước 1: Truy cập trang
        self.driver.get(PRODUCT_URL)
        self.test_helpers.wait_for_page_load(self.driver)
        print(f"✓ Accessed: {PRODUCT_URL}")
        
        # Bước 2: Chọn phân loại để focus vào quantity validation
        category_dropdown = self.test_helpers.find_element_by_multiple_selectors(
            self.driver, self.wait, ProductPageLocators.CATEGORY_DROPDOWN, timeout=5
        )
        
        if category_dropdown:
            try:
                select = Select(category_dropdown)
                if len(select.options) > 1:
                    select.select_by_index(1)
                    print("✓ Đã chọn phân loại đối tượng")
            except Exception as e:
                print(f"⚠️ Không thể chọn phân loại: {str(e)}")
        
        # Bước 3: Tìm quantity input field
        quantity_input = self.test_helpers.find_element_by_multiple_selectors(
            self.driver, self.wait, ProductPageLocators.QUANTITY_INPUT
        )
        
        if not quantity_input:
            return {"status": "FAILED", "message": "Không tìm thấy quantity input field"}
        
        # Bước 4: Test input behavior với text
        print(f"📝 Attempting to input text: '{input_value}'")
        
        # Sử dụng safe_input_quantity helper
        input_result = self.test_helpers.safe_input_quantity(self.driver, quantity_input, input_value)
        
        if not input_result["success"]:
            return {"status": "FAILED", "message": f"Không thể test input với giá trị '{input_value}': {input_result.get('error', '')}"}
        
        print(f"✓ Input result: '{input_result['input_value']}' → '{input_result['final_value']}'")
        
        # Kiểm tra xem input có bị filter/reject không
        if input_result["was_modified"]:
            print(f"🔒 Text input was filtered: '{input_result['input_value']}' → '{input_result['final_value']}'")
        
        # Bước 5: Thử submit để trigger validation
        add_to_cart_btn = self.test_helpers.find_clickable_element_by_multiple_selectors(
            self.driver, self.wait, ProductPageLocators.ADD_TO_CART_BUTTON
        )
        
        if not add_to_cart_btn:
            return {"status": "FAILED", "message": "Không tìm thấy button 'Thêm vào giỏ hàng'"}
        
        success = self.test_helpers.safe_click(self.driver, add_to_cart_btn)
        if not success:
            return {"status": "FAILED", "message": "Không thể click button"}
        
        print("✓ Đã click 'Thêm vào giỏ hàng'")
        
        # Bước 6: Kiểm tra validation response
        time.sleep(2)
        
        # Kiểm tra error message
        error_element = self.test_helpers.find_element_by_multiple_selectors(
            self.driver, self.wait, ProductPageLocators.ERROR_MESSAGE, timeout=5
        )
        
        expected_message = self.test_data['expected_message']
        
        if error_element and error_element.is_displayed():
            actual_message = error_element.text
            print(f"✓ Error message found: '{actual_message}'")
            
            if expected_message in actual_message or "số" in actual_message.lower() or "number" in actual_message.lower():
                return {
                    "status": "PASSED",
                    "message": f"Text input validation working correctly: '{actual_message}'"
                }
            else:
                return {
                    "status": "FAILED", 
                    "message": f"Wrong error message. Expected: '{expected_message}', Got: '{actual_message}'"
                }
        else:
            # Kiểm tra nếu field tự động clean input
            cleaned_value = quantity_input.get_attribute("value")
            if cleaned_value != str(input_value) and cleaned_value.isdigit():
                return {
                    "status": "PASSED",
                    "message": f"Input automatically cleaned/filtered: '{input_value}' → '{cleaned_value}'"
                }
            else:
                return {
                    "status": "FAILED",
                    "message": "No validation response - text input may have been accepted"
                }
    
    def execute_error_guessing(self):
        """
        Thực hiện Error Guessing technique
        
        Dự đoán lỗi có thể xảy ra với text input
        """
        print("\n🔮 ERROR GUESSING - TEXT INPUT")
        print("-" * 40)
        
        guessed_errors = [
            "Field có thể accept bất kỳ text nào",
            "JavaScript validation có thể bị bypass",
            "Server-side validation có thể thiếu",
            "Field có thể allow HTML injection",
            "Input có thể cause application crash",
            "Không có user feedback khi input invalid"
        ]
        
        print("🤔 Potential errors with text input:")
        for i, error in enumerate(guessed_errors, 1):
            print(f"   {i}. {error}")
        
        print(f"\n🎯 Testing with error-prone input: '{self.test_data['quantity']}'")
        return self.execute_equivalence_partitioning()
    
    def run_test(self):
        """Chạy full test case"""
        try:
            self.setup()
            
            print("=" * 70)
            print("TEST CASE #8: Equivalence Partitioning + Error Guessing")
            print("=" * 70)
            print(f"User: {CURRENT_USER}")
            print(f"Date: {TEST_DATE}")
            print(f"Technique: Equivalence Partitioning, Error Guessing")
            print(f"Tool: Selenium")
            print(f"Dynamic Testing: Input Validation")
            print(f"Input: Số lượng = '{self.test_data['quantity']}'")
            print(f"Expected: {self.test_data['expected_message']}")
            
            result = self.execute_error_guessing()
            
            print(f"\n🏁 FINAL RESULT: {result['status']}")
            print(f"📝 Message: {result['message']}")
            
            return result
            
        except Exception as e:
            error_info = self.error_handlers.handle_selenium_error(e, self.driver, "TC08")
            error_msg = f"Test execution error: {str(e)}"
            print(f"💥 ERROR: {error_msg}")
            return {"status": "ERROR", "message": error_msg}
        finally:
            self.teardown()

def run_test_case_08():
    """Entry point cho Test Case 8"""
    test = TestCase08()
    return test.run_test()

if __name__ == "__main__":
    # Setup logging
    ErrorHandlers.setup_logging()
    
    result = run_test_case_08()
    print(f"\n🎯 Test Case #8 Result: {result['status']}")