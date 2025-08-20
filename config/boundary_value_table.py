"""
Boundary Value Analysis Table for E-Commerce Product Testing
Based on standard BVA methodology
Author: quynh2204
Date: 2025-08-20 14:31:42
"""

class BoundaryValueTable:
    """
    Boundary Value Analysis Table cho Quantity field
    Theo chuẩn BVA: Valid Boundaries, Invalid Boundaries, Tags
    """
    
    # Field: Quantity (Số lượng sản phẩm)
    QUANTITY_BVA = {
        "field_name": "Quantity",
        "data_type": "Integer",
        "valid_range": "1 - 999",
        
        "boundaries": {
            # VALID BOUNDARIES
            "valid_boundaries": {
                "V1": {"value": 1, "description": "Minimum valid value", "tag": "Lower bound"},
                "V2": {"value": 2, "description": "Just above minimum", "tag": "Lower bound + 1"},
                "V3": {"value": 500, "description": "Middle valid value", "tag": "Normal value"},
                "V4": {"value": 998, "description": "Just below maximum", "tag": "Upper bound - 1"},
                "V5": {"value": 999, "description": "Maximum valid value", "tag": "Upper bound"}
            },
            
            # INVALID BOUNDARIES  
            "invalid_boundaries": {
                "X1": {"value": 0, "description": "Below minimum", "tag": "Lower bound - 1"},
                "X2": {"value": -1, "description": "Negative value", "tag": "Invalid negative"},
                "X3": {"value": -999, "description": "Large negative", "tag": "Extreme negative"},
                "X4": {"value": 1000, "description": "Just above maximum", "tag": "Upper bound + 1"},
                "X5": {"value": 9999, "description": "Large invalid value", "tag": "Extreme positive"},
                "X6": {"value": 999999, "description": "Stress test value", "tag": "Stress boundary"},
                "X7": {"value": "abc", "description": "Text input", "tag": "Non-numeric"},
                "X8": {"value": "!@#", "description": "Special characters", "tag": "Invalid chars"},
                "X9": {"value": "", "description": "Empty input", "tag": "Null input"},
                "X10": {"value": " ", "description": "Whitespace", "tag": "Space input"},
                "X11": {"value": "1.5", "description": "Decimal value", "tag": "Invalid decimal"},
                "X12": {"value": None, "description": "Null value", "tag": "Null"}
            }
        }
    }
    
    # Field: Category Selection (Phân loại đối tượng)
    CATEGORY_BVA = {
        "field_name": "Category Selection",
        "data_type": "Selection",
        "valid_range": "Must select one option",
        
        "boundaries": {
            "valid_boundaries": {
                "V1": {"value": "option_1", "description": "First valid option", "tag": "Valid selection"},
                "V2": {"value": "option_2", "description": "Second valid option", "tag": "Valid selection"},
                "V3": {"value": "option_n", "description": "Last valid option", "tag": "Valid selection"}
            },
            
            "invalid_boundaries": {
                "X1": {"value": None, "description": "No selection", "tag": "Null selection"},
                "X2": {"value": "", "description": "Empty selection", "tag": "Empty value"},
                "X3": {"value": "invalid_option", "description": "Non-existent option", "tag": "Invalid option"}
            }
        }
    }

    @staticmethod
    def get_test_data_matrix():
        """
        Tạo ma trận test data theo BVA
        Returns: Dictionary với organized test cases
        """
        return {
            "quantity_valid_boundaries": [
                {"test_id": "BVA_V1", "input": 1, "expected": "Accept", "boundary_type": "valid_min"},
                {"test_id": "BVA_V2", "input": 2, "expected": "Accept", "boundary_type": "valid_min_plus"},
                {"test_id": "BVA_V3", "input": 500, "expected": "Accept", "boundary_type": "valid_normal"},
                {"test_id": "BVA_V4", "input": 998, "expected": "Accept", "boundary_type": "valid_max_minus"},
                {"test_id": "BVA_V5", "input": 999, "expected": "Accept", "boundary_type": "valid_max"}
            ],
            
            "quantity_invalid_boundaries": [
                {"test_id": "BVA_X1", "input": 0, "expected": "Reject/Reset", "boundary_type": "invalid_zero"},
                {"test_id": "BVA_X2", "input": -1, "expected": "Reject/Reset", "boundary_type": "invalid_negative"},
                {"test_id": "BVA_X3", "input": -999, "expected": "Reject/Reset", "boundary_type": "invalid_large_negative"},
                {"test_id": "BVA_X4", "input": 1000, "expected": "Reject", "boundary_type": "invalid_over_max"},
                {"test_id": "BVA_X5", "input": 9999, "expected": "Reject", "boundary_type": "invalid_large"},
                {"test_id": "BVA_X6", "input": 999999, "expected": "Reject", "boundary_type": "invalid_stress"},
                {"test_id": "BVA_X7", "input": "abc", "expected": "Reject", "boundary_type": "invalid_text"},
                {"test_id": "BVA_X8", "input": "!@#", "expected": "Reject", "boundary_type": "invalid_special"},
                {"test_id": "BVA_X9", "input": "", "expected": "Reject", "boundary_type": "invalid_empty"},
                {"test_id": "BVA_X10", "input": " ", "expected": "Reject", "boundary_type": "invalid_space"},
                {"test_id": "BVA_X11", "input": "1.5", "expected": "Reject", "boundary_type": "invalid_decimal"},
                {"test_id": "BVA_X12", "input": None, "expected": "Reject", "boundary_type": "invalid_null"}
            ]
        }

    @staticmethod
    def print_bva_table():
        """In bảng BVA theo format chuẩn"""
        print("📊 BOUNDARY VALUE ANALYSIS TABLE")
        print("=" * 80)
        print(f"Field: Quantity | Data Type: Integer | Valid Range: 1-999")
        print("=" * 80)
        
        print("\n✅ VALID BOUNDARIES:")
        print(f"{'Tag':<6} {'Value':<10} {'Description':<25} {'Expected':<15}")
        print("-" * 60)
        
        valid_data = [
            ("V1", "1", "Minimum valid value", "Accept"),
            ("V2", "2", "Just above minimum", "Accept"),
            ("V3", "500", "Middle valid value", "Accept"),
            ("V4", "998", "Just below maximum", "Accept"),
            ("V5", "999", "Maximum valid value", "Accept")
        ]
        
        for tag, value, desc, expected in valid_data:
            print(f"{tag:<6} {value:<10} {desc:<25} {expected:<15}")
        
        print("\n❌ INVALID BOUNDARIES:")
        print(f"{'Tag':<6} {'Value':<10} {'Description':<25} {'Expected':<15}")
        print("-" * 60)
        
        invalid_data = [
            ("X1", "0", "Below minimum", "Reject/Reset"),
            ("X2", "-1", "Negative value", "Reject/Reset"),
            ("X3", "-999", "Large negative", "Reject/Reset"),
            ("X4", "1000", "Just above maximum", "Reject"),
            ("X5", "9999", "Large invalid value", "Reject"),
            ("X6", "999999", "Stress test value", "Reject"),
            ("X7", "abc", "Text input", "Reject"),
            ("X8", "!@#", "Special characters", "Reject"),
            ("X9", "''", "Empty input", "Reject"),
            ("X10", "' '", "Whitespace", "Reject"),
            ("X11", "1.5", "Decimal value", "Reject"),
            ("X12", "null", "Null value", "Reject")
        ]
        
        for tag, value, desc, expected in invalid_data:
            print(f"{tag:<6} {value:<10} {desc:<25} {expected:<15}")