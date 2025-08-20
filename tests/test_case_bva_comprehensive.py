"""
Comprehensive Boundary Value Analysis Test Case
Theo chuẩn BVA với bảng đầy đủ
Author: quynh2204  
Date: 2025-08-20 14:31:42
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import time

from config.settings import *
from config.locators import ProductPageLocators
from config.boundary_value_table import BoundaryValueTable
from utils.driver_manager import DriverManager
from utils.test_helpers import TestHelpers
from utils.error_handlers import ErrorHandlers

class ComprehensiveBVATest:
    """Comprehensive Boundary Value Analysis Test"""
    
    def __init__(self):
        self.driver = None
        self.wait = None
        self.test_helpers = TestHelpers()
        self.error_handlers = ErrorHandlers()
        self.bva_table = BoundaryValueTable()
        self.results = []
        
    def setup(self):
        """Setup test environment"""
        print("🔧 Setting up Comprehensive BVA Test...")
        self.driver = DriverManager.get_driver()
        self.wait = WebDriverWait(self.driver, EXPLICIT_WAIT)
        
    def teardown(self):
        """Cleanup after test"""
        if SCREENSHOT_ON_FAILURE:
            self.test_helpers.take_screenshot(self.driver, "BVA_comprehensive_final")
        
        if self.driver:
            time.sleep(2)
            self.driver.quit()
        print("🧹 Comprehensive BVA Test cleanup completed")
    
    def test_single_boundary_value(self, test_case):
        """
        Test một boundary value cụ thể
        
        Args:
            test_case (dict): Test case data từ BVA table
            
        Returns:
            dict: Test result
        """
        test_id = test_case["test_id"]
        input_value = test_case["input"]
        expected = test_case["expected"]
        boundary_type = test_case["boundary_type"]
        
        print(f"\n🧪 Testing {test_id}: {input_value} ({boundary_type})")
        
        try:
            # Navigate to page
            self.driver.get(PRODUCT_URL)
            time.sleep(2)
            
            # Select category if needed (để focus vào quantity testing)
            category_dropdown = self.test_helpers.find_element_by_multiple_selectors(
                self.driver, self.wait, ProductPageLocators.CATEGORY_DROPDOWN, timeout=5
            )
            
            if category_dropdown:
                try:
                    select = Select(category_dropdown)
                    if len(select.options) > 1:
                        select.select_by_index(1)
                        print(f"   ✓ Category selected")
                except:
                    print(f"   ⚠️ Could not select category")
            
            # Find quantity input
            quantity_input = self.test_helpers.find_element_by_multiple_selectors(
                self.driver, self.wait, ProductPageLocators.QUANTITY_INPUT
            )
            
            if not quantity_input:
                return {
                    "test_id": test_id,
                    "input": input_value,
                    "expected": expected,
                    "actual": "ELEMENT_NOT_FOUND",
                    "status": "ERROR",
                    "boundary_type": boundary_type
                }
            
            # Input the boundary value
            quantity_input.clear()
            time.sleep(0.5)
            
            if input_value is not None:
                quantity_input.send_keys(str(input_value))
            
            time.sleep(0.5)
            actual_field_value = quantity_input.get_attribute("value")
            print(f"   📊 Field value after input: '{actual_field_value}'")
            
            # Click add to cart
            add_to_cart_btn = self.test_helpers.find_element_by_multiple_selectors(
                self.driver, self.wait, ProductPageLocators.ADD_TO_CART_BUTTON
            )
            
            if add_to_cart_btn:
                self.test_helpers.safe_click(self.driver, add_to_cart_btn)
                print(f"   ✓ Add to cart clicked")
            
            time.sleep(2)
            
            # Check result
            result = self.analyze_boundary_result(
                test_id, input_value, expected, actual_field_value, boundary_type
            )
            
            return result
            
        except Exception as e:
            return {
                "test_id": test_id,
                "input": input_value,
                "expected": expected,
                "actual": f"ERROR: {str(e)}",
                "status": "ERROR",
                "boundary_type": boundary_type
            }
    
    def analyze_boundary_result(self, test_id, input_value, expected, actual_field_value, boundary_type):
        """Phân tích kết quả boundary test"""
        
        # Check for error messages
        error_element = self.test_helpers.find_element_by_multiple_selectors(
            self.driver, self.wait, ProductPageLocators.ERROR_MESSAGE, timeout=3
        )
        
        error_message = error_element.text if error_element else None
        
        # Check if field value changed (indicating validation)
        field_reset = actual_field_value != str(input_value) if input_value is not None else False
        
        # Determine actual behavior
        if error_message:
            actual_behavior = f"ERROR_MESSAGE: {error_message}"
        elif field_reset:
            actual_behavior = f"FIELD_RESET: {actual_field_value}"
        elif "Accept" in expected and not error_message:
            actual_behavior = "ACCEPTED"
        else:
            actual_behavior = "NO_VALIDATION_RESPONSE"
        
        # Determine status
        status = "UNKNOWN"
        
        if "Accept" in expected:
            # Should be accepted
            if not error_message and not field_reset:
                status = "PASSED"
            else:
                status = "FAILED"
        else:
            # Should be rejected
            if error_message or field_reset:
                status = "PASSED"
            else:
                status = "FAILED"
        
        return {
            "test_id": test_id,
            "input": input_value,
            "expected": expected,
            "actual": actual_behavior,
            "status": status,
            "boundary_type": boundary_type,
            "field_value": actual_field_value,
            "error_message": error_message
        }
    
    def run_complete_bva_test(self):
        """Chạy complete BVA test với tất cả boundary values"""
        
        print("📊 COMPREHENSIVE BOUNDARY VALUE ANALYSIS")
        print("=" * 60)
        
        # Print BVA table
        self.bva_table.print_bva_table()
        
        # Get test data matrix
        test_matrix = self.bva_table.get_test_data_matrix()
        
        print(f"\n🧪 EXECUTING BVA TESTS...")
        print(f"Total test cases: {len(test_matrix['quantity_valid_boundaries']) + len(test_matrix['quantity_invalid_boundaries'])}")
        
        # Test valid boundaries
        print(f"\n✅ TESTING VALID BOUNDARIES...")
        for test_case in test_matrix['quantity_valid_boundaries']:
            result = self.test_single_boundary_value(test_case)
            self.results.append(result)
            
            status_icon = "✅" if result['status'] == 'PASSED' else "❌"
            print(f"   {status_icon} {result['test_id']}: {result['status']}")
        
        # Test invalid boundaries  
        print(f"\n❌ TESTING INVALID BOUNDARIES...")
        for test_case in test_matrix['quantity_invalid_boundaries']:
            result = self.test_single_boundary_value(test_case)
            self.results.append(result)
            
            status_icon = "✅" if result['status'] == 'PASSED' else "❌"
            print(f"   {status_icon} {result['test_id']}: {result['status']}")
        
        return self.results
    
    def generate_bva_report(self):
        """Tạo báo cáo BVA chi tiết"""
        
        passed = len([r for r in self.results if r['status'] == 'PASSED'])
        failed = len([r for r in self.results if r['status'] == 'FAILED'])
        errors = len([r for r in self.results if r['status'] == 'ERROR'])
        
        print(f"\n📊 BVA TEST SUMMARY")
        print("=" * 50)
        print(f"Total Tests: {len(self.results)}")
        print(f"✅ Passed: {passed}")
        print(f"❌ Failed: {failed}")
        print(f"💥 Errors: {errors}")
        print(f"🎯 Pass Rate: {round((passed/len(self.results))*100, 2)}%" if self.results else "0%")
        
        print(f"\n📋 DETAILED RESULTS:")
        print(f"{'Test ID':<10} {'Input':<10} {'Expected':<15} {'Actual':<30} {'Status':<10}")
        print("-" * 85)
        
        for result in self.results:
            input_display = str(result['input'])[:8] if result['input'] is not None else "None"
            expected_display = result['expected'][:13]
            actual_display = result['actual'][:28]
            
            print(f"{result['test_id']:<10} {input_display:<10} {expected_display:<15} {actual_display:<30} {result['status']:<10}")
        
        # Boundary type analysis
        print(f"\n🔍 BOUNDARY TYPE ANALYSIS:")
        boundary_stats = {}
        for result in self.results:
            btype = result['boundary_type']
            if btype not in boundary_stats:
                boundary_stats[btype] = {'passed': 0, 'failed': 0, 'total': 0}
            
            boundary_stats[btype]['total'] += 1
            if result['status'] == 'PASSED':
                boundary_stats[btype]['passed'] += 1
            else:
                boundary_stats[btype]['failed'] += 1
        
        for btype, stats in boundary_stats.items():
            pass_rate = (stats['passed'] / stats['total']) * 100
            print(f"   {btype:<25}: {stats['passed']}/{stats['total']} ({pass_rate:.1f}%)")
    
    def run_test(self):
        """Main test execution"""
        try:
            self.setup()
            
            print("🚀 COMPREHENSIVE BOUNDARY VALUE ANALYSIS TEST")
            print("=" * 70)
            print(f"User: {CURRENT_USER}")
            print(f"Date: 2025-08-20 14:31:42")
            print(f"Technique: Comprehensive Boundary Value Analysis")
            print(f"Tool: Selenium")
            print(f"Dynamic Testing: Boundary Condition Testing")
            
            # Run complete BVA test
            self.run_complete_bva_test()
            
            # Generate report
            self.generate_bva_report()
            
            # Overall result
            passed = len([r for r in self.results if r['status'] == 'PASSED'])
            overall_status = "PASSED" if passed > len(self.results) * 0.8 else "FAILED"
            
            return {
                "status": overall_status,
                "message": f"BVA comprehensive test completed. {passed}/{len(self.results)} passed.",
                "detailed_results": self.results
            }
            
        except Exception as e:
            error_msg = f"BVA test execution error: {str(e)}"
            print(f"💥 ERROR: {error_msg}")
            return {"status": "ERROR", "message": error_msg}
        finally:
            self.teardown()

def run_comprehensive_bva_test():
    """Entry point cho Comprehensive BVA Test"""
    test = ComprehensiveBVATest()
    return test.run_test()

if __name__ == "__main__":
    # Setup logging
    ErrorHandlers.setup_logging()
    
    # Print BVA table first
    BoundaryValueTable.print_bva_table()
    
    # Run test
    result = run_comprehensive_bva_test()
    print(f"\n🎯 Comprehensive BVA Test Result: {result['status']}")