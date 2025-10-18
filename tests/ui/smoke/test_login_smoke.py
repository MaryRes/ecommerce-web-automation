import pytest
import logging
from selenium.webdriver.common.by import By

logger = logging.getLogger(__name__)

# pytest tests/test_login_smoke.py -v
# pytest -v -s --log-cli-level=INFO --tb=short tests/ui/smoke/test_login_smoke.py
@pytest.mark.smoke
class TestLoginPageSmoke:
    """Smoke tests for login page - basic functionality check."""

    def test_login_page_opens(self, browser, login_url):
        """Test that login page can be opened."""
        logger.info("Testing login page opening...")
        browser.get(login_url)

        assert "login" in browser.current_url.lower()
        logger.info("✓ Login page opens correctly")

    def test_login_form_present(self, browser, login_url):
        """Test that login form exists on page."""
        logger.info("Testing login form presence...")
        browser.get(login_url)

        form = browser.find_element(By.ID, "login_form")
        assert form is not None
        logger.info("✓ Login form is present")

    def test_register_form_present(self, browser, login_url):
        """Test that registration form exists on page."""
        logger.info("Testing registration form presence...")
        browser.get(login_url)

        form = browser.find_element(By.ID, "register_form")
        assert form is not None
        logger.info("✓ Registration form is present")
