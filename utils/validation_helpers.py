"""
Helper functions cho Input Validation Testing
"""

import re
from typing import Union, List, Dict

class ValidationHelpers:
    """Helper class cho validation testing"""
    
    @staticmethod
    def validate_numeric_input(value: Union[str, int, float]) -> Dict[str, any]:
        """
        Validate numeric input
        
        Args:
            value: Value to validate
            
        Returns:
            dict: Validation result with is_valid, message, cleaned_value
        """
        try:
            # Convert to string for processing
            str_value = str(value).strip()
            
            # Check if empty
            if not str_value:
                return {
                    "is_valid": False,
                    "message": "Input không được để trống",
                    "cleaned_value": None
                }
            
            # Check if contains only digits and allowed characters
            if re.match(r'^-?\d+$', str_value):
                numeric_value = int(str_value)
                
                if numeric_value < 0:
                    return {
                        "is_valid": False,
                        "message": "Không cho phép số âm",
                        "cleaned_value": None
                    }
                elif numeric_value == 0:
                    return {
                        "is_valid": False,
                        "message": "Số lượng phải lớn hơn 0",
                        "cleaned_value": None
                    }
                else:
                    return {
                        "is_valid": True,
                        "message": "Valid numeric input",
                        "cleaned_value": numeric_value
                    }
            else:
                return {
                    "is_valid": False,
                    "message": "Chỉ cho phép nhập số",
                    "cleaned_value": None
                }
                
        except Exception as e:
            return {
                "is_valid": False,
                "message": f"Validation error: {str(e)}",
                "cleaned_value": None
            }
    
    @staticmethod
    def validate_special_characters(value: str) -> Dict[str, any]:
        """
        Check for special characters in input
        
        Args:
            value: String value to check
            
        Returns:
            dict: Validation result
        """
        special_chars = re.findall(r'[!@#$%^&*()_+=\[\]{}|;:,.<>?]', value)
        
        if special_chars:
            return {
                "has_special_chars": True,
                "special_chars_found": list(set(special_chars)),
                "message": f"Chứa ký tự đặc biệt: {', '.join(set(special_chars))}"
            }
        else:
            return {
                "has_special_chars": False,
                "special_chars_found": [],
                "message": "Không chứa ký tự đặc biệt"
            }
    
    @staticmethod
    def get_equivalence_classes(data_type: str) -> Dict[str, List]:
        """
        Get equivalence classes for different data types
        
        Args:
            data_type: Type of data (quantity, text, etc.)
            
        Returns:
            dict: Equivalence classes
        """
        if data_type == "quantity":
            return {
                "valid_positive": [1, 2, 5, 10, 100],
                "invalid_zero": [0],
                "invalid_negative": [-1, -2, -10],
                "invalid_decimal": [1.5, 2.7, -1.2],
                "invalid_text": ["abc", "xyz", "test"],
                "invalid_special": ["!@#", "$%^", "()"],
                "invalid_mixed": ["1a", "2b", "a1"],
                "invalid_empty": ["", " ", None]
            }
        elif data_type == "category":
            return {
                "valid_selections": ["option1", "option2", "option3"],
                "invalid_none": [None, ""],
                "invalid_nonexistent": ["fake_option", "invalid_choice"]
            }
        else:
            return {}