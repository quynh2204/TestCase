"""
Cấu hình chung cho automation testing
Author: quynh2204
Date: 2025-08-20
"""

import os
from datetime import datetime

# URLs
BASE_URL = "https://atd.ueh.edu.vn"
PRODUCT_URL = "https://atd.ueh.edu.vn/business-analyst-in-practices-p16.html"

# Timeouts (seconds)
IMPLICIT_WAIT = 10
EXPLICIT_WAIT = 15
PAGE_LOAD_TIMEOUT = 30

# Browser settings
BROWSER = "chrome"  # chrome, firefox, edge
HEADLESS = True    # True để chạy không hiển thị browser
WINDOW_SIZE = "1920,1080"

# Screenshot settings
SCREENSHOT_ON_FAILURE = True
SCREENSHOT_DIR = "reports/screenshots"

# Test execution settings
MAX_RETRIES = 2
RETRY_DELAY = 3

# Current test info
CURRENT_USER = "quynh2204"
TEST_DATE = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Create directories if not exist
os.makedirs("reports/screenshots", exist_ok=True)
os.makedirs("reports/test_results", exist_ok=True)
os.makedirs("reports/logs", exist_ok=True)