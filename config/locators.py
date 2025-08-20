"""
Định nghĩa các selectors cho elements
Organized by page and functionality
"""

class ProductPageLocators:
    """Locators cho trang sản phẩm"""
    
    # Button "Thêm vào giỏ hàng"
    ADD_TO_CART_BUTTON = [
        "//button[contains(text(), 'Thêm vào giỏ hàng')]",
        "//button[contains(text(), 'Add to cart')]",
        "//input[@value='Thêm vào giỏ hàng']",
        ".add-to-cart",
        ".btn-add-cart",
        "#add-to-cart-button",
        ".add-cart-btn"
    ]
    
    # Quantity input field
    QUANTITY_INPUT = [
        "input[name='quantity']",
        "input[id='quantity']",
        ".quantity-input",
        "input[type='number']",
        ".qty-input"
    ]
    
    # Category/Classification dropdown
    CATEGORY_DROPDOWN = [
        "select[name*='category']",
        "select[name*='classification']",
        ".category-select",
        ".classification-select",
        "#category-select"
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
        ".invalid-feedback"
    ]
    
    # Success messages
    SUCCESS_MESSAGE = [
        ".success-message",
        ".alert-success",
        ".notice-success",
        "[class*='success']"
    ]