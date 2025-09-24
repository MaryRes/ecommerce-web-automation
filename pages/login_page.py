from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support import expected_conditions as EC
import logging
from typing import Tuple
from selenium.webdriver.common.by import By
from .base_page import BasePage
from .locators import LoginPageLocators, BasePageLocators

# Setup logger
logger = logging.getLogger(__name__)

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
        current_url = self.browser.current_url
        assert "login" in current_url.lower(), f"Login URL not correct. Current: {current_url}"
        logger.debug("Login URL validation passed")

    def should_be_login_form(self) -> None:
        """Verify that login form is present."""
        try:
            is_present = self.wait_for_element_present(LoginPageLocators.LOGIN_FORM)
            assert is_present, "Login form is not present on the page"
            logger.debug("Login form validation passed")

        except Exception as e:
            logger.error(f"Error checking login form: {e}")
            raise AssertionError(f"Login form validation failed: {e}")

    def should_be_register_form(self) -> None:
        """Verify that registration form is present."""
        try:
            is_present = self.wait_for_element_present(LoginPageLocators.REGISTER_FORM)
            assert is_present, "Registration form is not present on the page"
            logger.debug("Registration form validation passed")

        except Exception as e:
            logger.error(f"Error checking registration form: {e}")
            raise AssertionError(f"Registration form validation failed: {e}")
    def register_new_user(self, email: str, password: str) -> None:
        """Register a new user with given credentials."""
        try:
            # Find registration form elements (adjust selectors based on actual form)
            email_field = self.wait.until(
                EC.element_to_be_clickable(LoginPageLocators.REGISTER_EMAIL_FIELD)
            )
            password_field = self.browser.find_element(*LoginPageLocators.REGISTER_PASSWORD_FIELD)
            confirm_password_field = self.browser.find_element(*LoginPageLocators.REGISTER_CONFIRM_PASSWORD_FIELD)
            submit_button = self.browser.find_element(*LoginPageLocators.REGISTER_SUBMIT_BUTTON)

            # Fill registration form
            email_field.clear()
            email_field.send_keys(email)

            password_field.clear()
            password_field.send_keys(password)

            confirm_password_field.clear()
            confirm_password_field.send_keys(password)

            # Submit registration
            submit_button.click()
            logger.info(f"Registered new user: {email}")

        except Exception as e:
            logger.error(f"Error during user registration: {e}")
            raise

    def login_user(self, email: str, password: str) -> None:
        """Login with existing user credentials."""
        try:
            # Find login form elements (adjust selectors based on actual form)
            email_field = self.wait.until(
                EC.element_to_be_clickable(LoginPageLocators.LOGIN_EMAIL_FIELD)
            )
            password_field = self.browser.find_element(*LoginPageLocators.LOGIN_PASSWORD_FIELD)
            login_button = self.browser.find_element(*LoginPageLocators.LOGIN_SUBMIT_BUTTON)

            # Fill login form
            email_field.clear()
            email_field.send_keys(email)

            password_field.clear()
            password_field.send_keys(password)

            # Submit login
            login_button.click()
            logger.info(f"User logged in: {email}")

        except Exception as e:
            logger.error(f"Error during user login: {e}")
            raise

    def should_be_successful_login(self) -> None:
        """Verify that login was successful."""
        # Check for success indicators (adjust based on actual site behavior)
        try:
            # Example: check if user is redirected away from login page
            assert "login" not in self.browser.current_url.lower(), "Still on login page after login"

            # Or check for user menu/logout button
            # assert self.is_element_present(*MainPageLocators.USER_MENU), "User menu not found after login"

            logger.info("Login successful")

        except Exception as e:
            logger.error(f"Login verification failed: {e}")
            raise

    def should_be_successful_registration(self) -> None:
        """Verify that registration was successful."""
        try:
            # Check for success message or redirect
            # assert "registration complete" in self.browser.page_source.lower()
            assert "login" in self.browser.current_url.lower(), "Not redirected after registration"
            logger.info("Registration successful")

        except Exception as e:
            logger.error(f"Registration verification failed: {e}")
            raise

    def go_to_login_page(self) -> None:
        """Override base method for login page-specific behavior."""
        try:
            # Use the improved click method from base page
            self.click_element(BasePageLocators.LOGIN_LINK)
            self.wait.until(EC.url_contains("login"))
            logger.debug("Navigated to login page")

        except Exception as e:
            logger.error(f"Error navigating to login page: {e}")
            raise
