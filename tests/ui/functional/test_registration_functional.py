import logging
import time

import pytest
import allure
from pages.login_page import LoginPage
from data.data_manager import data_manager
# python -m pytest tests/ui/functional/test_registration_functional.py::TestRegistrationFunctional::test_successful_new_user_registration -v
# docker run --rm -v ${PWD}:/app qa-tests python -m pytest tests

@pytest.mark.functional
@allure.epic("Authentication")
@allure.feature("Registration Functional Tests")
class TestRegistrationFunctional:
    """Functional tests for user registration scenarios."""

    @allure.title("Successful new user registration")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("positive", "registration")
    def test_successful_new_user_registration(self, browser, login_url):
        """Verify new user can register successfully."""
        login_page = LoginPage(browser, login_url)

        with allure.step("Open registration page"):
            login_page.open()

        with allure.step("Generate unique email for registration"):
            email = data_manager.generate_unique_email()

        with allure.step("Generate strong password for registration"):
            password = data_manager.strong_passwords[0]  # Use first strong password

        with allure.step("Fill and submit registration form with valid data"):
            login_page.register_new_user(email, password)

        with allure.step("Verify registration success"):
            # Implement registration success verification
            login_page.should_be_successful_registration()

    @allure.title("Registration with weak password")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("negative", "validation")
    @pytest.mark.parametrize("weak_password", data_manager.weak_passwords[:2])  # Test first 2 cases
    def test_registration_with_weak_password(self, browser, login_url, weak_password):
        """Verify system enforces password strength requirements."""
        login_page = LoginPage(browser, login_url)
        logging.info("Testing registration with weak password...")

        with allure.step("Open registration page"):
            login_page.open()
            logging.info("Opened registration page for weak password test")

        with allure.step("Attempt registration with weak password"):
            email = data_manager.generate_unique_email()
            weak_password = data_manager.weak_passwords[0]

            login_page.register_new_user(email, weak_password)
            logging.info(f"Attempted registration with weak password: {weak_password}")

        with allure.step("Verify password strength error is shown"):
            login_page.should_be_password_problem_message()
            logging.info("✓ Weak password error message displayed")

        with allure.step("Verify registration error message is shown"):
            login_page.should_be_registration_error_message()
            logging.info("✓ Registration error message displayed")

        with allure.step("Verify user NOT registered"):
            login_page.should_not_be_logged_in()
            login_page.should_be_login_page()
            logging.info("✓ User not registered with weak password")

    @allure.title("Password mismatch validation - {scenario}")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("validation", "negative")
    @pytest.mark.parametrize("password_1, password_2, scenario", [
        # Different types of mismatches to cover edge cases
        ("StrongPass123", "DifferentPass123", "completely_different"),
        ("StrongPass123", "StrongPass123X", "suffix_difference"),
        ("StrongPass123", "XStrongPass123", "prefix_difference"),
        ("StrongPass123", "StrongPass124", "last_char_different")
    ])
    def test_registration_with_password_mismatch(self, browser, login_url, password_1, password_2, scenario):
        """Verify system validates password confirmation."""

        with allure.step(f"Setup login page for password mismatch test scenario: {scenario}"):
            login_page = LoginPage(browser, login_url)
            logging.info("Testing registration with password mismatch...")

        with allure.step("Open registration page"):
            login_page.open()
            logging.info("Opened registration page for password mismatch test")

        with allure.step("Attempt registration with mismatched passwords"):
            email = data_manager.generate_unique_email()
            password_1 = data_manager.strong_passwords[0]
            password_2 = "X" + password_1  # Different password
            logging.info(f"Attempting registration with passwords: '{password_1}' and '{password_2}'")

            login_page.register_new_user(email, password_1, password_2)
            logging.info("Submitted registration form with mismatched passwords")

        with allure.step("Verify password mismatch error is shown"):
            # Implement password confirmation validation
            login_page.should_be_password_problem_message()
            logging.info("✓ Password mismatch error message displayed")

        with allure.step("Verify password confirmation error is shown"):
            login_page.should_be_registration_error_message()
            logging.info("✓ Password confirmation error message displayed")

        with allure.step("Verify user NOT registered"):
            login_page.should_not_be_logged_in()
            login_page.should_be_login_page()
            logging.info("✓ User not registered due to password mismatch")

    @allure.title("Password space trimming bug - {password_1} vs '{password_2}'")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("bug", "validation")
    @pytest.mark.xfail(reason="KNOWN BUG: Password spaces are trimmed, making different passwords appear identical")
    @pytest.mark.parametrize("password_1, password_2", [
        ("StrongPass123", " StrongPass123"),  # space in beginning
        ("StrongPass123", "StrongPass123 "),  # space at end
        ("StrongPass123", " StrongPass123 "),  # spaces at both ends
    ])
    def test_password_space_trimming(self, browser, login_url, password_1, password_2):
        """Verify system treats passwords with leading/trailing spaces as different.

        This test is expected to fail due to a known bug where spaces are trimmed.
        """

        with allure.step(f"Setup login page for password space trimming test with '{password_1}' vs '{password_2}'"):
            login_page = LoginPage(browser, login_url)
            logging.info("Testing registration with password space trimming...")

        with allure.step("Open registration page"):
            login_page.open()
            logging.info("Opened registration page for password space trimming test")

        with allure.step("Attempt registration with passwords differing by spaces"):
            email = data_manager.generate_unique_email()
            logging.info(f"Attempting registration with passwords: '{password_1}' and '{password_2}'")

            login_page.register_new_user(email, password_1, password_2)
            logging.info("Submitted registration form with space-different passwords")

        with allure.step("Verify password mismatch error is shown"):
            # Implement password confirmation validation
            login_page.should_be_password_problem_message()
            logging.info("✓ Password mismatch error message displayed")

        with allure.step("Verify password confirmation error is shown"):
            login_page.should_be_registration_error_message()
            logging.info("✓ Password confirmation error message displayed")

        with allure.step("Verify user NOT registered"):
            login_page.should_not_be_logged_in()
            login_page.should_be_login_page()
            logging.info("✓ User not registered due to password space trimming issue")

    @allure.title("Registration with existing email")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("negative", "validation")
    def test_registration_with_existing_email(self, browser, login_url):
        """Verify system prevents duplicate email registration."""
        login_page = LoginPage(browser, login_url)

        with allure.step("Open registration page"):
            login_page.open()

        with allure.step("Attempt registration with existing email"):
            email = data_manager.valid_user["email"]
            password = data_manager.strong_passwords[0]
            login_page.register_new_user(email, password)

        with allure.step("Verify duplicate email error is shown"):
            login_page.should_be_registration_error_message()

        with allure.step("Verify user NOT registered"):
            login_page.should_not_be_logged_in()
            login_page.should_be_login_page()

    @allure.title("Security: XSS attempt in registration (email field)")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("security", "negative")
    def test_registration_with_xss_attempt_email(self, browser, login_url):
        """Verify system is protected against XSS attacks."""
        login_page = LoginPage(browser, login_url)

        with allure.step("Open registration page"):
            login_page.open()

        with allure.step("Attempt XSS injection in registration fields"):
            xss_payload = data_manager.xss_attempt
            login_page.register_new_user(xss_payload, xss_payload)

        with allure.step("Verify system sanitizes input safely"):
            login_page.should_be_invalid_email_message()

        with allure.step("Verify user NOT registered"):
            login_page.should_not_be_logged_in()
            login_page.should_be_login_page()


    @allure.title("Security: XSS attempt in registration (password field)")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("security", "negative")
    def test_registration_with_xss_attempt_password(self, browser, login_url):
        """Verify system is protected against XSS attacks."""
        login_page = LoginPage(browser, login_url)

        with allure.step("Open registration page"):
            login_page.open()

        with allure.step("Attempt XSS injection in registration fields"):
            xss_payload = data_manager.xss_attempt
            email = data_manager.generate_unique_email()
            login_page.register_new_user(email, xss_payload)

        with allure.step("Verify system sanitizes input safely"):
            login_page.should_be_successful_registration()
