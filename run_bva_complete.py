"""
Script chạy Complete BVA Testing
"""

from tests.test_case_bva_comprehensive import run_comprehensive_bva_test
from config.boundary_value_table import BoundaryValueTable

def main():
    print("📊 BOUNDARY VALUE ANALYSIS - COMPLETE TESTING")
    print("=" * 60)
    
    # Show BVA table
    BoundaryValueTable.print_bva_table()
    
    print(f"\nPress Enter to start comprehensive BVA test...")
    input()
    
    # Run comprehensive test
    result = run_comprehensive_bva_test()
    
    print(f"\n🎯 FINAL RESULT: {result['status']}")
    print(f"📝 MESSAGE: {result['message']}")

if __name__ == "__main__":
    main()