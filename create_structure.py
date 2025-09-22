#!/usr/bin/env python3
"""
Script to create project structure for ecommerce-web-automation
"""

import os
import sys


def create_structure():
    # Define the project structure
    structure = {
        'config/': [
            '__init__.py',
            'settings.py'
        ],
        'data/': [
            '__init__.py',
            'test_data.py',
            'test_data.json'
        ],
        'pages/': [
            '__init__.py',
            'base_page.py',
            'main_page.py',
            'catalog_page.py',
            'product_page.py',
            'cart_page.py',
            'auth_page.py',
            'checkout_page.py',
            'account_page.py'
        ],
        'tests/__init__.py': None,
        'tests/conftest.py': None,
        'tests/ui/__init__.py': None,
        'tests/ui/test_main_page.py': None,
        'tests/ui/test_catalog.py': None,
        'tests/ui/test_auth.py': None,
        'tests/e2e/__init__.py': None,
        'tests/e2e/test_smoke.py': None,
        'tests/e2e/test_order_flow.py': None,
        'utils/': [
            '__init__.py',
            'helpers.py',
            'locators.py'
        ],
        'logs/.gitkeep': None,
        'screenshots/.gitkeep': None,
        'allure-results/.gitkeep': None
    }

    # Create directories and files
    for path, files in structure.items():
        if files is None:  # It's a file path
            dir_name = os.path.dirname(path)
            if dir_name and not os.path.exists(dir_name):
                os.makedirs(dir_name, exist_ok=True)
                print(f"📁 Created directory: {dir_name}")

            if not os.path.exists(path):
                with open(path, 'w') as f:
                    if path.endswith('.py'):
                        f.write('\"\"\"Module description\"\"\"\n\n')
                    elif path.endswith('.gitkeep'):
                        f.write('# This file ensures directory is tracked by Git\n')
                print(f"📄 Created file: {path}")
        else:  # It's a directory with files
            if not os.path.exists(path):
                os.makedirs(path, exist_ok=True)
                print(f"📁 Created directory: {path}")

            for file in files:
                file_path = os.path.join(path, file)
                if not os.path.exists(file_path):
                    with open(file_path, 'w') as f:
                        if file.endswith('.py'):
                            f.write('\"\"\"Module description\"\"\"\n\n')
                        elif file.endswith('.json'):
                            f.write('{\n    "test_data": "example"\n}\n')
                print(f"📄 Created file: {file_path}")

    # Create basic content for key files
    create_config_files()
    create_test_files()

    print("\n✅ Project structure created successfully!")
    print("🎯 Next steps:")
    print("   1. Review the created files")
    print("   2. Start implementing Page Objects")
    print("   3. Write your first test!")


def create_config_files():
    """Create basic content for configuration files"""

    # config/settings.py
    settings_content = '''"""
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
'''

    with open('config/settings.py', 'w') as f:
        f.write(settings_content)


def create_test_files():
    """Create basic content for test files"""

    # tests/conftest.py
    conftest_content = '''"""
Pytest configuration and fixtures
"""
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions


@pytest.fixture
def browser():
    \"\"\"Fixture to initialize browser\"\"\"
    # You can parameterize this later for different browsers
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)
    yield driver
    driver.quit()


@pytest.fixture
def base_url():
    \"\"\"Fixture to provide base URL\"\"\"
    return "https://example-shop.com"
'''

    with open('tests/conftest.py', 'w') as f:
        f.write(conftest_content)


if __name__ == "__main__":
    create_structure()