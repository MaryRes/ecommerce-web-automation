#

import pytest
import logging
import allure
from pages.login_page import LoginPage

logger = logging.getLogger(__name__)


#pytest -m "regression and ui" -v -s --log-cli-level=INFO --alluredir=allure-results --tb=short

@pytest.mark.regression
@pytest.mark.ui
@allure.epic("Authentication")
@allure.feature("Login Page Regression Tests")
class TestLoginPageRegression:
    """
    Regression tests for login page - comprehensive functionality check.
    """

    @allure.title("REG-UI: Test Login Page Opens by URL")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("Verify that the login page opens correctly via URL")
    def test_login_page_opens_by_url(self, browser, login_url):
        """
        Test that login page opens correctly via URL.
        """
        login_page = LoginPage(browser, login_url)
        with allure.step("Open login page via URL"):
            logger.info("Testing login page opening via URL...")
            login_page.open()

        with allure.step("Verify URL includes 'login'"):
            login_page.should_be_login_url()
            logger.info("✓ Login page opens correctly via URL")

    @allure.title("REG-UI: Test Login Form Presence on Login Page")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("Verify that the login form is present on the login page")
    def test_login_form_present(self, browser, login_url):
        """
        Test that login form is present on the login page.
        """
        login_page = LoginPage(browser, login_url)
        with allure.step("Open login page"):
            logger.info("Testing presence of login form...")
            login_page.open()

        with allure.step("Verify login form presence"):
            login_page.should_be_login_form()
            logger.info("✓ Login form is present on the page")

    @allure.title("REG-UI: Test Registration Form Presence on Login Page")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("Verify that the registration form is present on the login page")
    def test_registration_form_present(self, browser, login_url):
        """
        Test that registration form is present on the login page.
        """
        login_page = LoginPage(browser, login_url)
        with allure.step("Open login page"):
            logger.info("Testing presence of registration form...")
            login_page.open()

        with allure.step("Verify registration form presence"):
            login_page.should_be_register_form()
            logger.info("✓ Registration form is present on the page")

    # ===== INDIVIDUAL ELEMENT TESTS =====
    @allure.title("REG-UI: Test Login Email Field Accessibility")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_login_email_field_accessible(self, browser, login_url):
        """
        Test that the email field in the login form is accessible.
        """
        login_page = LoginPage(browser, login_url)
        logger.info("Testing accessibility of login email field...")
        login_page.open()
        login_page.should_have_accessible_login_email_field()
        logger.info("✓ Login email field is accessible")

    @allure.title("REG-UI: Test Login Password Field Accessibility")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_login_password_field_accessible(self, browser, login_url):
        """
        Test that the password field in the login form is accessible.
        """
        login_page = LoginPage(browser, login_url)
        logger.info("Testing accessibility of login password field...")
        login_page.open()
        login_page.should_have_accessible_login_password_field()
        logger.info("✓ Login password field is accessible")

    @allure.title("REG-UI: Test Login Submit Button Accessibility")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_login_submit_button_accessible(self, browser, login_url):
        """
        Test that the submit button in the login form is accessible.
        """
        login_page = LoginPage(browser, login_url)

        logger.info("Testing accessibility of login submit button...")
        login_page.open()
        login_page.should_have_accessible_login_submit_button()
        logger.info("✓ Login submit button is accessible")

    @allure.title("REG-UI: Test Registration Email Field Accessibility")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_registration_email_field_accessible(self, browser, login_url):
        """
        Test that the email field in the registration form is accessible.
        """
        login_page = LoginPage(browser, login_url)
        logger.info("Testing accessibility of registration email field...")
        login_page.open()
        login_page.should_have_accessible_registration_email_field()
        logger.info("✓ Registration email field is accessible")

    @allure.title("REG-UI: Test Registration Password Field Accessibility")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_registration_password_field_accessible(self, browser, login_url):
        """
        Test that the password field in the registration form is accessible.
        """
        login_page = LoginPage(browser, login_url)

        logger.info("Testing accessibility of registration password field...")
        login_page.open()
        login_page.should_have_accessible_registration_password_field()
        logger.info("✓ Registration password field is accessible")

    @allure.title("REG-UI: Test Registration Confirm Password Field Accessibility")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_registration_confirm_password_field_accessible(self, browser, login_url):
        """
        Test that the confirmation password field in the registration form is accessible.
        """
        login_page = LoginPage(browser, login_url)

        logger.info("Testing accessibility of registration confirm password field...")
        login_page.open()
        login_page.should_have_accessible_registration_confirm_password_field()
        logger.info("✓ Registration confirm password field is accessible")

    @allure.title("REG-UI: Test Registration Submit Button Accessibility")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_registration_submit_button_accessible(self, browser, login_url):
        """
        Test that the submit button in the registration form is accessible.
        """
        login_page = LoginPage(browser, login_url)

        logger.info("Testing accessibility of registration submit button...")
        login_page.open()
        login_page.should_have_accessible_registration_submit_button()
        logger.info("✓ Registration submit button is accessible")
