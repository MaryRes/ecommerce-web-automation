"""
Pytest configuration with settings integration
"""

import pytest
import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
import time

# Import project settings
from config import settings

# Setup logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format=settings.LOG_FORMAT
)
logger = logging.getLogger(__name__)

def pytest_addoption(parser):
    """Add command line options for test configuration"""
    parser.addoption(
        '--browser',
        action='store',
        default=settings.DEFAULT_BROWSER,
        help='Browser to use: chrome or firefox'
    )
    parser.addoption(
        '--headless',
        action='store_true',
        default=settings.DEFAULT_HEADLESS,
        help='Run browser in headless mode'
    )
    parser.addoption(
        '--language',
        action='store',
        default=settings.DEFAULT_LANGUAGE,
        help='Browser language: en, ru, es, etc.'
    )

@pytest.fixture(scope="function")
def browser(request):
    """Main browser fixture using settings"""

    browser_name = request.config.getoption("--browser")
    headless = request.config.getoption("--headless")
    language = request.config.getoption("--language")

    logger.info(f"Starting {browser_name} browser (headless: {headless}, language: {language})")

    if browser_name == "chrome":
        options = ChromeOptions()
        options.add_experimental_option('prefs', {'intl.accept_languages': language})

        if headless:
            options.add_argument('--headless=new')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')

        options.add_argument(f'--window-size={settings.WINDOW_WIDTH},{settings.WINDOW_HEIGHT}')

        driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()),
            options=options
        )

    elif browser_name == "firefox":
        options = FirefoxOptions()
        options.set_preference('intl.accept_languages', language)

        if headless:
            options.add_argument('--headless')

        driver = webdriver.Firefox(
            service=FirefoxService(GeckoDriverManager().install()),
            options=options
        )

    else:
        raise pytest.UsageError("--browser must be 'chrome' or 'firefox'")

    # Apply settings
    driver.implicitly_wait(settings.IMPLICIT_WAIT)
    driver.set_page_load_timeout(settings.PAGE_LOAD_TIMEOUT)

    yield driver

    logger.info("Closing browser")
    driver.quit()

# URL fixtures using our settings
@pytest.fixture
def base_url():
    return settings.BASE_URL

@pytest.fixture
def login_url():
    return settings.LOGIN_URL

@pytest.fixture
def catalog_url():
    return settings.CATALOG_URL

@pytest.fixture
def basket_url():
    return settings.BASKET_URL

# Test data fixtures
@pytest.fixture
def valid_user():
    return settings.VALID_USER

@pytest.fixture
def invalid_user():
    return settings.INVALID_USER

# Timer fixture using settings
@pytest.fixture(autouse=True)
def test_timer(request):

    start_time = time.time()
    yield
    duration = time.time() - start_time
    if duration > settings.SLOW_TEST_THRESHOLD:
        logger.warning(f"⏱ Slow test '{request.node.name}' took {duration:.2f}s")