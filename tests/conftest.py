"""
Pytest configuration and fixtures
"""
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions


@pytest.fixture
def browser():
    """Fixture to initialize browser"""
    # You can parameterize this later for different browsers
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)
    yield driver
    driver.quit()


@pytest.fixture
def base_url():
    """Fixture to provide base URL"""
    return "https://example-shop.com"
