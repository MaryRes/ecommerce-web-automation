import pytest
import logging
import allure
from selenium.webdriver.common.by import By

from pages.login_page import LoginPage

logger = logging.getLogger(__name__)

# pytest tests/test_login_smoke.py -v
# pytest -v -s --log-cli-level=INFO --tb=short tests/ui/smoke/test_login_smoke.py
# pytest --alluredir=allure-results
# allure serve allure-results
@pytest.mark.smoke
@allure.epic("Authentication")
@allure.feature("Login Page Smoke Tests")
@pytest.mark.ui
@pytest.mark.smoke
class TestLoginPageSmoke:
    """Smoke tests for login page - basic functionality check."""

    @allure.title("Test Login Page Opens")
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.description("""Verify that the login page:
                        - Can be opened successfully"
                        - contains all necessary elements
                        """)
    def test_login_page_fully_functional(self, browser, login_url):
        """Test that login page opens with all required elements."""

        login_page = LoginPage(browser, login_url)
        with allure.step("Open login page"):
            logger.info("Testing login page opening...")
            login_page.open()

        with allure.step("Verify base functionality of login page"):
            login_page.should_be_login_page()
            logger.info("✓ Login page opens correctly")

