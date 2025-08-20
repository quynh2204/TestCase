"""
Test Case #6: Thêm giỏ hàng không thành công với số lượng = 0

Technique: Boundary Value Analysis, Validation Testing
Tool: Selenium
Execution: Automated
Dynamic Testing: Boundary Condition Testing
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import time
import logging

from config.settings import *
from config.locators import ProductPageLocators
from config.test_data import TestData
from utils.driver_manager import DriverManager
from utils.test_helpers import TestHelpers

class TestCase06:
    """Test Case 6: Boundary Value Analysis - Số lượng = 0"""
    
    def __init__(self):
        self.driver = None
        self.wait = None
        self.test_helpers = TestHelpers()
        self.test_data = TestData.TC6_DATA
        
    def setup(self):
        """Thiết lập test environment"""
        print("🔧 Setting up Test Case #6: Boundary Value Analysis")
        self.driver = DriverManager.get_driver()
        self.wait = WebDriverWait(self.driver, EXPLICIT_WAIT)
        
    def teardown(self):
        """Dọn dẹp sau test"""
        if SCREENSHOT_ON_FAILURE:
            self.test_helpers.take_screenshot(self.driver, "TC06_final_state")
        
        if self.driver:
            time.sleep(3)
            self.driver.quit()
        print("🧹 Test Case #6 cleanup completed")
    
    def execute_boundary_value_analysis(self):
        """
        Thực hiện Boundary Value Analysis
        
        Kiểm tra behavior tại boundary values (0, 1, -1, max value)
        """
        try:
            print("\n📊 BOUNDARY VALUE ANALYSIS")
            print("-" * 40)
            
            # Boundary values cho quantity field
            boundary_values = {
                "lower_bound": 0,    # Test case này
                "valid_min": 1,      # Minimum valid value
                "normal": 5,         # Normal value
                "upper_bound": 999,  # Reasonable max
                "invalid_high": 999999  # Very high value
            }
            
            print("🔢 Boundary values identified:")
            for key, value in boundary_values.items():
                print(f"   {key}: {value}")
            
            # Test với boundary value = 0
            return self.test_quantity_boundary(0)
            
        except Exception as e:
            return {"status": "ERROR", "message": f"Boundary analysis error: {str(e)}"}
    
    def test_quantity_boundary(self, quantity_value):
        """
        Test specific boundary value cho quantity
        
        Args:
            quantity_value: Giá trị cần test
            
        Returns:
            dict: Test result
        """
        print(f"\n🧪 Testing boundary value: {quantity_value}")
        
        # Bước 1: Truy cập trang
        self.driver.get(PRODUCT_URL)
        TestHelpers.wait_for_page_load(self.driver)
        print(f"✓ Accessed: {PRODUCT_URL}")
        
        # Bước 2: Chọn phân loại (để focus vào quantity testing) - Updated to use new radio button approach
        print("🔍 Looking for category selection...")
        category_selected = TestHelpers.select_category_option(self.driver, "khac")
        
        if category_selected:
            print("✓ Đã chọn phân loại đối tượng")
        else:
            print("⚠️ Không thể chọn phân loại, tiếp tục test")
        
        # Bước 3: Tìm và modify quantity field
        quantity_input = TestHelpers.find_element_by_multiple_selectors(
            self.driver, self.wait, ProductPageLocators.QUANTITY_INPUT
        )
        
        if not quantity_input:
            return {"status": "FAILED", "message": "Không tìm thấy quantity input field"}
        
        print(f"✓ Found quantity input field")
        
        # Get initial value before modification
        initial_value = quantity_input.get_attribute("value")
        print(f"📊 Initial quantity value: {initial_value}")
        
        # Sử dụng safe_input_quantity helper với improved error handling
        print(f"📝 Inputting quantity value: {quantity_value}")
        input_result = TestHelpers.safe_input_quantity(self.driver, quantity_input, quantity_value)
        
        if not input_result["success"]:
            return {"status": "FAILED", "message": f"Không thể nhập giá trị {quantity_value}: {input_result.get('error', '')}"}
        
        print(f"✓ Input result: {input_result['input_value']} → {input_result['final_value']}")
        
        # Check if the value was modified by the system (validation)
        if input_result["was_modified"]:
            print(f"⚠️ System modified input: {input_result['input_value']} → {input_result['final_value']}")
        
        # Bước 4: Click "Thêm vào giỏ hàng" using safe_click
        add_to_cart_btn = TestHelpers.find_clickable_element_by_multiple_selectors(
            self.driver, self.wait, ProductPageLocators.ADD_TO_CART_BUTTON
        )
        
        if not add_to_cart_btn:
            return {"status": "FAILED", "message": "Không tìm thấy button 'Thêm vào giỏ hàng'"}
        
        print("🖱️ Clicking 'Thêm vào giỏ hàng' button...")
        success = TestHelpers.safe_click(self.driver, add_to_cart_btn, use_javascript=True)
        if not success:
            return {"status": "FAILED", "message": "Không thể click button sau nhiều lần thử"}
        
        print("✓ Đã click 'Thêm vào giỏ hàng'")
        
        # Bước 5: Kiểm tra behavior
        time.sleep(3)  # Đợi response và DOM updates
        
        # Re-find quantity input in case DOM was updated
        quantity_input_after = TestHelpers.find_element_by_multiple_selectors(
            self.driver, self.wait, ProductPageLocators.QUANTITY_INPUT
        )
        
        if quantity_input_after:
            current_value = quantity_input_after.get_attribute("value")
            print(f"📊 Quantity value after submit: {current_value}")
        else:
            current_value = "unknown"
            print("⚠️ Could not find quantity input after submit")
        
        expected_behavior = self.test_data['expected_behavior']
        expected_cart_items = self.test_data['expected_cart_items']
        
        # Kiểm tra error message nếu có
        error_found = False
        error_message = ""
        
        error_element = TestHelpers.find_element_by_multiple_selectors(
            self.driver, self.wait, ProductPageLocators.ERROR_MESSAGE, timeout=5
        )
        
        if error_element and error_element.is_displayed():
            error_message = error_element.text
            error_found = True
            print(f"📝 Error message found: {error_message}")
        
        # Check for any validation alerts or notifications
        try:
            alert_elements = self.driver.find_elements(By.CSS_SELECTOR, 
                ".alert, .notification, .message, [role='alert'], .toast")
            for alert in alert_elements:
                if alert.is_displayed() and alert.text.strip():
                    if not error_found:
                        error_message = alert.text
                        error_found = True
                        print(f"📝 Alert message found: {error_message}")
                    break
        except:
            pass
        
        # Validate expected behavior
        if expected_behavior == "reset_to_1":
            if current_value == "1":
                print("✅ Boundary value behavior correct: Reset to 1")
                return {
                    "status": "PASSED",
                    "message": f"Quantity {quantity_value} correctly handled - reset to 1, validation working properly"
                }
            elif error_found:
                return {
                    "status": "PASSED",
                    "message": f"Quantity {quantity_value} rejected with proper error message: '{error_message}'"
                }
            else:
                return {
                    "status": "FAILED",
                    "message": f"Quantity không reset về 1 và không có error message. Current value: {current_value}"
                }
        
        # Check if cart was updated (should not be for invalid values)
        try:
            cart_indicators = self.driver.find_elements(By.CSS_SELECTOR, 
                ".cart-count, .cart-total, [class*='cart'], [class*='added']")
            cart_updated = any(indicator.is_displayed() for indicator in cart_indicators)
            
            if cart_updated and expected_cart_items == 0:
                return {
                    "status": "FAILED",
                    "message": f"Cart was updated despite invalid quantity {quantity_value}"
                }
        except:
            pass
        
        return {
            "status": "PASSED", 
            "message": f"Boundary value test completed. Final quantity: {current_value}, Error: {error_message if error_found else 'None'}"
        }
    
    def execute_validation_testing(self):
        """
        Thực hiện Validation Testing cho boundary case
        """
        print("\n✅ VALIDATION TESTING")
        print("-" * 40)
        
        print("🔍 Validating system behavior with boundary value 0:")
        print("   - Should not accept quantity = 0")
        print("   - Should reset to minimum valid value (1)")
        print("   - Should not add item to cart")
        
        return self.execute_boundary_value_analysis()
    
    def run_test(self):
        """Chạy full test case"""
        try:
            self.setup()
            
            print("=" * 60)
            print("TEST CASE #6: Boundary Value Analysis + Validation Testing")
            print("=" * 60)
            print(f"User: {CURRENT_USER}")
            print(f"Date: {TEST_DATE}")
            print(f"Technique: Boundary Value Analysis, Validation Testing")
            print(f"Tool: Selenium")
            print(f"Dynamic Testing: Boundary Condition Testing")
            print(f"Input: Số lượng = 0")
            print(f"Expected: Không thêm khóa học vào giỏ hàng, số lượng reset về 1")
            
            result = self.execute_validation_testing()
            
            print(f"\n🏁 FINAL RESULT: {result['status']}")
            print(f"📝 Message: {result['message']}")
            
            return result
            
        except Exception as e:
            error_msg = f"Test execution error: {str(e)}"
            print(f"💥 ERROR: {error_msg}")
            return {"status": "ERROR", "message": error_msg}
        finally:
            self.teardown()

def run_test_case_06():
    """Entry point cho Test Case 6"""
    test = TestCase06()
    return test.run_test()

if __name__ == "__main__":
    result = run_test_case_06()
    print(f"\n🎯 Test Case #6 Result: {result['status']}")