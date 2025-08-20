"""
Test Case #9: Thêm giỏ hàng không thành công với số lượng quá lớn

Technique: Boundary Value Analysis, Stress/Load Testing
Tool: Selenium + JMeter
Execution: Automated
Dynamic Testing: Stress/Load Testing
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
import subprocess
import psutil
import threading

from config.settings import *
from config.locators import ProductPageLocators
from config.test_data import TestData
from utils.driver_manager import DriverManager
from utils.test_helpers import TestHelpers
from utils.boundary_helpers import BoundaryHelpers
from utils.error_handlers import ErrorHandlers

class TestCase09:
    """Test Case 9: Stress Testing với số lượng cực lớn"""
    
    def __init__(self):
        self.driver = None
        self.wait = None
        self.test_helpers = TestHelpers()
        self.boundary_helpers = BoundaryHelpers()
        self.error_handlers = ErrorHandlers()
        self.test_data = TestData.TC9_DATA
        self.performance_metrics = {}
        
    def setup(self):
        """Thiết lập test environment"""
        print("🔧 Setting up Test Case #9: Stress/Load Testing")
        self.driver = DriverManager.get_driver()
        self.wait = WebDriverWait(self.driver, EXPLICIT_WAIT)
        
        # Setup performance monitoring
        self.setup_performance_monitoring()
        
    def teardown(self):
        """Dọn dẹp sau test"""
        if SCREENSHOT_ON_FAILURE:
            self.test_helpers.take_screenshot(self.driver, "TC09_final_state")
        
        # Stop performance monitoring
        self.stop_performance_monitoring()
        
        if self.driver:
            time.sleep(3)
            self.driver.quit()
        print("🧹 Test Case #9 cleanup completed")
    
    def setup_performance_monitoring(self):
        """Setup monitoring cho stress testing"""
        print("📊 Setting up performance monitoring...")
        self.monitoring_active = True
        self.performance_metrics = {
            "cpu_usage": [],
            "memory_usage": [],
            "response_times": [],
            "start_time": time.time()
        }
        
        # Start monitoring thread
        self.monitor_thread = threading.Thread(target=self.monitor_performance)
        self.monitor_thread.daemon = True
        self.monitor_thread.start()
    
    def monitor_performance(self):
        """Monitor system performance during test"""
        while self.monitoring_active:
            try:
                cpu_percent = psutil.cpu_percent(interval=1)
                memory_percent = psutil.virtual_memory().percent
                
                self.performance_metrics["cpu_usage"].append(cpu_percent)
                self.performance_metrics["memory_usage"].append(memory_percent)
                
                time.sleep(2)
            except:
                break
    
    def stop_performance_monitoring(self):
        """Stop performance monitoring"""
        self.monitoring_active = False
        self.performance_metrics["end_time"] = time.time()
        self.performance_metrics["total_duration"] = (
            self.performance_metrics["end_time"] - self.performance_metrics["start_time"]
        )
        
        print("📈 Performance monitoring completed")
        self.print_performance_summary()
    
    def print_performance_summary(self):
        """Print performance summary"""
        if self.performance_metrics["cpu_usage"]:
            avg_cpu = sum(self.performance_metrics["cpu_usage"]) / len(self.performance_metrics["cpu_usage"])
            max_cpu = max(self.performance_metrics["cpu_usage"])
            
            avg_memory = sum(self.performance_metrics["memory_usage"]) / len(self.performance_metrics["memory_usage"])
            max_memory = max(self.performance_metrics["memory_usage"])
            
            print(f"\n📊 PERFORMANCE METRICS:")
            print(f"   Test Duration: {self.performance_metrics['total_duration']:.2f} seconds")
            print(f"   Average CPU: {avg_cpu:.1f}%")
            print(f"   Peak CPU: {max_cpu:.1f}%")
            print(f"   Average Memory: {avg_memory:.1f}%")
            print(f"   Peak Memory: {max_memory:.1f}%")
    
    def execute_boundary_value_analysis(self):
        """
        Thực hiện Boundary Value Analysis cho large numbers
        """
        try:
            print("\n📊 BOUNDARY VALUE ANALYSIS - LARGE VALUES")
            print("-" * 50)
            
            # Get quantity boundaries
            boundaries = self.boundary_helpers.get_quantity_boundaries()
            print("🔢 Quantity boundaries:")
            for key, value in boundaries.items():
                print(f"   {key}: {value}")
            
            # Analyze test value
            test_value = self.test_data['quantity']  # 999999
            analysis = self.boundary_helpers.analyze_boundary_behavior(
                test_value, 
                boundaries['absolute_minimum'], 
                boundaries['system_maximum']
            )
            
            print(f"\n🔍 Analysis for value {test_value}:")
            print(f"   Category: {analysis['category']}")
            print(f"   Expected Behavior: {analysis['expected_behavior']}")
            print(f"   Risk Level: {analysis['risk_level']}")
            print(f"   Description: {analysis['description']}")
            
            return self.test_large_quantity(test_value)
            
        except Exception as e:
            error_info = self.error_handlers.handle_selenium_error(e, self.driver, "TC09_boundary")
            return {"status": "ERROR", "message": f"Boundary analysis error: {str(e)}"}
    
    def test_large_quantity(self, quantity_value):
        """
        Test với số lượng cực lớn
        
        Args:
            quantity_value: Large quantity to test
            
        Returns:
            dict: Test result
        """
        print(f"\n🚀 STRESS TESTING with quantity: {quantity_value}")
        
        start_time = time.time()
        
        # Bước 1: Truy cập trang
        page_load_start = time.time()
        self.driver.get(PRODUCT_URL)
        page_load_time = time.time() - page_load_start
        print(f"✓ Page loaded in {page_load_time:.2f} seconds")
        
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
        
        # Bước 3: Input large quantity
        quantity_input = self.test_helpers.find_element_by_multiple_selectors(
            self.driver, self.wait, ProductPageLocators.QUANTITY_INPUT
        )
        
        if not quantity_input:
            return {"status": "FAILED", "message": "Không tìm thấy quantity input field"}
        
        # Test input performance
        input_start = time.time()
        quantity_input.clear()
        
        # Input large number character by character để test performance
        large_number_str = str(quantity_value)
        print(f"📝 Inputting large number: {large_number_str} ({len(large_number_str)} digits)")
        
        for i, digit in enumerate(large_number_str):
            quantity_input.send_keys(digit)
            if i % 2 == 0:  # Check every few digits
                current_value = quantity_input.get_attribute("value")
                if len(current_value) > 10:  # Performance concern threshold
                    break
        
        input_time = time.time() - input_start
        final_value = quantity_input.get_attribute("value")
        print(f"✓ Input completed in {input_time:.2f} seconds")
        print(f"📊 Final field value: '{final_value}'")
        
        # Bước 4: Stress test submit
        submit_start = time.time()
        add_to_cart_btn = self.test_helpers.find_element_by_multiple_selectors(
            self.driver, self.wait, ProductPageLocators.ADD_TO_CART_BUTTON
        )
        
        if not add_to_cart_btn:
            return {"status": "FAILED", "message": "Không tìm thấy button 'Thêm vào giỏ hàng'"}
        
        success = self.test_helpers.safe_click(self.driver, add_to_cart_btn)
        if not success:
            return {"status": "FAILED", "message": "Không thể click button"}
        
        submit_time = time.time() - submit_start
        print(f"✓ Submit completed in {submit_time:.2f} seconds")
        
        # Bước 5: Check stress test results
        time.sleep(3)  # Wait for response
        
        # Check for error message
        error_element = self.test_helpers.find_element_by_multiple_selectors(
            self.driver, self.wait, ProductPageLocators.ERROR_MESSAGE, timeout=5
        )
        
        expected_message = self.test_data['expected_message']
        total_time = time.time() - start_time
        
        # Record response time
        self.performance_metrics["response_times"].append(total_time)
        
        if error_element:
            actual_message = error_element.text
            print(f"✓ Error message found: '{actual_message}'")
            print(f"📈 Total response time: {total_time:.2f} seconds")
            
            if expected_message in actual_message:
                return {
                    "status": "PASSED",
                    "message": f"Large quantity correctly rejected: '{actual_message}' (Response: {total_time:.2f}s)"
                }
            else:
                return {
                    "status": "FAILED",
                    "message": f"Wrong error message. Expected: '{expected_message}', Got: '{actual_message}'"
                }
        else:
            return {
                "status": "FAILED",
                "message": f"No error message for large quantity {quantity_value}"
            }
    
    def execute_load_testing(self):
        """
        Thực hiện Load Testing (simulated)
        """
        print("\n🔥 LOAD TESTING SIMULATION")
        print("-" * 40)
        
        print("🧪 Simulating multiple concurrent requests...")
        
        # Simulate multiple rapid requests
        request_results = []
        for i in range(5):
            print(f"   Request {i+1}/5...")
            start_time = time.time()
            
            try:
                # Quick test cycle
                self.driver.refresh()
                time.sleep(1)
                
                # Quick input test
                quantity_input = self.test_helpers.find_element_by_multiple_selectors(
                    self.driver, self.wait, ProductPageLocators.QUANTITY_INPUT, timeout=5
                )
                
                if quantity_input:
                    quantity_input.clear()
                    quantity_input.send_keys("999999")
                    
                response_time = time.time() - start_time
                request_results.append(response_time)
                print(f"     Response time: {response_time:.2f}s")
                
            except Exception as e:
                print(f"     Request failed: {str(e)}")
                request_results.append(None)
        
        # Analyze load test results
        successful_requests = [r for r in request_results if r is not None]
        if successful_requests:
            avg_response = sum(successful_requests) / len(successful_requests)
            print(f"\n📊 Load Test Results:")
            print(f"   Successful requests: {len(successful_requests)}/5")
            print(f"   Average response time: {avg_response:.2f}s")
            print(f"   Max response time: {max(successful_requests):.2f}s")
            print(f"   Min response time: {min(successful_requests):.2f}s")
        
        return self.execute_boundary_value_analysis()
    
    def create_jmeter_script(self):
        """Tạo JMeter script cho load testing"""
        jmeter_dir = "performance/jmeter_scripts"
        os.makedirs(jmeter_dir, exist_ok=True)
        
        jmeter_script = f"""<?xml version="1.0" encoding="UTF-8"?>
<jmeterTestPlan version="1.2" properties="5.0" jmeter="5.4.1">
  <hashTree>
    <TestPlan guiclass="TestPlanGui" testclass="TestPlan" testname="Large Quantity Load Test" enabled="true">
      <stringProp name="TestPlan.comments">Load test for large quantity input</stringProp>
      <boolProp name="TestPlan.functional_mode">false</boolProp>
      <boolProp name="TestPlan.tearDown_on_shutdown">true</boolProp>
      <boolProp name="TestPlan.serialize_threadgroups">false</boolProp>
      <elementProp name="TestPlan.arguments" elementType="Arguments" guiclass="ArgumentsPanel" testclass="Arguments" testname="User Defined Variables" enabled="true">
        <collectionProp name="Arguments.arguments"/>
      </elementProp>
      <stringProp name="TestPlan.user_define_classpath"></stringProp>
    </TestPlan>
    <hashTree>
      <ThreadGroup guiclass="ThreadGroupGui" testclass="ThreadGroup" testname="Load Test Users" enabled="true">
        <stringProp name="ThreadGroup.on_sample_error">continue</stringProp>
        <elementProp name="ThreadGroup.main_controller" elementType="LoopController" guiclass="LoopControlGui" testclass="LoopController" testname="Loop Controller" enabled="true">
          <boolProp name="LoopController.continue_forever">false</boolProp>
          <stringProp name="LoopController.loops">3</stringProp>
        </elementProp>
        <stringProp name="ThreadGroup.num_threads">10</stringProp>
        <stringProp name="ThreadGroup.ramp_time">5</stringProp>
      </ThreadGroup>
      <hashTree>
        <HTTPSamplerProxy guiclass="HttpTestSampleGui" testclass="HTTPSamplerProxy" testname="Product Page Request" enabled="true">
          <elementProp name="HTTPsampler.Arguments" elementType="Arguments" guiclass="HTTPArgumentsPanel" testclass="Arguments" testname="User Defined Variables" enabled="true">
            <collectionProp name="Arguments.arguments">
              <elementProp name="quantity" elementType="HTTPArgument">
                <boolProp name="HTTPArgument.always_encode">false</boolProp>
                <stringProp name="Argument.value">999999</stringProp>
                <stringProp name="Argument.metadata">=</stringProp>
                <boolProp name="HTTPArgument.use_equals">true</boolProp>
                <stringProp name="Argument.name">quantity</stringProp>
              </elementProp>
            </collectionProp>
          </elementProp>
          <stringProp name="HTTPSampler.domain">atd.ueh.edu.vn</stringProp>
          <stringProp name="HTTPSampler.port"></stringProp>
          <stringProp name="HTTPSampler.protocol">https</stringProp>
          <stringProp name="HTTPSampler.contentEncoding"></stringProp>
          <stringProp name="HTTPSampler.path">/business-analyst-in-practices-p16.html</stringProp>
          <stringProp name="HTTPSampler.method">POST</stringProp>
          <boolProp name="HTTPSampler.follow_redirects">true</boolProp>
          <boolProp name="HTTPSampler.auto_redirects">false</boolProp>
          <boolProp name="HTTPSampler.use_keepalive">true</boolProp>
          <boolProp name="HTTPSampler.DO_MULTIPART_POST">false</boolProp>
          <stringProp name="HTTPSampler.embedded_url_re"></stringProp>
          <stringProp name="HTTPSampler.connect_timeout"></stringProp>
          <stringProp name="HTTPSampler.response_timeout"></stringProp>
        </HTTPSamplerProxy>
      </hashTree>
    </hashTree>
  </hashTree>
</jmeterTestPlan>"""
        
        script_path = f"{jmeter_dir}/large_quantity_test.jmx"
        with open(script_path, 'w', encoding='utf-8') as f:
            f.write(jmeter_script)
        
        print(f"✓ JMeter script created: {script_path}")
        return script_path
    
    def run_test(self):
        """Chạy full test case"""
        try:
            self.setup()
            
            print("=" * 70)
            print("TEST CASE #9: Boundary Value Analysis + Stress/Load Testing")
            print("=" * 70)
            print(f"User: {CURRENT_USER}")
            print(f"Date: {TEST_DATE}")
            print(f"Technique: Boundary Value Analysis, Stress/Load Testing")
            print(f"Tool: Selenium + JMeter")
            print(f"Dynamic Testing: Stress/Load Testing")
            print(f"Input: Số lượng = {self.test_data['quantity']}")
            print(f"Expected: {self.test_data['expected_message']}")
            
            # Create JMeter script
            jmeter_script = self.create_jmeter_script()
            
            # Run load testing
            result = self.execute_load_testing()
            
            print(f"\n🏁 FINAL RESULT: {result['status']}")
            print(f"📝 Message: {result['message']}")
            
            return result
            
        except Exception as e:
            error_info = self.error_handlers.handle_selenium_error(e, self.driver, "TC09")
            error_msg = f"Test execution error: {str(e)}"
            print(f"💥 ERROR: {error_msg}")
            return {"status": "ERROR", "message": error_msg}
        finally:
            self.teardown()

def run_test_case_09():
    """Entry point cho Test Case 9"""
    test = TestCase09()
    return test.run_test()

if __name__ == "__main__":
    # Setup logging
    ErrorHandlers.setup_logging()
    
    result = run_test_case_09()
    print(f"\n🎯 Test Case #9 Result: {result['status']}")