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

        # TODO: make_new_user with valid user_credentials creation before every test to avoid error 500!!!
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
            login_page.should_not_be_logged_in()
            login_page.should_be_login_page()

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
            login_page.should_not_be_logged_in()
            login_page.should_be_login_page()

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
            login_page.should_not_be_logged_in()
            login_page.should_be_login_page()

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
            login_page.should_not_be_logged_in()
            login_page.should_be_login_page()

    @pytest.mark.parametrize("sql_payload", [
        "' OR '1'='1",
        "' OR 1=1--",
        "admin'--",
        "' UNION SELECT 1,2,3--",
        "'; DROP TABLE users--",
        "' OR 'a'='a",
        "1'1",
        "\\' OR \\'1\\'=\\'1",
        "test@test.com' OR '1'='1",
        "something' OR email IS NOT NULL AND '1'='1"
    ], ids=[
        "basic_or_condition",
        "comment_bypass",
        "admin_access_attempt",
        "union_data_extraction",
        "destructive_drop_table",
        "always_true_condition",
        "quote_manipulation",
        "escaped_quotes",
        "email_with_injection",
        "complex_condition"
    ])
    @allure.title("Security: SQL injection attempt with payload: {sql_payload}")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("security", "negative")
    def test_login_with_sql_injection_attempt(self, browser, login_url, sql_payload):
        """Verify system is protected against SQL injection."""
        login_page = LoginPage(browser, login_url)
        user_credentials = data_manager.valid_user
        email = user_credentials["email"]
        password = user_credentials["password"]

        with allure.step("Open login page"):
            login_page.open()

        with allure.step("Attempt SQL injection in email field"):
            login_page.login_user(sql_payload, password)

        with allure.step("Verify system rejects injection attempt safely"):
            login_page.should_be_invalid_email_message()

        with allure.step("Verify user NOT logged in"):
            login_page.should_not_be_logged_in()

        with allure.step("Verify user is on login page"):
            login_page.should_be_login_page()

        with allure.step("Verify login form still functional"):
            login_page.login_user(email, password)
            login_page.should_be_logged_in()

        with allure.step("Cleanup: logout for next test case"):
            login_page.logout_user()

    @allure.title("Login with very long password")
    @allure.severity(allure.severity_level.MINOR)
    @allure.tag("negative", "validation")
    def test_login_with_very_long_password(self, browser, login_url):
        """Verify system handles extremely long passwords correctly."""
        login_page = LoginPage(browser, login_url)

        with allure.step("Open login page"):
            login_page.open()

        with allure.step("Attempt login with very long password"):
            email = data_manager.valid_user["email"]
            long_password = "A" * 1000  # Example of a very long password
            login_page.login_user(email, long_password)

        with allure.step("Verify system handles long input appropriately"):
            login_page.should_be_invalid_password_message()

        with allure.step("Verify user NOT logged in"):
            login_page.should_not_be_logged_in()
            login_page.should_be_login_page()


