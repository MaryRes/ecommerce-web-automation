import math
import time
import logging
from typing import List, Tuple, Optional, Union, Any
from selenium.common.exceptions import NoSuchElementException, NoAlertPresentException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from .locators import BasePageLocators

logger = logging.getLogger(__name__)


class WaitConfig:
    """Configuration for wait times."""
    DEFAULT_TIMEOUT = 10
    POLL_FREQUENCY = 0.5


class BasePage:
    """
    Base page class with consistent Pythonic methods for all pages.

    Key improvements:
    - Consistent naming convention
    - Reduced code duplication
    - Better type hints
    - Context manager for temporary waits
    - More descriptive method names
    - Separation of concerns
    """

    def __init__(
            self,
            browser: WebDriver,
            url: str,
            timeout: int = WaitConfig.DEFAULT_TIMEOUT,
            use_implicit_wait: bool = False,  # Explicit waits are preferred
            poll_frequency: float = WaitConfig.POLL_FREQUENCY
    ):
        self.browser = browser
        self.url = url
        self.timeout = timeout
        self._wait = WebDriverWait(browser, timeout, poll_frequency=poll_frequency)

        # Avoid implicit waits when using explicit waits
        if use_implicit_wait:
            self.browser.implicitly_wait(timeout)
        else:
            self.browser.implicitly_wait(0)

        logger.info("Initialized BasePage for URL: %s", url)

    def open(self) -> None:
        """Open the page URL."""
        self.browser.get(self.url)
        logger.debug("Opened page: %s", self.url)

    # ====== CONTEXT MANAGERS ======

    def _temporary_wait(self, timeout: Optional[int] = None) -> WebDriverWait:
        """Create a temporary WebDriverWait instance."""
        return WebDriverWait(
            self.browser,
            timeout if timeout is not None else self.timeout,
            poll_frequency=self._wait._poll
        )

    # ====== ELEMENT PRESENCE & VISIBILITY INCLUDING WAITING ======

    def is_element_present(self, locator: Tuple[By, str], timeout: Optional[int] = None) -> bool:
        """Check if element is present in DOM."""
        try:
            self._temporary_wait(timeout).until(EC.presence_of_element_located(locator))
            return True
        except NoSuchElementException:
            return False

    def is_element_visible(self, locator: Tuple[By, str], timeout: Optional[int] = None) -> bool:
        """Check if element is visible on page."""
        try:
            self._temporary_wait(timeout).until(EC.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False

    def is_element_clickable(self, locator: Tuple[By, str], timeout: Optional[int] = None) -> bool:
        """Check if element is clickable."""
        try:
            self._temporary_wait(timeout).until(EC.element_to_be_clickable(locator))
            return True
        except TimeoutException:
            return False

    def is_element_absent(self, locator: Tuple[By, str], timeout: Optional[int] = None) -> bool:
        """Check that element is NOT present in DOM."""
        try:
            self._temporary_wait(timeout).until_not(EC.presence_of_element_located(locator))
            return True
        except TimeoutException:
            return False

    def is_element_invisible(self, locator: Tuple[By, str], timeout: Optional[int] = None) -> bool:
        """Check that element is NOT visible (may still be in DOM)."""
        try:
            self._temporary_wait(timeout).until(EC.invisibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False

    # ====== WAIT METHODS ======

    def wait_for_presence(self, locator: Tuple[By, str], timeout: Optional[int] = None) -> WebElement:
        """Wait for element to be present in DOM and return it."""
        return self._temporary_wait(timeout).until(EC.presence_of_element_located(locator))

    def wait_for_presence_of_all(self, locator: Tuple[By, str], timeout: Optional[int] = None) -> List[WebElement]:
        """Wait for all elements to be present in DOM and return them."""
        return self._temporary_wait(timeout).until(EC.presence_of_all_elements_located(locator))

    def wait_for_visibility(self, locator: Tuple[By, str], timeout: Optional[int] = None) -> WebElement:
        """Wait for element to be visible and return it."""
        return self._temporary_wait(timeout).until(EC.visibility_of_element_located(locator))

    def wait_for_clickable(self, locator: Tuple[By, str], timeout: Optional[int] = None) -> WebElement:
        """Wait for element to be clickable and return it."""
        return self._temporary_wait(timeout).until(EC.element_to_be_clickable(locator))

    def wait_for_url_contains(self, text: str, timeout: Optional[int] = None) -> bool:
        """Wait for URL to contain specific text."""
        try:
            self._temporary_wait(timeout).until(EC.url_contains(text))
            logger.debug("URL now contains '%s'", text)
            return True
        except TimeoutException:
            logger.warning("URL does not contain '%s' within timeout", text)
            return False

    def wait_for_url_change(self, original_url: Optional[str] = None, timeout: Optional[int] = None) -> bool:
        """Wait for URL to change from original URL."""
        original = original_url or self.browser.current_url
        try:
            self._temporary_wait(timeout).until(lambda driver: driver.current_url != original)
            logger.debug("URL changed from %s to %s", original, self.browser.current_url)
            return True
        except TimeoutException:
            logger.warning("URL did not change from %s within timeout", original)
            return False

    # ====== ELEMENT INTERACTIONS ======

    def click(self, locator: Tuple[By, str], timeout: Optional[int] = None) -> None:
        """Click on element after ensuring it's clickable."""
        element = self.wait_for_clickable(locator, timeout)
        element.click()
        logger.debug("Clicked element: %s", locator)

    def send_keys(self, locator: Tuple[By, str], text: str, timeout: Optional[int] = None) -> None:
        """Type text into input field after ensuring it's clickable."""
        element = self.wait_for_clickable(locator, timeout)
        element.clear()
        element.send_keys(text)
        logger.debug("Typed text '%s' into %s", text, locator)

    def get_text(self, locator: Tuple[By, str], timeout: Optional[int] = None) -> str:
        """Get text from visible element."""
        element = self.wait_for_presence(locator, timeout)
        return element.text.strip()

    def get_all_texts(self, locator: Tuple[By, str], timeout: Optional[int] = None) -> List[str]:
        """Get texts from all matching elements."""
        elements = self.wait_for_presence_of_all(locator, timeout)
        return [element.text.strip() for element in elements]

    # ====== NAVIGATION METHODS ======

    def go_to_login_page(self) -> None:
        """Navigate to login page."""
        self.click(BasePageLocators.LOGIN_LINK)
        if self.wait_for_url_contains("login"):
            logger.info("Successfully navigated to login page")
        else:
            raise TimeoutException("Login page navigation timeout")

    # ====== ALERT AND QUIZ METHODS ======

    def solve_quiz_and_accept(self) -> None:
        """Solve math quiz from alert and accept result."""
        try:
            alert = self.browser.switch_to.alert
            x = alert.text.split(" ")[2]
            answer = str(math.log(abs(12 * math.sin(float(x)))))
            alert.send_keys(answer)
            alert.accept()

            # Handle result alert if present
            try:
                alert = self.browser.switch_to.alert
                logger.info("Quiz result: %s", alert.text)
                alert.accept()
            except NoAlertPresentException:
                logger.debug("No result alert presented")

        except Exception as e:
            logger.error("Error solving quiz: %s", e)
            raise

    # ====== ASSERTION METHODS ======

    def should_have_login_link(self) -> None:
        """Verify that login link is present."""
        assert self.is_element_present(BasePageLocators.LOGIN_LINK), "Login link is not present"

    def assert_text_equals(self, locator: Tuple[By, str], expected_text: str) -> None:
        """Assert that element text equals expected text."""
        actual_text = self.get_text(locator)
        assert actual_text == expected_text, f"Expected '{expected_text}', got '{actual_text}'"

    def assert_text_contains(self, locator: Tuple[By, str], expected_substring: str) -> None:
        """Assert that element text contains substring."""
        actual_text = self.get_text(locator)
        assert expected_substring in actual_text, f"Text '{actual_text}' doesn't contain '{expected_substring}'"

    def assert_all_texts_equal(self, locators: List[Tuple[By, str]]) -> None:
        """Assert that all elements have the same text."""
        texts = [self.get_text(locator) for locator in locators if self.is_element_present(locator)]

        if not texts:
            raise AssertionError("No elements found for comparison")

        unique_texts = set(texts)
        assert len(unique_texts) == 1, f"Texts are not equal: {unique_texts}"

    def assert_url_contains(self, expected_substring: str, timeout: Optional[int] = None) -> None:
        """Assert that current URL contains expected substring."""
        success = self.wait_for_url_contains(expected_substring, timeout)
        assert success, f"URL does not contain '{expected_substring}' within timeout. Current: {self.get_current_url()}"

    # ====== UTILITY METHODS ======

    def take_screenshot(self, name: str) -> str:
        """Take page screenshot and return file path."""
        filename = f"screenshots/{name}_{int(time.time())}.png"
        self.browser.save_screenshot(filename)
        logger.debug("Screenshot saved: %s", filename)
        return filename

    def get_current_url(self) -> str:
        """Get current page URL."""
        return self.browser.current_url

    def refresh(self) -> None:
        """Refresh current page."""
        self.browser.refresh()
        logger.debug("Page refreshed")

    @staticmethod
    def wait_seconds(seconds: float) -> None:
        """Wait for specified number of seconds (use sparingly)."""
        logger.debug("Waiting %.1f seconds", seconds)
        time.sleep(seconds)

    # ====== COMPATIBILITY METHODS ======

    # Legacy method names for backward compatibility
    def is_element_disappeared(self, locator: Tuple[By, str], timeout: Optional[int] = None) -> bool:
        """Legacy alias for is_element_invisible."""
        return self.is_element_invisible(locator, timeout)

    def is_not_element_present(self, locator: Tuple[By, str], timeout: Optional[int] = None) -> bool:
        """Legacy alias for is_element_absent."""
        return self.is_element_absent(locator, timeout)

    def wait_for_element_to_be_clickable(self, locator: Tuple[By, str], timeout: Optional[int] = None) -> None:
        """Legacy method - use wait_for_clickable instead."""
        self.wait_for_clickable(locator, timeout)

    def click_element(self, locator: Tuple[By, str], timeout: Optional[int] = None) -> None:
        """Legacy alias for click."""
        self.click(locator, timeout)

    def type_text(self, locator: Tuple[By, str], text: str, timeout: Optional[int] = None) -> None:
        """Legacy alias for send_keys."""
        self.send_keys(locator, text, timeout)