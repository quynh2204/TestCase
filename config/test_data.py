"""
Dữ liệu test cho các test cases
"""

class TestData:
    """Test data cho các test cases"""
    
    # Test Case 5: Không chọn phân loại
    TC5_DATA = {
        "category_selection": None,  # Không chọn
        "quantity": 1,
        "expected_message": "Vui lòng chọn một khóa học"
    }
    
    # Test Case 6: Số lượng = 0
    TC6_DATA = {
        "category_selection": "default",
        "quantity": 0,
        "expected_behavior": "reset_to_1",
        "expected_cart_items": 0
    }
    
    # Test Case 7: Số lượng = -1
    TC7_DATA = {
        "category_selection": "default",
        "quantity": -1,
        "expected_behavior": "reset_to_1",
        "expected_cart_items": 0
    }
    
    # Test Case 8: Số lượng = chữ "e"
    TC8_DATA = {
        "category_selection": "default",
        "quantity": "e",
        "expected_message": "Hãy nhập số hợp lệ",
        "expected_cart_items": 0
    }
    
    # Test Case 9: Số lượng = 999999
    TC9_DATA = {
        "category_selection": "default",
        "quantity": 999999,
        "expected_message": "Số lượng không hợp lệ",
        "expected_cart_items": 0
    }
    
    # Test Case 10: Ký tự đặc biệt
    TC10_DATA = {
        "category_selection": "default",
        "quantity": "!@#",
        "expected_message": "Hãy nhập số hợp lệ",
        "expected_cart_items": 0
    }