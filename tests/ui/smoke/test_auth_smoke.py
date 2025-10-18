import pytest
import logging
from pages.login_page import LoginPage
import random

# pytest tests/test_auth_smoke.py -v

logger = logging.getLogger(__name__)
@pytest.mark.smoke
class TestAuthSmoke:

    """Smoke tests for authentication - login and registration."""
    @pytest.mark.login
    def test_login_with_valid_user(self, browser, login_url, valid_user):
        """Test login functionality with valid credentials."""
        login_page = LoginPage(browser, login_url)
        login_page.open()

        login_page.login_user(valid_user["email"], valid_user["password"])
        login_page.should_be_logged_in()
        logger.info("✓ User logged in successfully")

    @pytest.mark.registration
    def test_new_user_registration(self, browser, login_url):
        """Test new user registration functionality."""
        login_page = LoginPage(browser, login_url)
        login_page.open()

        unique_email = f"testuser{random.randint(1000, 9999)}@example.com"

        login_page.register_new_user(unique_email, "TestPassword123")
        login_page.should_be_successful_registration()
        logger.info("✓ New user registered successfully")