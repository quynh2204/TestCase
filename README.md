# 🧪 E-Commerce Product Testing Automation

Dự án automation testing cho trang sản phẩm e-commerce sử dụng Selenium WebDriver với Python.

## 👤 **Thông tin dự án**
- **Author:** quynh2204
- **Date:** 2025-08-20 13:22:57
- **Framework:** Selenium WebDriver
- **Language:** Python 3.x
- **Target URL:** https://atd.ueh.edu.vn/business-analyst-in-practices-p16.html

## 📋 **Test Cases**

| Test ID | Description | Techniques | Dynamic Testing | Input | Expected Result |
|---------|-------------|------------|-----------------|-------|-----------------|
| **TC05** | Không chọn phân loại đối tượng | Input Validation, Decision Table | Input Validation | Không chọn phân loại | Hiển thị thông báo lỗi "Vui lòng chọn một khóa học" |
| **TC06** | Số lượng = 0 | Boundary Value Analysis, Validation Testing | Boundary Condition Testing | Số lượng = 0 | Không thêm vào giỏ hàng, reset về 1 |
| **TC07** | Số lượng = -1 | Equivalence Partitioning, Error Guessing | Error Handling | Số lượng = -1 | Không cho phép số âm, reset về 1 |
| **TC08** | Nhập chữ "e" | Equivalence Partitioning, Error Guessing | Input Validation | Số lượng = "e" | Hiển thị lỗi "Hãy nhập số hợp lệ" |
| **TC09** | Số lượng = 999999 | Boundary Value Analysis, Stress/Load Testing | Stress/Load Testing | Số lượng = 999999 | Hiển thị "Số lượng không hợp lệ" |
| **TC10** | Ký tự đặc biệt | Equivalence Partitioning, Error Guessing | Error Handling | Số lượng = "!@#" | Hiển thị lỗi "Hãy nhập số hợp lệ" |

## 🛠️ **Cài đặt**

### **1. Yêu cầu hệ thống**
- Python 3.7 trở lên
- Google Chrome browser
- Internet connection

### **2. Clone dự án**
```bash
git clone <repository-url>
cd QAQC_ECommerce_Testing