import pytest
import logging
import allure
from pages.login_page import LoginPage
import random

# pytest tests/test_auth_smoke.py -v
# TODO: add allure steps

logger = logging.getLogger(__name__)


@pytest.mark.smoke
@pytest.mark.ui
@allure.epic("Authentication")
@allure.feature("Authorization smoke tests")
class TestAuthSmoke:
    """Smoke tests for authentication - login and registration."""

    @pytest.mark.login
    @allure.title("Successful login with valid credentials")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("""
    Verify that a user can log in with valid credentials
    Steps:
    1. Open login page
    2. Enter valid email and password
    3. Submit login form
    4. Verify user is logged in
    """)
    @allure.tag("smoke", "login", "ui", "authentication")
    def test_login_with_valid_user(self, browser, login_url, valid_user):
        """Test login functionality with valid credentials."""
        login_page = LoginPage(browser, login_url)

        with allure.step("Open login page"):
            login_page.open()
            logger.info("Opened login page for login test")

        with allure.step(f"Login with user: {valid_user['email']}"):
            login_page.login_user(valid_user["email"], valid_user["password"])
            logger.info(f"Attempted login for user: {valid_user['email']}")

        with allure.step("Verify user is logged in"):
            login_page.should_be_logged_in()
            logger.info("✓ User logged in successfully")

    @pytest.mark.registration
    @allure.title("Successful new user registration")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("""
    Verify that new user can successfully register in the system.
    Steps:
    1. Open login page
    2. Generate unique email
    3. Fill registration form
    4. Submit registration
    5. Verify registration success
    """)
    @allure.tag("smoke", "registration", "ui", "authentication")
    def test_new_user_registration(self, browser, login_url):
        """Test new user registration functionality."""
        login_page = LoginPage(browser, login_url)

        with allure.step("Open login page"):
            login_page.open()
            logger.info("Opened login page for registration test")

        with allure.step("Generate unique test email"):
            unique_email = f"testuser{random.randint(1000, 9999)}@example.com"
            logger.info(f"Generated unique email for registration: {unique_email}")

        with allure.step("Register new user with generated email"):
            login_page.register_new_user(unique_email, "TestPassword123")
            logger.info(f"Attempted registration for user: {unique_email}")

        with allure.step("Verify registration was successful"):
            login_page.should_be_successful_registration()
            logger.info("✓ New user registered successfully")
