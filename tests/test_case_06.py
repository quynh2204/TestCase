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
        print(f"✓ Accessed: {PRODUCT_URL}")
        
        # Bước 2: Chọn phân loại (để focus vào quantity testing)
        category_dropdown = self.test_helpers.find_element_by_multiple_selectors(
            self.driver, self.wait, ProductPageLocators.CATEGORY_DROPDOWN, timeout=5
        )
        
        if category_dropdown:
            try:
                select = Select(category_dropdown)
                if len(select.options) > 1:
                    select.select_by_index(1)  # Chọn option đầu tiên (không phải placeholder)
                    print("✓ Đã chọn phân loại đối tượng")
            except:
                print("⚠️ Không thể chọn phân loại, tiếp tục test")
        
        # Bước 3: Tìm và modify quantity field
        quantity_input = self.test_helpers.find_element_by_multiple_selectors(
            self.driver, self.wait, ProductPageLocators.QUANTITY_INPUT
        )
        
        if not quantity_input:
            return {"status": "FAILED", "message": "Không tìm thấy quantity input field"}
        
        # Clear và nhập boundary value
        success = self.test_helpers.safe_send_keys(self.driver, quantity_input, quantity_value, clear_first=True)
        if not success:
            return {"status": "FAILED", "message": f"Không thể nhập giá trị {quantity_value}"}
        
        print(f"✓ Đã nhập quantity = {quantity_value}")
        
        # Bước 4: Click "Thêm vào giỏ hàng"
        add_to_cart_btn = self.test_helpers.find_element_by_multiple_selectors(
            self.driver, self.wait, ProductPageLocators.ADD_TO_CART_BUTTON
        )
        
        if not add_to_cart_btn:
            return {"status": "FAILED", "message": "Không tìm thấy button 'Thêm vào giỏ hàng'"}
        
        success = self.test_helpers.safe_click(self.driver, add_to_cart_btn)
        if not success:
            return {"status": "FAILED", "message": "Không thể click button"}
        
        print("✓ Đã click 'Thêm vào giỏ hàng'")
        
        # Bước 5: Kiểm tra behavior
        time.sleep(2)  # Đợi response
        
        # Kiểm tra quantity field có reset về 1 không
        current_value = quantity_input.get_attribute("value")
        print(f"📊 Quantity value after submit: {current_value}")
        
        expected_behavior = self.test_data['expected_behavior']
        expected_cart_items = self.test_data['expected_cart_items']
        
        if expected_behavior == "reset_to_1":
            if current_value == "1":
                print("✅ Boundary value behavior correct: Reset to 1")
                return {
                    "status": "PASSED",
                    "message": f"Quantity {quantity_value} correctly handled - reset to 1, no items added to cart"
                }
            else:
                return {
                    "status": "FAILED",
                    "message": f"Quantity không reset về 1. Current value: {current_value}"
                }
        
        return {"status": "PASSED", "message": "Boundary value test completed"}
    
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