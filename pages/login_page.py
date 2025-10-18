import time

from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support import expected_conditions as EC
import logging
from typing import Tuple
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from .base_page import BasePage
from .locators import LoginPageLocators, BasePageLocators

logger = logging.getLogger(__name__)


# TODO: переписать функции с использованием функций из base_page особенно ВНИМАНИЕ НА ОЖИДАНИЯ!!!
# TODO: сделать коммит и пуш
# TODO: убрать избыточные проверки и ожидания
# TODO: добавить типизацию
# TODO: добавить allure шаги
# TODO: docker
# TODO: параллельный запуск тестов

class LoginPage(BasePage):
    """Page Object for login/registration page."""

    def should_be_login_page(self) -> None:
        """Verify that all login page elements are present."""
        self.should_be_login_url()
        self.should_be_login_form()
        self.should_be_register_form()
        logger.info("Login page validation passed")

    def should_be_login_url(self) -> None:
        """Verify that current URL contains 'login'."""
        self.assert_url_contains("/login")
        logger.debug("Login URL validation passed")

    def should_be_login_form(self) -> None:
        """Verify that login form is present."""
        # No waiting - implicit wait already works
        assert self.is_element_present(*LoginPageLocators.LOGIN_FORM), \
            "Login form is not present on the page"
        logger.debug("Login form validation passed")

    def should_be_register_form(self) -> None:
        """Verify that registration form is present."""
        # No waiting - implicit wait already works
        assert self.is_element_present(*LoginPageLocators.REGISTER_FORM), \
            "Registration form is not present on the page"
        logger.debug("Registration form validation passed")

    def should_be_logged_in(self) -> None:
        """Verify that user is successfully logged in."""
        assert self.is_element_present(BasePageLocators.USER_ICON), "User icon not found - login failed"
        logger.info("Login successful")

    def should_be_successful_registration(self) -> None:
        """Verify registration success using language-agnostic checks."""
        # 1. check we are not on login page anymore
        current_url = self.get_current_url().lower()
        assert "login" not in current_url, "Still on registration page"

        # 2. Check success notification (language-agnostic)
        assert self.is_element_present(LoginPageLocators.REGISTRATION_SUCCESS), \
            "Success notification not found"

        # 3. Check user icon presence
        assert self.is_element_present(BasePageLocators.USER_ICON), \
            "User not logged in after registration"

        # 4. Check absence of error messages
        assert self.is_not_element_present(BasePageLocators.ERROR_ALERT), \
            "Error message present after registration"

        logger.info("Registration successful")

    def register_new_user(self, email: str, password: str) -> None:
        """Register a new user - only performs the action."""
        # Fill the registration form
        self.send_keys(LoginPageLocators.REGISTER_EMAIL_FIELD, email)
        self.send_keys(LoginPageLocators.REGISTER_PASSWORD_FIELD, password)
        self.send_keys(LoginPageLocators.REGISTER_CONFIRM_PASSWORD_FIELD, password)

        # Submit registration
        self.click(LoginPageLocators.REGISTER_SUBMIT_BUTTON)

        logger.info(f"Attempted to register user: {email}")

    def login_user(self, email: str, password: str) -> None:
        """Login user - only performs the action."""
        # Fill the login form
        self.send_keys(LoginPageLocators.LOGIN_EMAIL_FIELD, email)
        self.send_keys(LoginPageLocators.LOGIN_PASSWORD_FIELD, password)

        # Submit login
        self.click(LoginPageLocators.LOGIN_SUBMIT_BUTTON)

        logger.info(f"Attempted to login user: {email}")



    def go_to_login_page(self) -> None:
        """Navigate to login page using BasePage methods."""
        self.click(BasePageLocators.LOGIN_LINK)
        success = self.wait_for_url_contains("/login")
        assert success, "Failed to navigate to login page"
        logger.info("Navigated to login page")

    def _generate_unique_email(self) -> str:
        """Generate unique email for testing."""
        return f"test_{time.time()}@example.com"