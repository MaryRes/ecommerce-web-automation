import pytest
import logging
from pages.login_page import LoginPage

# pytest tests/test_auth_smoke.py -v

logger = logging.getLogger(__name__)

class TestAuthSmoke:

    """Smoke tests for authentication - login and registration."""
    @pytest.mark.login
    def test_login_with_valid_user(self, browser, login_url, valid_user):
        """Test login functionality with valid credentials."""
        login_page = LoginPage(browser, login_url)
        browser.get(login_url)

        login_page.login_user(valid_user["email"], valid_user["password"])
        login_page.should_be_successful_login()
        logger.info("✓ User logged in successfully")