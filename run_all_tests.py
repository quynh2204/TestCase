"""
Script chạy tất cả test cases - COMPLETE VERSION
Author: quynh2204
Date: 2025-08-20
"""

import time
from datetime import datetime
import json
import os
import sys

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config.settings import CURRENT_USER, TEST_DATE
from utils.error_handlers import ErrorHandlers

# Import all test cases
from tests.test_case_05 import run_test_case_05
from tests.test_case_06 import run_test_case_06  
from tests.test_case_07 import run_test_case_07
from tests.test_case_08 import run_test_case_08
from tests.test_case_09 import run_test_case_09
from tests.test_case_10 import run_test_case_10

def run_all_tests():
    """Chạy tất cả test cases và tạo báo cáo"""
    
    # Setup logging
    log_file = ErrorHandlers.setup_logging()
    print(f"📄 Log file: {log_file}")
    
    print("🚀 STARTING COMPLETE AUTOMATION TEST SUITE")
    print("=" * 80)
    print(f"User: {CURRENT_USER}")
    print(f"Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)
    
    test_cases = [
        {
            "id": "TC05", 
            "function": run_test_case_05, 
            "description": "Input Validation - Không chọn phân loại",
            "techniques": "Input Validation, Decision Table",
            "dynamic_testing": "Input Validation",
            "input": "Không chọn phân loại đối tượng",
            "expected": "Hiển thị thông báo lỗi 'Vui lòng chọn một khóa học'"
        },
        {
            "id": "TC06", 
            "function": run_test_case_06, 
            "description": "Boundary Value Analysis - Số lượng = 0",
            "techniques": "Boundary Value Analysis, Validation Testing",
            "dynamic_testing": "Boundary Condition Testing",
            "input": "Số lượng = 0",
            "expected": "Không thêm khóa học vào giỏ hàng, số lượng reset về 1"
        },
        {
            "id": "TC07", 
            "function": run_test_case_07, 
            "description": "Error Handling - Số lượng = -1",
            "techniques": "Equivalence Partitioning, Error Guessing",
            "dynamic_testing": "Error Handling",
            "input": "Số lượng = -1",
            "expected": "Không cho phép nhập số âm, số lượng reset về 1"
        },
        {
            "id": "TC08", 
            "function": run_test_case_08, 
            "description": "Input Validation - Nhập chữ 'e'",
            "techniques": "Equivalence Partitioning, Error Guessing",
            "dynamic_testing": "Input Validation",
            "input": "Số lượng = 'e'",
            "expected": "Hiển thị lỗi 'Hãy nhập số hợp lệ', không thêm sản phẩm vào giỏ hàng"
        },
        {
            "id": "TC09", 
            "function": run_test_case_09, 
            "description": "Stress Testing - Số lượng = 999999",
            "techniques": "Boundary Value Analysis, Stress/Load Testing",
            "dynamic_testing": "Stress/Load Testing",
            "input": "Số lượng = 999999",
            "expected": "Hiển thị thông báo 'Số lượng không hợp lệ', không thêm khóa học"
        },
        {
            "id": "TC10", 
            "function": run_test_case_10, 
            "description": "Error Handling - Ký tự đặc biệt '!@#'",
            "techniques": "Equivalence Partitioning, Error Guessing",
            "dynamic_testing": "Error Handling",
            "input": "Số lượng = !@#",
            "expected": "Hiển thị lỗi 'Hãy nhập số hợp lệ', không thêm sản phẩm vào giỏ hàng"
        }
    ]
    
    results = []
    passed = 0
    failed = 0
    errors = 0
    total_execution_time = 0
    
    suite_start_time = time.time()
    
    for test_case in test_cases:
        print(f"\n{'='*25} {test_case['id']} {'='*25}")
        print(f"📋 Description: {test_case['description']}")
        print(f"🔧 Techniques: {test_case['techniques']}")
        print(f"⚡ Dynamic Testing: {test_case['dynamic_testing']}")
        print(f"📥 Input: {test_case['input']}")
        print(f"📤 Expected: {test_case['expected']}")
        print("-" * 70)
        
        start_time = time.time()
        
        try:
            result = test_case['function']()
            execution_time = time.time() - start_time
            total_execution_time += execution_time
            
            # Enrich result with test case metadata
            result['test_id'] = test_case['id']
            result['description'] = test_case['description']
            result['techniques'] = test_case['techniques']
            result['dynamic_testing'] = test_case['dynamic_testing']
            result['input'] = test_case['input']
            result['expected'] = test_case['expected']
            result['execution_time'] = round(execution_time, 2)
            result['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            results.append(result)
            
            if result['status'] == 'PASSED':
                passed += 1
                print(f"✅ {test_case['id']}: PASSED ({execution_time:.2f}s)")
            elif result['status'] == 'FAILED':
                failed += 1
                print(f"❌ {test_case['id']}: FAILED ({execution_time:.2f}s)")
            else:
                errors += 1
                print(f"💥 {test_case['id']}: ERROR ({execution_time:.2f}s)")
                
        except Exception as e:
            execution_time = time.time() - start_time
            total_execution_time += execution_time
            error_result = {
                'test_id': test_case['id'],
                'description': test_case['description'],
                'techniques': test_case['techniques'],
                'dynamic_testing': test_case['dynamic_testing'],
                'input': test_case['input'],
                'expected': test_case['expected'],
                'status': 'ERROR',
                'message': f'Exception during execution: {str(e)}',
                'execution_time': round(execution_time, 2),
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            results.append(error_result)
            errors += 1
            print(f"💥 {test_case['id']}: ERROR - {str(e)} ({execution_time:.2f}s)")
    
    suite_end_time = time.time()
    suite_duration = suite_end_time - suite_start_time
    
    # Tạo báo cáo
    report_files = generate_test_report(results, passed, failed, errors, suite_duration)
    
    print("\n" + "=" * 80)
    print("🏁 TEST SUITE COMPLETED")
    print("=" * 80)
    print(f"📊 SUMMARY:")
    print(f"   ✅ Passed: {passed}")
    print(f"   ❌ Failed: {failed}")
    print(f"   💥 Errors: {errors}")
    print(f"   📈 Total: {len(results)}")
    print(f"   🎯 Pass Rate: {round((passed / len(results)) * 100, 2)}%" if results else "0%")
    print(f"   ⏱️ Total Execution Time: {suite_duration:.2f} seconds")
    print(f"   ⏱️ Average Test Time: {total_execution_time/len(results):.2f} seconds" if results else "N/A")
    print(f"📄 Reports Generated:")
    for report_file in report_files:
        print(f"   📋 {report_file}")
    print(f"🕐 End time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)
    
    return results

def generate_test_report(results, passed, failed, errors, suite_duration):
    """Tạo báo cáo test dạng JSON, HTML và CSV"""
    
    timestamp = int(time.time())
    report_files = []
    
    # Summary data
    summary_data = {
        'test_suite': 'E-Commerce Product Testing - Complete Suite',
        'user': CURRENT_USER,
        'execution_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'suite_duration': round(suite_duration, 2),
        'summary': {
            'total': len(results),
            'passed': passed,
            'failed': failed,
            'errors': errors,
            'pass_rate': round((passed / len(results)) * 100, 2) if results else 0
        },
        'test_results': results,
        'metadata': {
            'framework': 'Selenium WebDriver',
            'python_version': sys.version,
            'platform': os.name,
            'techniques_used': list(set([r.get('techniques', '') for r in results])),
            'dynamic_testing_types': list(set([r.get('dynamic_testing', '') for r in results]))
        }
    }
    
    # 1. JSON Report
    json_file = f"reports/test_results/test_report_{timestamp}.json"
    os.makedirs(os.path.dirname(json_file), exist_ok=True)
    
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(summary_data, f, ensure_ascii=False, indent=2)
    
    report_files.append(json_file)
    
    # 2. HTML Report
    html_report = generate_html_report(summary_data)
    html_file = f"reports/test_results/test_report_{timestamp}.html"
    
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(html_report)
    
    report_files.append(html_file)
    
    # 3. CSV Report
    csv_file = generate_csv_report(results, timestamp)
    report_files.append(csv_file)
    
    return report_files

def generate_html_report(report_data):
    """Tạo báo cáo HTML chi tiết"""
    
    # Calculate additional metrics
    techniques_stats = {}
    dynamic_testing_stats = {}
    
    for result in report_data['test_results']:
        # Count techniques
        techniques = result.get('techniques', '').split(', ')
        for technique in techniques:
            if technique.strip():
                techniques_stats[technique.strip()] = techniques_stats.get(technique.strip(), 0) + 1
        
        # Count dynamic testing types
        dt_type = result.get('dynamic_testing', '')
        if dt_type:
            dynamic_testing_stats[dt_type] = dynamic_testing_stats.get(dt_type, 0) + 1
    
    html = f"""
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>📊 E-Commerce Testing Report - {report_data['execution_date']}</title>
    <style>
        body {{ 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            margin: 0; 
            padding: 20px; 
            background-color: #f5f5f5;
        }}
        .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 0 20px rgba(0,0,0,0.1); }}
        .header {{ 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
            color: white; 
            padding: 30px; 
            border-radius: 10px; 
            margin-bottom: 30px;
            text-align: center;
        }}
        .header h1 {{ margin: 0; font-size: 2.5em; }}
        .header p {{ margin: 10px 0 0 0; opacity: 0.9; }}
        
        .metrics-grid {{ 
            display: grid; 
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); 
            gap: 20px; 
            margin-bottom: 30px; 
        }}
        .metric-card {{ 
            background: #f8f9fa; 
            padding: 20px; 
            border-radius: 8px; 
            text-align: center; 
            border-left: 4px solid #007bff;
        }}
        .metric-value {{ font-size: 2em; font-weight: bold; color: #333; }}
        .metric-label {{ color: #666; margin-top: 5px; }}
        
        .section {{ margin: 30px 0; }}
        .section h2 {{ 
            color: #333; 
            border-bottom: 2px solid #007bff; 
            padding-bottom: 10px;
            display: flex;
            align-items: center;
        }}
        .section h2:before {{ content: '📊'; margin-right: 10px; }}
        
        table {{ 
            border-collapse: collapse; 
            width: 100%; 
            margin: 20px 0;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        th, td {{ 
            border: 1px solid #ddd; 
            padding: 12px; 
            text-align: left; 
        }}
        th {{ 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
            color: white; 
            font-weight: 600;
        }}
        tr:nth-child(even) {{ background-color: #f8f9fa; }}
        tr:hover {{ background-color: #e3f2fd; }}
        
        .status {{ 
            padding: 6px 12px; 
            border-radius: 20px; 
            font-weight: bold; 
            text-transform: uppercase;
            font-size: 0.8em;
        }}
        .passed {{ background: #d4edda; color: #155724; }}
        .failed {{ background: #f8d7da; color: #721c24; }}
        .error {{ background: #fff3cd; color: #856404; }}
        
        .technique-badge {{ 
            display: inline-block; 
            background: #e3f2fd; 
            color: #1976d2; 
            padding: 4px 8px; 
            border-radius: 12px; 
            font-size: 0.8em; 
            margin: 2px;
        }}
        
        .chart-container {{ 
            background: #f8f9fa; 
            padding: 20px; 
            border-radius: 8px; 
            margin: 20px 0;
        }}
        
        .footer {{ 
            margin-top: 40px; 
            padding-top: 20px; 
            border-top: 1px solid #ddd; 
            text-align: center; 
            color: #666;
        }}
        
        @media (max-width: 768px) {{
            .container {{ padding: 15px; }}
            .metrics-grid {{ grid-template-columns: 1fr; }}
            table {{ font-size: 0.9em; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🧪 E-Commerce Product Testing Report</h1>
            <p><strong>User:</strong> {report_data['user']} | <strong>Date:</strong> {report_data['execution_date']}</p>
            <p><strong>Duration:</strong> {report_data['suite_duration']} seconds</p>
        </div>
        
        <div class="metrics-grid">
            <div class="metric-card">
                <div class="metric-value">{report_data['summary']['total']}</div>
                <div class="metric-label">Total Tests</div>
            </div>
            <div class="metric-card">
                <div class="metric-value" style="color: #28a745;">{report_data['summary']['passed']}</div>
                <div class="metric-label">Passed</div>
            </div>
            <div class="metric-card">
                <div class="metric-value" style="color: #dc3545;">{report_data['summary']['failed']}</div>
                <div class="metric-label">Failed</div>
            </div>
            <div class="metric-card">
                <div class="metric-value" style="color: #ffc107;">{report_data['summary']['errors']}</div>
                <div class="metric-label">Errors</div>
            </div>
            <div class="metric-card">
                <div class="metric-value" style="color: #007bff;">{report_data['summary']['pass_rate']}%</div>
                <div class="metric-label">Pass Rate</div>
            </div>
        </div>
        
        <div class="section">
            <h2>🔧 Testing Techniques Used</h2>
            <div class="chart-container">
    """
    
    for technique, count in techniques_stats.items():
        html += f'<span class="technique-badge">{technique} ({count})</span> '
    
    html += f"""
            </div>
        </div>
        
        <div class="section">
            <h2>⚡ Dynamic Testing Types</h2>
            <div class="chart-container">
    """
    
    for dt_type, count in dynamic_testing_stats.items():
        html += f'<span class="technique-badge">{dt_type} ({count})</span> '
    
    html += f"""
            </div>
        </div>
        
        <div class="section">
            <h2>📋 Detailed Test Results</h2>
            <table>
                <thead>
                    <tr>
                        <th>Test ID</th>
                        <th>Description</th>
                        <th>Input</th>
                        <th>Expected Result</th>
                        <th>Status</th>
                        <th>Actual Result</th>
                        <th>Techniques</th>
                        <th>Dynamic Testing</th>
                        <th>Execution Time (s)</th>
                        <th>Timestamp</th>
                    </tr>
                </thead>
                <tbody>
    """
    
    for result in report_data['test_results']:
        status_class = result['status'].lower()
        techniques_formatted = '</span> <span class="technique-badge">'.join(result.get('techniques', '').split(', '))
        if techniques_formatted:
            techniques_formatted = f'<span class="technique-badge">{techniques_formatted}</span>'
        
        html += f"""
                    <tr>
                        <td><strong>{result['test_id']}</strong></td>
                        <td>{result['description']}</td>
                        <td><code>{result.get('input', 'N/A')}</code></td>
                        <td>{result.get('expected', 'N/A')}</td>
                        <td><span class="status {status_class}">{result['status']}</span></td>
                        <td>{result['message']}</td>
                        <td>{techniques_formatted}</td>
                        <td><span class="technique-badge">{result.get('dynamic_testing', 'N/A')}</span></td>
                        <td>{result['execution_time']}</td>
                        <td>{result['timestamp']}</td>
                    </tr>
        """
    
    html += f"""
                </tbody>
            </table>
        </div>
        
        <div class="section">
            <h2>🔍 Test Environment Details</h2>
            <div class="chart-container">
                <p><strong>Framework:</strong> {report_data['metadata']['framework']}</p>
                <p><strong>Python Version:</strong> {report_data['metadata']['python_version']}</p>
                <p><strong>Platform:</strong> {report_data['metadata']['platform']}</p>
                <p><strong>Test URL:</strong> https://atd.ueh.edu.vn/business-analyst-in-practices-p16.html</p>
            </div>
        </div>
        
        <div class="footer">
            <p>Generated by QAQC Automation Framework | quynh2204 | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <p>🔧 Powered by Selenium WebDriver | 📊 Dynamic Testing Techniques Applied</p>
        </div>
    </div>
</body>
</html>
    """
    
    return html

def generate_csv_report(results, timestamp):
    """Tạo báo cáo CSV"""
    import csv
    
    csv_file = f"reports/test_results/test_report_{timestamp}.csv"
    
    with open(csv_file, 'w', newline='', encoding='utf-8') as f:
        fieldnames = [
            'test_id', 'description', 'input', 'expected', 'status', 
            'message', 'techniques', 'dynamic_testing', 'execution_time', 'timestamp'
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        
        writer.writeheader()
        for result in results:
            writer.writerow({
                'test_id': result.get('test_id', ''),
                'description': result.get('description', ''),
                'input': result.get('input', ''),
                'expected': result.get('expected', ''),
                'status': result.get('status', ''),
                'message': result.get('message', ''),
                'techniques': result.get('techniques', ''),
                'dynamic_testing': result.get('dynamic_testing', ''),
                'execution_time': result.get('execution_time', ''),
                'timestamp': result.get('timestamp', '')
            })
    
    return csv_file

if __name__ == "__main__":
    run_all_tests()