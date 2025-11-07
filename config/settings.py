"""
Configuration settings for ecommerce automation project
"""

# ==================== URL CONFIGURATION ====================
BASE_URL = "http://selenium1py.pythonanywhere.com"

# Page URLs
LOGIN_URL = f"{BASE_URL}/accounts/login/"
CATALOG_URL = f"{BASE_URL}/catalogue/"
BASKET_URL = f"{BASE_URL}/basket/"
REGISTER_URL = f"{BASE_URL}/accounts/register/"
MAIN_PAGE_URL = BASE_URL + "/"

# Product URLs for specific tests
PRODUCT_URLS = {
    "shellcoders_handbook": f"{BASE_URL}/catalogue/the-shellcoders-handbook_209/",
    "city_and_stars": f"{BASE_URL}/catalogue/the-city-and-the-stars_95/",
    "hacking_exposed": f"{BASE_URL}/catalogue/hacking-exposed-wireless_208/",
    "coders_at_work": f"{BASE_URL}/catalogue/coders-at-work_207/"
}

# ==================== TEST USERS ====================
# Valid test user for login tests
VALID_USER = {
    "email": "testuser100@ex.com",
    "password": "testpassword123"
}

# Invalid user for negative tests
INVALID_USER = {
    "email": "invalid@example.com",
    "password": "wrongpassword"
}

# New user for registration test
NEW_USER = {
    "email": "newuser420958@example.com",
    "password": "newpassword123",
    "confirm_password": "newpassword123"
}

# Empty credentials
EMPTY_USER = {
    "email": "",
    "password": ""
}

# ==================== TIMEOUT CONFIGURATION ====================
IMPLICIT_WAIT = 10           # Default implicit wait for elements
PAGE_LOAD_TIMEOUT = 30       # Maximum page load time
ELEMENT_TIMEOUT = 10         # Explicit wait timeout for elements
POLL_FREQUENCY = 0.5         # How often to check for elements

# ==================== BROWSER CONFIGURATION ====================
DEFAULT_BROWSER = "chrome"
DEFAULT_HEADLESS = True      # Headless by default for CI
DEFAULT_LANGUAGE = "en"      # Default browser language

# Browser window size
WINDOW_WIDTH = 1920
WINDOW_HEIGHT = 1080

# ==================== TEST DATA ====================
# Product data for tests
PRODUCTS = {
    "shellcoders_handbook": {
        "title": "The shellcoder's handbook",
        "price": "£9.99",
        "stock": True
    },
    "city_and_stars": {
        "title": "The City and the Stars",
        "price": "£10.99",
        "stock": True
    }
}

# Promo codes (based on bugs you found!)
PROMO_CODES = {
    "valid": "OFFER20",
    "invalid": "INVALIDCODE",
    "expired": "EXPIRED2023"
}

# ==================== PATHS & DIRECTORIES ====================
SCREENSHOTS_DIR = "screenshots"
LOGS_DIR = "logs"
ALLURE_RESULTS_DIR = "allure-results"


# Test data paths
TEST_DATA_PATH = "data/data_manager.json"

# ==================== TEST CONFIGURATION ====================
# Slow test threshold in seconds
SLOW_TEST_THRESHOLD = 5.0

# Retry configuration for flaky tests
RETRY_COUNT = 2
RETRY_DELAY = 1

# ==================== LOGGING CONFIGURATION ====================
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"


