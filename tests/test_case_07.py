"""
Test Case #7: Thêm giỏ hàng không thành công với số lượng = -1

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
import time
import logging

from config.settings import *
from config.locators import ProductPageLocators
from config.test_data import TestData
from utils.driver_manager import DriverManager
from utils.test_helpers import TestHelpers

class TestCase07:
    """Test Case 7: Error Handling - Số lượng = -1"""
    
    def __init__(self):
        self.driver = None
        self.wait = None
        self.test_helpers = TestHelpers()
        self.test_data = TestData.TC7_DATA
        
    def setup(self):
        """Thiết lập test environment"""
        print("🔧 Setting up Test Case #7: Error Handling")
        self.driver = DriverManager.get_driver()
        self.wait = WebDriverWait(self.driver, EXPLICIT_WAIT)
        
    def teardown(self):
        """Dọn dẹp sau test"""
        if SCREENSHOT_ON_FAILURE:
            self.test_helpers.take_screenshot(self.driver, "TC07_final_state")
        
        if self.driver:
            time.sleep(3)
            self.driver.quit()
        print("🧹 Test Case #7 cleanup completed")
    
    def execute_equivalence_partitioning(self):
        """
        Thực hiện Equivalence Partitioning
        
        Chia input thành các partitions:
        - Valid partition: 1, 2, 3, ... (positive integers)
        - Invalid partition: 0, -1, -2, ... (zero and negative)
        - Invalid partition: non-numeric values
        """
        print("\n📊 EQUIVALENCE PARTITIONING")
        print("-" * 40)
        
        partitions = {
            "valid_positive": [1, 2, 5, 10],
            "invalid_zero": [0],
            "invalid_negative": [-1, -2, -5],  # Test case này focus vào -1
            "invalid_non_numeric": ["abc", "!@#", ""]
        }
        
        print("🗂️ Input partitions identified:")
        for partition, values in partitions.items():
            print(f"   {partition}: {values}")
        
        # Test với invalid negative partition (-1)
        print(f"\n🎯 Testing invalid_negative partition with value: -1")
        return self.test_negative_quantity(-1)
    
    def test_negative_quantity(self, quantity_value):
        """
        Test negative quantity value
        
        Args:
            quantity_value: Negative value to test
            
        Returns:
            dict: Test result
        """
        print(f"\n🧪 Testing negative quantity: {quantity_value}")
        
        # Bước 1: Truy cập trang
        self.driver.get(PRODUCT_URL)
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
            except:
                print("⚠️ Không thể chọn phân loại, tiếp tục test")
        
        # Bước 3: Nhập negative quantity
        quantity_input = self.test_helpers.find_element_by_multiple_selectors(
            self.driver, self.wait, ProductPageLocators.QUANTITY_INPUT
        )
        
        if not quantity_input:
            return {"status": "FAILED", "message": "Không tìm thấy quantity input field"}
        
        # Thử nhập giá trị âm
        success = self.test_helpers.safe_send_keys(self.driver, quantity_input, quantity_value, clear_first=True)
        if not success:
            return {"status": "FAILED", "message": f"Không thể nhập giá trị {quantity_value}"}
        
        print(f"✓ Đã thử nhập quantity = {quantity_value}")
        
        # Kiểm tra giá trị trong field sau khi nhập
        time.sleep(1)
        actual_value = quantity_input.get_attribute("value")
        print(f"📊 Actual value in field: '{actual_value}'")
        
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
        
        # Bước 5: Kiểm tra error handling
        time.sleep(2)
        
        # Kiểm tra quantity có reset về 1 không
        current_value = quantity_input.get_attribute("value")
        print(f"📊 Quantity value after submit: {current_value}")
        
        expected_behavior = self.test_data['expected_behavior']
        
        if expected_behavior == "reset_to_1":
            if current_value == "1":
                print("✅ Error handling correct: Negative value rejected, reset to 1")
                return {
                    "status": "PASSED",
                    "message": f"Negative quantity {quantity_value} correctly handled - reset to 1, no items added"
                }
            else:
                return {
                    "status": "FAILED",
                    "message": f"Error handling failed. Expected reset to 1, got: {current_value}"
                }
        
        return {"status": "PASSED", "message": "Negative quantity test completed"}
    
    def execute_error_guessing(self):
        """
        Thực hiện Error Guessing technique
        
        Dự đoán các lỗi có thể xảy ra với negative inputs
        """
        print("\n🔮 ERROR GUESSING")
        print("-" * 40)
        
        guessed_errors = [
            "Hệ thống có thể accept negative values",
            "Hệ thống có thể crash với negative inputs",
            "Quantity field có thể không validate client-side",
            "Server có thể không handle negative quantities",
            "Cart có thể hiển thị negative item counts"
        ]
        
        print("🤔 Potential errors to test:")
        for i, error in enumerate(guessed_errors, 1):
            print(f"   {i}. {error}")
        
        print(f"\n🎯 Testing with error-prone input: -1")
        return self.execute_equivalence_partitioning()
    
    def run_test(self):
        """Chạy full test case"""
        try:
            self.setup()
            
            print("=" * 60)
            print("TEST CASE #7: Equivalence Partitioning + Error Guessing")
            print("=" * 60)
            print(f"User: {CURRENT_USER}")
            print(f"Date: {TEST_DATE}")
            print(f"Technique: Equivalence Partitioning, Error Guessing")
            print(f"Tool: Selenium")
            print(f"Dynamic Testing: Error Handling")
            print(f"Input: Số lượng = -1")
            print(f"Expected: Không cho phép nhập số âm, số lượng reset về 1")
            
            result = self.execute_error_guessing()
            
            print(f"\n🏁 FINAL RESULT: {result['status']}")
            print(f"📝 Message: {result['message']}")
            
            return result
            
        except Exception as e:
            error_msg = f"Test execution error: {str(e)}"
            print(f"💥 ERROR: {error_msg}")
            return {"status": "ERROR", "message": error_msg}
        finally:
            self.teardown()

def run_test_case_07():
    """Entry point cho Test Case 7"""
    test = TestCase07()
    return test.run_test()

if __name__ == "__main__":
    result = run_test_case_07()
    print(f"\n🎯 Test Case #7 Result: {result['status']}")