"""
Định nghĩa các selectors cho elements
Organized by page and functionality
"""

class ProductPageLocators:
    """Locators cho trang sản phẩm"""
    
    # Button "Thêm vào giỏ hàng" - Updated với selectors thực tế
    ADD_TO_CART_BUTTON = [
        "button.styles_add_to_cart__LTr7C",
        "button[data-pdid='16'].add_to_cart",
        ".add_to_cart.styles_add_to_cart__LTr7C",
        "//button[contains(@class, 'styles_add_to_cart__LTr7C')]",
        "//button[contains(text(), 'Thêm vào giỏ')]",
        "//button[contains(@class, 'add_to_cart')]"
    ]
    
    # Quantity input field - Updated với selectors thực tế
    QUANTITY_INPUT = [
        "input.styles_qty_pd_input__dFgvy",
        ".qty_pd_box input.text-center",
        "input[type='text'].styles_qty_pd_input__dFgvy",
        "//input[@class='text-center styles_qty_pd_input__dFgvy']",
        ".styles_qty_pd__IF7fO input[type='text']"
    ]
    
    # Button tăng/giảm quantity
    QUANTITY_DECREASE_BUTTON = [
        ".styles_qty_pd__IF7fO button:first-child",
        ".qty_pd_box button:first-of-type",
        "//div[contains(@class, 'styles_qty_pd__IF7fO')]//button[text()='-']"
    ]
    
    QUANTITY_INCREASE_BUTTON = [
        ".styles_qty_pd__IF7fO button:last-child",
        ".qty_pd_box button:last-of-type", 
        "//div[contains(@class, 'styles_qty_pd__IF7fO')]//button[text()='+']"
    ]
    
    # Button "Đăng ký ngay"
    BUY_NOW_BUTTON = [
        "button.styles_buy_now__DEI8S",
        "button[data-pdid='16'].buy_now",
        ".buy_now.styles_buy_now__DEI8S",
        "//button[contains(@class, 'styles_buy_now__DEI8S')]",
        "//button[contains(text(), 'Đăng ký ngay')]"
    ]
    
    # Category/Classification selection - Updated for actual HTML structure with radio buttons
    CATEGORY_SELECTION = [
        # Main container for category selection
        ".pd-attr-box[id='pd_attr_0']",
        "div.pd-attr-box",
        
        # Radio button inputs
        "input[name='attr_0'][type='radio']",
        "input.pd_attr[data-type='0']",
        
        # Clickable labels for each option
        "label.attr_order",
        
        # Specific category options
        "input[value='35'][name='attr_0']",  # Cao học UEH/ VB2 UEH
        "input[value='38'][name='attr_0']",  # Học viên cũ tại ATD
        "input[value='39'][name='attr_0']",  # SV trường khác UEH
        "input[value='40'][name='attr_0']",  # SV UEH
        "input[value='42'][name='attr_0']",  # Khác
        
        # XPath selectors for radio options
        "//input[@type='radio' and @name='attr_0']",
        "//label[@class='attr_order']",
        "//div[@class='pd-attr-box']//input[@type='radio']",
        
        # Fallback selectors
        "[data-type='0']",
        ".choose",
        "span.choose"
    ]
    
    # Specific category option labels (for clicking)
    CATEGORY_LABELS = {
        "cao_hoc_ueh": "label[tooltip='Cao học UEH/ VB2 UEH']",
        "hoc_vien_cu": "label[tooltip='Học viên cũ tại ATD']", 
        "sv_truong_khac": "label[tooltip='SV trường khác UEH']",
        "sv_ueh": "label[tooltip='SV UEH']",
        "khac": "label[tooltip='Khác']"
    }
    
    # Old category dropdown selectors (kept for backward compatibility)
    CATEGORY_DROPDOWN = [
        "select[name*='category']",
        "select[name*='classification']",
        ".category-select",
        ".classification-select",
        "#category-select",
        "select",
        ".form-select",
        ".dropdown-toggle"
    ]
    
    # Error messages
    ERROR_MESSAGE = [
        ".error-message",
        ".alert-danger",
        ".alert-error",
        ".validation-error",
        ".notice-error",
        "[class*='error']",
        ".message-error",
        ".invalid-feedback",
        ".text-danger",
        ".warning",
        "div[role='alert']"
    ]
    
    # Success messages
    SUCCESS_MESSAGE = [
        ".success-message",
        ".alert-success",
        ".notice-success",
        "[class*='success']",
        ".text-success",
        "div[class*='success']"
    ]
    
    # Container chứa form quantity
    QUANTITY_CONTAINER = [
        ".styles_qty_pd_box__JONgL",
        "div[class*='qty_pd_box']"
    ]