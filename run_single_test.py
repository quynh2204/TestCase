"""
Script chạy test case đơn lẻ
Author: quynh2204
Date: 2025-08-20
"""

import sys
import os
import argparse
from datetime import datetime

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config.settings import CURRENT_USER
from utils.error_handlers import ErrorHandlers

# Import all test cases
from tests.test_case_05 import run_test_case_05
from tests.test_case_06 import run_test_case_06  
from tests.test_case_07 import run_test_case_07
from tests.test_case_08 import run_test_case_08
from tests.test_case_09 import run_test_case_09
from tests.test_case_10 import run_test_case_10

# Test case mapping
TEST_CASES = {
    '05': {
        'function': run_test_case_05,
        'description': 'Input Validation - Không chọn phân loại',
        'techniques': 'Input Validation, Decision Table'
    },
    '06': {
        'function': run_test_case_06,
        'description': 'Boundary Value Analysis - Số lượng = 0',
        'techniques': 'Boundary Value Analysis, Validation Testing'
    },
    '07': {
        'function': run_test_case_07,
        'description': 'Error Handling - Số lượng = -1',
        'techniques': 'Equivalence Partitioning, Error Guessing'
    },
    '08': {
        'function': run_test_case_08,
        'description': 'Input Validation - Nhập chữ e',
        'techniques': 'Equivalence Partitioning, Error Guessing'
    },
    '09': {
        'function': run_test_case_09,
        'description': 'Stress Testing - Số lượng = 999999',
        'techniques': 'Boundary Value Analysis, Stress/Load Testing'
    },
    '10': {
        'function': run_test_case_10,
        'description': 'Error Handling - Ký tự đặc biệt',
        'techniques': 'Equivalence Partitioning, Error Guessing'
    }
}

def list_available_tests():
    """Hiển thị danh sách test cases có sẵn"""
    print("📋 AVAILABLE TEST CASES:")
    print("=" * 60)
    for test_id, test_info in TEST_CASES.items():
        print(f"TC{test_id}: {test_info['description']}")
        print(f"       Techniques: {test_info['techniques']}")
        print("-" * 60)

def run_specific_test(test_id):
    """
    Chạy test case cụ thể
    
    Args:
        test_id (str): ID của test case (05, 06, 07, 08, 09, 10)
    """
    
    if test_id not in TEST_CASES:
        print(f"❌ Test case TC{test_id} không tồn tại!")
        print("📋 Các test cases có sẵn:")
        for tid in TEST_CASES.keys():
            print(f"   TC{tid}")
        return False
    
    # Setup logging
    log_file = ErrorHandlers.setup_logging()
    
    test_info = TEST_CASES[test_id]
    
    print("🚀 RUNNING SINGLE TEST CASE")
    print("=" * 50)
    print(f"User: {CURRENT_USER}")
    print(f"Test ID: TC{test_id}")
    print(f"Description: {test_info['description']}")
    print(f"Techniques: {test_info['techniques']}")
    print(f"Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Log file: {log_file}")
    print("=" * 50)
    
    try:
        start_time = datetime.now()
        result = test_info['function']()
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        print("\n" + "=" * 50)
        print("🏁 TEST EXECUTION COMPLETED")
        print("=" * 50)
        print(f"📊 Result: {result['status']}")
        print(f"📝 Message: {result['message']}")
        print(f"⏱️ Duration: {duration:.2f} seconds")
        print(f"🕐 End time: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 50)
        
        return result['status'] == 'PASSED'
        
    except Exception as e:
        print(f"\n💥 ERROR executing test TC{test_id}: {str(e)}")
        return False

def main():
    """Main function với argument parsing"""
    parser = argparse.ArgumentParser(
        description='Chạy test case đơn lẻ cho E-Commerce Product Testing',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ví dụ sử dụng:
  python run_single_test.py --test 05        # Chạy test case 05
  python run_single_test.py --test 09        # Chạy test case 09
  python run_single_test.py --list           # Hiển thị danh sách test cases
  python run_single_test.py --help           # Hiển thị hướng dẫn này

Test Cases có sẵn: 05, 06, 07, 08, 09, 10
        """
    )
    
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        '--test', '-t',
        type=str,
        help='ID của test case cần chạy (05, 06, 07, 08, 09, 10)'
    )
    group.add_argument(
        '--list', '-l',
        action='store_true',
        help='Hiển thị danh sách test cases có sẵn'
    )
    
    args = parser.parse_args()
    
    if args.list:
        list_available_tests()
        return
    
    if args.test:
        # Normalize test ID
        test_id = args.test.zfill(2)  # Pad with zero if needed
        success = run_specific_test(test_id)
        sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()