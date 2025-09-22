"""
Configuration settings for ecommerce automation project
"""

# Base URLs
BASE_URL = "https://example-shop.com"
ADMIN_URL = f"{BASE_URL}/admin"

# Browser settings
BROWSER = "chrome"
HEADLESS = False
IMPLICIT_WAIT = 10
PAGE_LOAD_TIMEOUT = 30

# Test data paths
TEST_DATA_PATH = "data/test_data.json"

# Reporting
ALLURE_RESULTS_DIR = "allure-results"
SCREENSHOTS_DIR = "screenshots"
LOGS_DIR = "logs"
