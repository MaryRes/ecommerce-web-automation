"""
Functional tests for login and registration scenarios.

Tests cover:
- Positive authentication flows (valid credentials)
- Negative validation scenarios (invalid inputs)  
- Security testing (injection attacks)
- Registration flows (new user sign-up)
"""
import logging
import time

import pytest
import allure
from pages.login_page import LoginPage
from data.data_manager import data_manager


# python -m pytest tests/ui/functional/test_login_functional.py::TestLoginFunctional::test_login_with_valid_credentials -v
# docker run --rm -v ${PWD}:/app qa-tests python -m pytest tests/ui/functional/test_login_functional.py -v
#docker run --rm -v ${PWD}:/app qa-tests pytest my_new_test -v
@pytest.mark.functional
@allure.epic("Authentication")
@allure.feature("Login Functional Tests")
class TestLoginFunctional:
    """Functional tests for user login scenarios - validation and error cases."""

    @pytest.mark.flaky(reruns=3)
    @allure.title("Successful login with valid credentials")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("positive", "authentication")
    def test_login_with_valid_credentials(self, browser, login_url):
        """Verify successful login with correct credentials."""
        login_page = LoginPage(browser, login_url)

        with allure.step("Open login page"):
            login_page.open()

        with allure.step("Enter valid email and password"):
            user_credentials = data_manager.valid_user
            email = user_credentials["email"]
            password = user_credentials["password"]
            login_page.login_user(email, password)

        with allure.step("Verify user is successfully logged in"):
            login_page.should_be_successful_login()

    @allure.title("Login with invalid email format")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("negative", "validation")
    @pytest.mark.parametrize("invalid_email", data_manager.invalid_emails[:3])  # Test first 3 cases
    def test_login_with_invalid_email_format(self, browser, login_url, invalid_email):
        """Verify system validates email format correctly."""
        login_page = LoginPage(browser, login_url)

        with allure.step("Open login page"):
            login_page.open()

        with allure.step(f"Attempt login with invalid email: {invalid_email}"):
            password = ""
            login_page.login_user(invalid_email, password)
        with allure.step("Verify error message is shown"):
            # Implement error message verification
            login_page.should_be_invalid_email_message()

        with allure.step("Verify user NOT logged in"):
            login_page.should_be_login_page()
            login_page.should_be_login_url()

    @pytest.mark.new
    @allure.title("Login with non-existent email")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("negative", "validation")
    def test_login_with_nonexistent_email(self, browser, login_url):
        """Verify system handles non-existent users correctly."""
        login_page = LoginPage(browser, login_url)

        with allure.step("Open login page"):
            login_page.open()

        with allure.step("Attempt login with non-existent email"):
            # Use generated email that doesn't exist
            non_existent_email = login_page.generate_unique_email()
            password = ""
            login_page.login_user(non_existent_email, password)

        with allure.step("Verify appropriate error message is displayed"):
            # Implement error message verification
            login_page.should_be_invalid_email_message()

        with allure.step("Verify user NOT logged in"):
            login_page.should_be_login_page()
            login_page.should_be_login_url()

    @pytest.mark.new
    @allure.title("Login with incorrect password")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("negative", "security")
    def test_login_with_incorrect_password(self, browser, login_url):
        """Verify system rejects incorrect passwords."""
        login_page = LoginPage(browser, login_url)

        with allure.step("Open login page"):
            login_page.open()

        with allure.step("Attempt login with correct email but wrong password"):
            # Use valid email with wrong password
            user_credentials = data_manager.valid_user
            valid_email = user_credentials["email"]
            wrong_password = "Wrong" + user_credentials["password"]
            login_page.login_user(valid_email, wrong_password)

        with allure.step("Verify authentication error is shown"):
            # Implement error message verification
            login_page.should_be_invalid_password_message()

        with allure.step("Verify user NOT logged in"):
            login_page.should_be_login_page()
            login_page.should_be_login_url()

    @allure.title("Login with empty credentials")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("negative", "validation")
    @pytest.mark.parametrize("field,email,password", [
        ("email", "", "some_password"),
        ("password", "test@example.com", ""),
        ("both", "", "")
    ])
    def test_login_with_empty_credentials(self, browser, login_url, field, email, password):
        """Verify system requires all mandatory fields."""
        login_page = LoginPage(browser, login_url)

        with allure.step("Open login page"):
            login_page.open()

        with allure.step(f"Attempt login with empty {field}"):
            # Implement login with empty fields
            login_page.login_user(email, password)

        with allure.step("Verify required field error is shown"):
            # Implement validation error verification
            if email == "":
                login_page.should_be_invalid_email_message()
            if password == "":
                login_page.should_be_invalid_password_message()

        with allure.step("Verify user NOT logged in"):
            login_page.should_be_login_page()
            login_page.should_be_login_url()

    @allure.title("Security: SQL injection attempt in login")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("security", "negative")
    def test_login_with_sql_injection_attempt(self, browser, login_url):
        """Verify system is protected against SQL injection."""
        login_page = LoginPage(browser, login_url)

        with allure.step("Open login page"):
            login_page.open()

        with allure.step("Attempt SQL injection in email field"):
            # Use test_data.sql_injection
            user_credentials = data_manager.sql_injection

        with allure.step("Verify system rejects injection attempt safely"):
            # TODO: Implement security validation
            pass

    @allure.title("Login with very long password")
    @allure.severity(allure.severity_level.MINOR)
    @allure.tag("negative", "validation")
    def test_login_with_very_long_password(self, browser, login_url):
        """Verify system handles extremely long passwords correctly."""
        login_page = LoginPage(browser, login_url)

        with allure.step("Open login page"):
            login_page.open()

        with allure.step("Attempt login with very long password"):
            # TODO: Use test_data.weak_passwords for long password
            pass

        with allure.step("Verify system handles long input appropriately"):
            # TODO: Implement input length validation
            pass


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
            login_page.should_be_login_page()
            login_page.should_be_login_url()
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
            login_page.should_be_login_page()
            login_page.should_be_login_url()
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
            login_page.should_be_login_page()
            login_page.should_be_login_url()
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
            # TODO: Use test_data.valid_user email
            pass

        with allure.step("Verify duplicate email error is shown"):
            # TODO: Implement duplicate email validation
            pass

    @allure.title("Security: XSS attempt in registration")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("security", "negative")
    def test_registration_with_xss_attempt(self, browser, login_url):
        """Verify system is protected against XSS attacks."""
        login_page = LoginPage(browser, login_url)

        with allure.step("Open registration page"):
            login_page.open()

        with allure.step("Attempt XSS injection in registration fields"):
            # TODO: Use test_data.xss_attempt
            pass

        with allure.step("Verify system sanitizes input safely"):
            # TODO: Implement XSS protection validation
            pass
