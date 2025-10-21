import time
from typing import Tuple, Optional

import allure
import logging

from selenium.webdriver.common.by import By

from .base_page import BasePage
from .locators import LoginPageLocators, BasePageLocators

logger = logging.getLogger(__name__)


# TODO: добавить allure шаги
# TODO: docker
# TODO: параллельный запуск тестов

class LoginPage(BasePage):
    """Page Object for login/registration page."""

    # ===== BASIC PAGE VERIFICATIONS =====
    @allure.step("Verify login page elements")
    def should_be_login_page(self) -> None:
        """Verify that all login page elements are present."""
        self.should_be_login_url()
        self.should_be_login_form()
        self.should_be_register_form()
        logger.info("Login page validation passed")

    @allure.step("Verify login URL")
    def should_be_login_url(self) -> None:
        """Verify that current URL contains 'login'."""
        self.assert_url_contains("/login")
        logger.debug("Login URL validation passed")

    @allure.step("Verify login form presence")
    def should_be_login_form(self) -> None:
        """Verify that login form is present."""
        # No waiting - implicit wait already works
        assert self.is_element_present(LoginPageLocators.LOGIN_FORM), \
            "Login form is not present on the page"
        logger.debug("Login form validation passed")

    @allure.step("Verify registration form presence")
    def should_be_register_form(self) -> None:
        """Verify that registration form is present."""
        # No waiting - implicit wait already works
        assert self.is_element_present(LoginPageLocators.REGISTER_FORM), \
            "Registration form is not present on the page"
        logger.debug("Registration form validation passed")

    # ===== ELEMENT ACCESSIBILITY VERIFICATIONS =====
    @allure.step("Verify login email field accessibility")
    def should_have_accessible_login_email_field(self) -> None:
        """Verify that login email field is present and clickable."""
        self.should_be_element_accessible(LoginPageLocators.LOGIN_EMAIL_FIELD, "Login email field")
        logger.debug("Login email field is accessible")

    @allure.step("Verify login password field accessibility")
    def should_have_accessible_login_password_field(self) -> None:
        """Verify that login password field is present and clickable."""
        self.should_be_element_accessible(LoginPageLocators.LOGIN_PASSWORD_FIELD, "Login password field")
        logger.debug("Login password field is accessible")

    @allure.step("Verify registration email field accessibility")
    def should_have_accessible_registration_email_field(self) -> None:
        """Verify that registration email field is present and clickable."""
        self.should_be_element_accessible(LoginPageLocators.REGISTER_EMAIL_FIELD, "Registration email field")
        logger.debug("Registration email field is accessible")


    @allure.step("Verify registration password field accessibility")
    def should_have_accessible_registration_password_field(self) -> None:
        """Verify that registration password field is present and clickable."""
        self.should_be_element_accessible(LoginPageLocators.REGISTER_PASSWORD_FIELD, "Registration password field")
        logger.debug("Registration password field is accessible")

    @allure.step("Verify registration confirm password field accessibility")
    def should_have_accessible_registration_confirm_password_field(self) -> None:
        """Verify that registration confirm password field is present and clickable."""
        self.should_be_element_accessible(LoginPageLocators.REGISTER_CONFIRM_PASSWORD_FIELD, "Registration confirm password field")
        logger.debug("Registration confirm password field is accessible")

    @allure.step("Verify login submit button is accessible")
    def should_have_accessible_login_submit_button(self) -> None:
        """Verify that login submit button is present and clickable."""
        self.should_be_element_accessible(LoginPageLocators.LOGIN_SUBMIT_BUTTON, "Login submit button")
        logger.debug("Login submit button is accessible")

    @allure.step("Verify registration submit button is accessible")
    def should_have_accessible_registration_submit_button(self) -> None:
        """Verify that registration submit button is present and clickable."""
        self.should_be_element_accessible(LoginPageLocators.REGISTER_SUBMIT_BUTTON, "Registration submit button")
        logger.debug("Registration submit button is accessible")


    # ===== USER ACTIONS =====

    @allure.step("Verify user is logged in")
    def should_be_logged_in(self) -> None:
        """Verify that user is successfully logged in."""
        assert self.is_element_present(BasePageLocators.USER_ICON), "User icon not found - login failed"
        logger.info("Login successful")

    @allure.step("Verify successful registration")
    def should_be_successful_login(self) -> None:
        """Verify login success using language-agnostic checks."""
        # 1. Check success notification (language-agnostic)
        with allure.step("Check login success notification"):
            assert self.is_element_present(LoginPageLocators.LOGIN_SUCCESS), \
                "Success notification not found"

        # 2. Check user icon presence
        with allure.step("Check user icon presence after login"):
            assert self.is_element_present(BasePageLocators.USER_ICON), \
                "User not logged in after login"

        # 3. Check absence of error messages
        with allure.step("Check absence of error messages after login"):
            assert self.is_not_element_present(BasePageLocators.ERROR_ALERT), \
                "Error message present after login"

        # 4. check we are not on login page anymore
        with allure.step("Check URL after login"):
            current_url = self.get_current_url().lower()
            assert "login" not in current_url, "Still on login page"

        logger.info("Login successful")

    @allure.step("Verify successful registration")
    def should_be_successful_registration(self) -> None:
        """Verify registration success using language-agnostic checks."""

        # 2. Check success notification (language-agnostic)
        with allure.step("Check registration success notification"):
            assert self.is_element_present(LoginPageLocators.REGISTRATION_SUCCESS), \
                "Success notification not found"

        # 3. Check user icon presence
        with allure.step("Check user icon presence after registration"):
            assert self.is_element_present(BasePageLocators.USER_ICON), \
                "User not logged in after registration"

        # 4. Check absence of error messages
        with allure.step("Check absence of error messages after registration"):
            assert self.is_not_element_present(BasePageLocators.ERROR_ALERT), \
                "Error message present after registration"

        # 1. check we are not on login page anymore
        with allure.step("Check URL after registration"):
            current_url = self.get_current_url().lower()
            assert "login" not in current_url, "Still on registration page"

        logger.info("Registration successful")

    @allure.step("Register new user")
    def register_new_user(self, email: str, password: str) -> None:
        """Register a new user - only performs the action."""
        # Fill the registration form
        with allure.step("Fill registration form"):
            self.send_keys(LoginPageLocators.REGISTER_EMAIL_FIELD, email)
        with allure.step("Fill first password field"):
            self.send_keys(LoginPageLocators.REGISTER_PASSWORD_FIELD, password)
        with allure.step("Fill confirm password field"):
            self.send_keys(LoginPageLocators.REGISTER_CONFIRM_PASSWORD_FIELD, password)

        # Submit registration
        with allure.step("Submit registration form"):
            self.click(LoginPageLocators.REGISTER_SUBMIT_BUTTON)

        logger.info(f"Attempted to register user: {email}")

    @allure.step("Login user")
    def login_user(self, email: str, password: str) -> None:
        """Login user - only performs the action."""
        # Fill the login form
        with allure.step("Fill email in login form"):
            self.send_keys(LoginPageLocators.LOGIN_EMAIL_FIELD, email)
        with allure.step("Fill password in login form"):
            self.send_keys(LoginPageLocators.LOGIN_PASSWORD_FIELD, password)

        # Submit login
        with allure.step("Submit login form"):
            self.click(LoginPageLocators.LOGIN_SUBMIT_BUTTON)

        logger.info(f"Attempted to login user: {email}")

    @allure.step("Navigate to login page")
    def go_to_login_page(self) -> None:
        """Navigate to login page using BasePage methods."""
        self.click(BasePageLocators.LOGIN_LINK)
        success = self._wait_for_url_contains("/login")
        assert success, "Failed to navigate to login page"
        logger.info("Navigated to login page")

    @allure.step("Generate unique email for testing")
    def _generate_unique_email(self) -> str:
        """Generate unique email for testing."""
        return f"test_{time.time()}@example.com"
