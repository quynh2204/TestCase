"""
Helper functions cho Boundary Value Analysis
"""

from typing import List, Dict, Tuple

class BoundaryHelpers:
    """Helper class cho boundary value testing"""
    
    @staticmethod
    def get_boundary_values(min_value: int, max_value: int) -> Dict[str, List[int]]:
        """
        Generate boundary values for testing
        
        Args:
            min_value: Minimum valid value
            max_value: Maximum valid value
            
        Returns:
            dict: Boundary values categorized
        """
        return {
            "below_minimum": [min_value - 2, min_value - 1],
            "minimum": [min_value],
            "just_above_minimum": [min_value + 1],
            "normal_values": [
                min_value + (max_value - min_value) // 4,
                min_value + (max_value - min_value) // 2,
                min_value + 3 * (max_value - min_value) // 4
            ],
            "just_below_maximum": [max_value - 1],
            "maximum": [max_value],
            "above_maximum": [max_value + 1, max_value + 2]
        }
    
    @staticmethod
    def analyze_boundary_behavior(input_value: int, min_val: int, max_val: int) -> Dict[str, any]:
        """
        Analyze boundary behavior for input
        
        Args:
            input_value: Value to analyze
            min_val: Minimum boundary
            max_val: Maximum boundary
            
        Returns:
            dict: Analysis result
        """
        if input_value < min_val:
            return {
                "category": "below_minimum",
                "expected_behavior": "reject_or_reset",
                "risk_level": "high",
                "description": f"Value {input_value} is below minimum {min_val}"
            }
        elif input_value == min_val:
            return {
                "category": "minimum_boundary",
                "expected_behavior": "accept",
                "risk_level": "medium",
                "description": f"Value {input_value} is at minimum boundary"
            }
        elif input_value > max_val:
            return {
                "category": "above_maximum",
                "expected_behavior": "reject_or_limit",
                "risk_level": "high",
                "description": f"Value {input_value} exceeds maximum {max_val}"
            }
        elif input_value == max_val:
            return {
                "category": "maximum_boundary",
                "expected_behavior": "accept",
                "risk_level": "medium",
                "description": f"Value {input_value} is at maximum boundary"
            }
        else:
            return {
                "category": "within_range",
                "expected_behavior": "accept",
                "risk_level": "low",
                "description": f"Value {input_value} is within valid range"
            }
    
    @staticmethod
    def get_quantity_boundaries() -> Dict[str, int]:
        """
        Get standard quantity boundaries for e-commerce
        
        Returns:
            dict: Boundary values
        """
        return {
            "absolute_minimum": 1,
            "practical_minimum": 1,
            "reasonable_maximum": 100,
            "system_maximum": 9999,
            "stress_test_value": 999999
        }