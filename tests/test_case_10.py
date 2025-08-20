"""
Test Case #10: Thêm sản phẩm không thành công với ký tự đặc biệt trong số lượng

Technique: Equivalence Partitioning, Error Guessing
Tool: Selenium
Execution: Automated
Dynamic Testing: Error Handling
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

class TestCase10:
    """Test Case 10: Error Handling - Ký tự đặc biệt"""
    
    def __init__(self):
        self.driver = None
        self.wait = None
        self.test_helpers = TestHelpers()
        self.validation_helpers = ValidationHelpers()
        self.error_handlers = ErrorHandlers()
        self.test_data = TestData.TC10_DATA
        
    def setup(self):
        """Thiết lập test environment"""
        print("🔧 Setting up Test Case #10: Error Handling - Special Characters")
        self.driver = DriverManager.get_driver()
        self.wait = WebDriverWait(self.driver, EXPLICIT_WAIT)
        
    def teardown(self):
        """Dọn dẹp sau test"""
        if SCREENSHOT_ON_FAILURE:
            self.test_helpers.take_screenshot(self.driver, "TC10_final_state")
        
        if self.driver:
            time.sleep(3)
            self.driver.quit()
        print("🧹 Test Case #10 cleanup completed")
    
    def execute_equivalence_partitioning(self):
        """
        Thực hiện Equivalence Partitioning cho special characters
        
        Chia input thành các partitions:
        - Valid: Positive integers (1, 2, 3...)
        - Invalid: Special symbols (!@#, $%^, ()[], etc.)
        - Invalid: Mixed alphanumeric with symbols (1!, a@, etc.)
        """
        try:
            print("\n📊 EQUIVALENCE PARTITIONING - SPECIAL CHARACTERS")
            print("-" * 55)
            
            # Define special character partitions
            special_char_partitions = {
                "mathematical_symbols": ["!@#", "$%^", "&*()", "+=", "-+"],
                "punctuation": [".,;", ":?", "!'", '"', "[]{}"],
                "currency_symbols": ["$$$", "€€€", "¥¥¥", "£££"],
                "programming_symbols": ["<>", "||", "&&", "//", "\\\\"],
                "mixed_with_numbers": ["1!", "2@", "3#", "4$", "5%"],
                "unicode_symbols": ["★☆", "♠♥", "◄►", "▲▼"],
                "whitespace_special": ["   ", "\t\t", "\n\n"]
            }
            
            print("🗂️ Special character partitions:")
            for partition, values in special_char_partitions.items():
                print(f"   {partition}: {values}")
            
            # Test với mathematical_symbols partition
            test_value = self.test_data['quantity']  # "!@#"
            print(f"\n🎯 Testing mathematical_symbols partition with: '{test_value}'")
            
            # Validate special characters
            validation_result = self.validation_helpers.validate_special_characters(test_value)
            print(f"📋 Special character analysis: {validation_result['message']}")
            
            return self.test_special_characters(test_value)
            
        except Exception as e:
            error_info = self.error_handlers.handle_selenium_error(e, self.driver, "TC10_equivalence")
            return {"status": "ERROR", "message": f"Equivalence partitioning error: {str(e)}"}
    
    def test_special_characters(self, input_value):
        """
        Test special characters trong quantity field
        
        Args:
            input_value: Special character string to test
            
        Returns:
            dict: Test result
        """
        print(f"\n🧪 Testing special characters: '{input_value}'")
        
        # Bước 1: Truy cập trang
        self.driver.get(PRODUCT_URL)
        self.test_helpers.wait_for_page_load(self.driver)
        print(f"✓ Accessed: {PRODUCT_URL}")
        
        # Bước 2: Chọn phân loại
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
        
        # Bước 3: Test special character input
        quantity_input = self.test_helpers.find_element_by_multiple_selectors(
            self.driver, self.wait, ProductPageLocators.QUANTITY_INPUT
        )
        
        if not quantity_input:
            return {"status": "FAILED", "message": "Không tìm thấy quantity input field"}
        
        # Analyze special characters trước khi test
        char_analysis = self.validation_helpers.validate_special_characters(input_value)
        if char_analysis['has_special_chars']:
            print(f"🔍 Detected special characters: {char_analysis['special_chars_found']}")
        
        # Test input behavior
        print(f"📝 Attempting to input special characters: '{input_value}'")
        
        # Sử dụng safe_input_quantity helper
        input_result = self.test_helpers.safe_input_quantity(self.driver, quantity_input, input_value)
        
        if not input_result["success"]:
            return {"status": "FAILED", "message": f"Không thể test input với giá trị '{input_value}': {input_result.get('error', '')}"}
        
        print(f"✓ Input result: '{input_result['input_value']}' → '{input_result['final_value']}'")
        
        # Test security: Try các cách input khác nhau
        input_methods = [
            ("direct_input", lambda: self.test_helpers.safe_input_quantity(self.driver, quantity_input, input_value)),
            ("char_by_char", lambda: self.input_char_by_char(quantity_input, input_value)),
            ("copy_paste", lambda: self.simulate_copy_paste(quantity_input, input_value))
        ]
        
        results = {}
        for method_name, method_func in input_methods:
            try:
                print(f"   🧪 Testing {method_name}...")
                quantity_input.clear()
                
                if method_name == "direct_input":
                    method_result = method_func()
                    current_value = method_result.get("final_value", "")
                else:
                    method_func()
                    time.sleep(0.5)
                    current_value = quantity_input.get_attribute("value")
                
                results[method_name] = current_value
                print(f"     Result: '{current_value}'")
                
            except Exception as e:
                results[method_name] = f"ERROR: {str(e)}"
                print(f"     Error: {str(e)}")
        
        # Bước 4: Test submit behavior
        add_to_cart_btn = self.test_helpers.find_clickable_element_by_multiple_selectors(
            self.driver, self.wait, ProductPageLocators.ADD_TO_CART_BUTTON
        )
        
        if not add_to_cart_btn:
            return {"status": "FAILED", "message": "Không tìm thấy button 'Thêm vào giỏ hàng'"}
        
        # Ensure có value trong field để test
        final_field_value = quantity_input.get_attribute("value")
        print(f"📊 Final field value before submit: '{final_field_value}'")
        
        success = self.test_helpers.safe_click(self.driver, add_to_cart_btn)
        if not success:
            return {"status": "FAILED", "message": "Không thể click button"}
        
        print("✓ Đã click 'Thêm vào giỏ hàng'")
        
        # Bước 5: Kiểm tra error handling
        time.sleep(2)
        
        # Check for error message
        error_element = self.test_helpers.find_element_by_multiple_selectors(
            self.driver, self.wait, ProductPageLocators.ERROR_MESSAGE, timeout=5
        )
        
        expected_message = self.test_data['expected_message']
        
        if error_element and error_element.is_displayed():
            actual_message = error_element.text
            print(f"✓ Error message found: '{actual_message}'")
            
            if expected_message in actual_message or "số" in actual_message.lower() or "hợp lệ" in actual_message.lower():
                return {
                    "status": "PASSED",
                    "message": f"Special characters correctly handled: '{actual_message}'"
                }
            else:
                return {
                    "status": "FAILED",
                    "message": f"Wrong error message. Expected: '{expected_message}', Got: '{actual_message}'"
                }
        else:
            # Check if input was sanitized
            sanitized_value = quantity_input.get_attribute("value")
            if sanitized_value != input_value:
                return {
                    "status": "PASSED",
                    "message": f"Input sanitized: '{input_value}' → '{sanitized_value}'"
                }
            else:
                return {
                    "status": "FAILED",
                    "message": f"Special characters were accepted without validation: '{input_value}'"
                }
    
    def input_char_by_char(self, element, text):
        """Input text character by character"""
        for char in text:
            element.send_keys(char)
            time.sleep(0.1)
    
    def simulate_copy_paste(self, element, text):
        """Simulate copy-paste operation"""
        try:
            # Use JavaScript to set value (simulating paste)
            self.driver.execute_script(f"arguments[0].value = '{text}';", element)
            # Trigger input event
            self.driver.execute_script("arguments[0].dispatchEvent(new Event('input'));", element)
        except Exception as e:
            print(f"Copy-paste simulation failed: {str(e)}")
    
    def execute_error_guessing(self):
        """
        Thực hiện Error Guessing cho special characters
        
        Dự đoán lỗi có thể xảy ra với special character input
        """
        print("\n🔮 ERROR GUESSING - SPECIAL CHARACTERS")
        print("-" * 45)
        
        guessed_errors = [
            "XSS injection through special characters",
            "SQL injection via input field",
            "Application crash with unicode characters",
            "Buffer overflow with long special char strings",
            "Bypass client-side validation",
            "Server error with unescaped characters",
            "Data corruption in database",
            "Session hijacking via malicious input"
        ]
        
        print("🤔 Potential security/error risks:")
        for i, error in enumerate(guessed_errors, 1):
            print(f"   {i}. {error}")
        
        # Test for potential XSS
        xss_payloads = [
            "<script>alert('xss')</script>",
            "javascript:alert(1)",
            "';alert('xss');//",
            "<img src=x onerror=alert(1)>"
        ]
        
        print(f"\n🛡️ Testing XSS payloads:")
        for payload in xss_payloads:
            print(f"   {payload}")
        
        print(f"\n🎯 Testing with error-prone input: '{self.test_data['quantity']}'")
        return self.execute_equivalence_partitioning()
    
    def run_test(self):
        """Chạy full test case"""
        try:
            self.setup()
            
            print("=" * 70)
            print("TEST CASE #10: Equivalence Partitioning + Error Guessing")
            print("=" * 70)
            print(f"User: {CURRENT_USER}")
            print(f"Date: {TEST_DATE}")
            print(f"Technique: Equivalence Partitioning, Error Guessing")
            print(f"Tool: Selenium")
            print(f"Dynamic Testing: Error Handling")
            print(f"Input: Số lượng = '{self.test_data['quantity']}'")
            print(f"Expected: {self.test_data['expected_message']}")
            
            result = self.execute_error_guessing()
            
            print(f"\n🏁 FINAL RESULT: {result['status']}")
            print(f"📝 Message: {result['message']}")
            
            return result
            
        except Exception as e:
            error_info = self.error_handlers.handle_selenium_error(e, self.driver, "TC10")
            error_msg = f"Test execution error: {str(e)}"
            print(f"💥 ERROR: {error_msg}")
            return {"status": "ERROR", "message": error_msg}
        finally:
            self.teardown()

def run_test_case_10():
    """Entry point cho Test Case 10"""
    test = TestCase10()
    return test.run_test()

if __name__ == "__main__":
    # Setup logging
    ErrorHandlers.setup_logging()
    
    result = run_test_case_10()
    print(f"\n🎯 Test Case #10 Result: {result['status']}")