import math
import time
import logging
import allure
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
    Base page class for all page objects.
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

    @allure.step("Open page URL")
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
    @allure.step("Check if element is present: {locator}")
    def is_element_present(self, locator: Tuple[By, str], timeout: Optional[int] = None) -> bool:
        """Check if element is present in DOM."""
        try:
            self._temporary_wait(timeout).until(EC.presence_of_element_located(locator))
            return True
        except NoSuchElementException:
            return False

    @allure.step("Check if element is visible: {locator}")
    def is_element_visible(self, locator: Tuple[By, str], timeout: Optional[int] = None) -> bool:
        """Check if element is visible on page."""
        try:
            self._temporary_wait(timeout).until(EC.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False

    @allure.step("Check if element is clickable: {locator}")
    def is_element_clickable(self, locator: Tuple[By, str], timeout: Optional[int] = None) -> bool:
        """Check if element is clickable."""
        try:
            self._temporary_wait(timeout).until(EC.element_to_be_clickable(locator))
            return True
        except TimeoutException:
            return False

    @allure.step("Check if element is absent: {locator}")
    def is_element_absent(self, locator: Tuple[By, str], timeout: Optional[int] = None) -> bool:
        """Check that element is NOT present in DOM."""
        try:
            self._temporary_wait(timeout).until_not(EC.presence_of_element_located(locator))
            return True
        except TimeoutException:
            return False

    @allure.step("Check if element is invisible: {locator}")
    def is_element_invisible(self, locator: Tuple[By, str], timeout: Optional[int] = None) -> bool:
        """Check that element is NOT visible (may still be in DOM)."""
        try:
            self._temporary_wait(timeout).until(EC.invisibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False

    # ====== WAIT METHODS ======
    @allure.step("Wait for presence of element: {locator}")
    def wait_for_presence(self, locator: Tuple[By, str], timeout: Optional[int] = None) -> WebElement:
        """Wait for element to be present in DOM and return it."""
        return self._temporary_wait(timeout).until(EC.presence_of_element_located(locator))

    @allure.step("Wait for presence of all elements: {locator}")
    def wait_for_presence_of_all(self, locator: Tuple[By, str], timeout: Optional[int] = None) -> List[WebElement]:
        """Wait for all elements with locator to be present in DOM and return them."""
        return self._temporary_wait(timeout).until(EC.presence_of_all_elements_located(locator))

    @allure.step("Wait for visibility of element: {locator}")
    def wait_for_visibility(self, locator: Tuple[By, str], timeout: Optional[int] = None) -> WebElement:
        """Wait for element to be visible and return it."""
        return self._temporary_wait(timeout).until(EC.visibility_of_element_located(locator))

    @allure.step("Wait for element to be clickable: {locator}")
    def wait_for_clickable(self, locator: Tuple[By, str], timeout: Optional[int] = None) -> WebElement:
        """Wait for element to be clickable and return it."""
        return self._temporary_wait(timeout).until(EC.element_to_be_clickable(locator))

    def _wait_for_url_contains(self, text: str, timeout: Optional[int] = None) -> bool:
        """Wait for URL to contain specific text."""
        try:
            self._temporary_wait(timeout).until(EC.url_contains(text))
            logger.debug("URL now contains '%s'", text)
            return True
        except TimeoutException:
            logger.warning("URL does not contain '%s' within timeout", text)
            return False

    @allure.step("Wait for URL to change from: {original_url}")
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
    @allure.step("Click on element: {locator}")
    def click(self, locator: Tuple[By, str], timeout: Optional[int] = None) -> None:
        """Click on element after ensuring it's clickable."""
        element = self.wait_for_clickable(locator, timeout)
        element.click()
        logger.debug("Clicked element: %s", locator)

    @allure.step("Type text '{text}' to element: {locator}")
    def send_keys(self, locator: Tuple[By, str], text: str, timeout: Optional[int] = None) -> None:
        """Type text into input field after ensuring it's clickable."""
        element = self.wait_for_clickable(locator, timeout)
        element.clear()
        element.send_keys(text)
        logger.debug("Typed text '%s' into %s", text, locator)

    @allure.step("Get text from element: {locator}")
    def get_text(self, locator: Tuple[By, str], timeout: Optional[int] = None) -> str:
        """Get text from visible element."""
        element = self.wait_for_presence(locator, timeout)
        return element.text.strip()

    @allure.step("Get texts from all matching elements: {locator}")
    def get_all_texts(self, locator: Tuple[By, str], timeout: Optional[int] = None) -> List[str]:
        """Get texts from all matching elements."""
        elements = self.wait_for_presence_of_all(locator, timeout)
        return [element.text.strip() for element in elements]

    # ====== NAVIGATION METHODS ======
    @allure.step("Navigate to login page")
    def go_to_login_page(self) -> None:
        """Navigate to login page."""
        self.click(BasePageLocators.LOGIN_LINK)
        if self._wait_for_url_contains("login"):
            logger.info("Successfully navigated to login page")
        else:
            raise TimeoutException("Login page navigation timeout")

    # ====== ALERT AND QUIZ METHODS ======

    @allure.step("Solve quiz from alert and accept")
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

    # ===== UNIVERSAL VERIFICATION METHODS =====
    @allure.step("Verify that element is clickable: {element_name}")
    def should_be_element_clickable(self, locator: Tuple[By, str], element_name: str, timeout: Optional[int] = None) -> None:
        """Verify that element is clickable."""

        assert self.is_element_clickable(locator, timeout), f"Element {element_name} is not clickable"
        logger.debug("Element %s is clickable", element_name)

    @allure.step("Verify that element is present: {element_name}")
    def should_be_element_present(self, locator: Tuple[By, str], element_name: str, timeout: Optional[int] = None) -> None:
        """Verify that element is present."""

        assert self.is_element_present(locator, timeout), f"Element {element_name} is not present"
        logger.debug("Element %s is present", element_name)

    @allure.step("Verify that element is accessible: {element_name}")
    def should_be_element_accessible(self, locator: Tuple[By, str], element_name: str, timeout: Optional[int] = None) -> None:
        """Verify that element is accessible (visible and clickable)."""

        self.should_be_element_present(locator, element_name, timeout)
        self.should_be_element_clickable(locator, element_name, timeout)
        logger.debug("Element %s is accessible", element_name)

    @allure.step("Verify that element is NOT present: {element_name}")
    def should_not_be_element_present(self, locator: Tuple[By, str], element_name: str, timeout: Optional[int] = None) -> None:
        """Verify that element is NOT present."""
        assert self.is_element_absent(locator, timeout), f"Element {element_name} is present but should not be"
        logger.debug("Element %s is not present as expected", element_name)

    @allure.step("Verify that element has expected text: {expected_text}")
    def should_have_element_text(
            self,
            locator: Tuple[By, str],
            expected_text: str,
            element_name: str,
            timeout: Optional[int] = None
    ) -> None:
        """Verify that element has expected text."""
        actual_text = self.get_text(locator, timeout)
        assert actual_text == expected_text, f"Element {element_name} text mismatch: expected '{expected_text}', got '{actual_text}'"
        logger.debug("Element %s has expected text: %s", element_name, expected_text)

    @allure.step("Verify that element text contains expected substring: {expected_substring}")
    def should_contain_element_text(
            self,
            locator: Tuple[By, str],
            expected_substring: str,
            element_name: str,
            timeout: Optional[int] = None
    ) -> None:
        """Verify that element text contains expected substring."""
        actual_text = self.get_text(locator, timeout)
        assert expected_substring in actual_text, f"Element {element_name} text does not contain '{expected_substring}'"
        logger.debug("Element %s text contains expected substring: %s", element_name, expected_substring)

    # ====== ASSERTION METHODS ======
    @allure.step("Verify that login link is present")
    def should_have_login_link(self) -> None:
        """Verify that login link is present."""
        assert self.is_element_present(BasePageLocators.LOGIN_LINK), "Login link is not present"

    @allure.step("Assert that element text equals expected text: {expected_text}")
    def assert_text_equals(self, locator: Tuple[By, str], expected_text: str) -> None:
        """Assert that element text equals expected text."""
        actual_text = self.get_text(locator)
        assert actual_text == expected_text, f"Expected '{expected_text}', got '{actual_text}'"

    @allure.step("Assert that element text contains substring: {expected_substring}")
    def assert_text_contains(self, locator: Tuple[By, str], expected_substring: str) -> None:
        """Assert that element text contains substring."""
        actual_text = self.get_text(locator)
        assert expected_substring in actual_text, f"Text '{actual_text}' doesn't contain '{expected_substring}'"

    @allure.step("Assert that all elements have equal text")
    def assert_all_texts_equal(self, locators: List[Tuple[By, str]]) -> None:
        """Assert that all elements have the same text."""
        texts = [self.get_text(locator) for locator in locators if self.is_element_present(locator)]

        if not texts:
            raise AssertionError("No elements found for comparison")

        unique_texts = set(texts)
        assert len(unique_texts) == 1, f"Texts are not equal: {unique_texts}"

    @allure.step("Assert that current URL contains substring: {expected_substring}")
    def assert_url_contains(self, expected_substring: str, timeout: Optional[int] = None) -> None:
        """Assert that current URL contains expected substring."""
        success = self._wait_for_url_contains(expected_substring, timeout)
        assert success, f"URL does not contain '{expected_substring}' within timeout. Current: {self.get_current_url()}"

    # ====== UTILITY METHODS ======

    def _take_screenshot(self, name: str) -> str:
        """Take page screenshot and return file path."""
        filename = f"screenshots/{name}_{int(time.time())}.png"
        self.browser.save_screenshot(filename)
        logger.debug("Screenshot saved: %s", filename)
        return filename

    @allure.step("Get current page URL")
    def get_current_url(self) -> str:
        """Get current page URL."""
        return self.browser.current_url

    @allure.step("Refresh current page")
    def refresh(self) -> None:
        """Refresh current page."""
        self.browser.refresh()
        logger.debug("Page refreshed")

    @staticmethod
    def _wait_seconds(seconds: float) -> None:
        """Wait for specified number of seconds (use sparingly)."""
        logger.debug("Waiting %.1f seconds", seconds)
        time.sleep(seconds)

    # ====== COMPATIBILITY METHODS ======

    # Legacy method names for backward compatibility
    @allure.step("Check if element has disappeared: {locator}")
    def is_element_disappeared(self, locator: Tuple[By, str], timeout: Optional[int] = None) -> bool:
        """Legacy alias for is_element_invisible."""
        return self.is_element_invisible(locator, timeout)

    @allure.step("Check if element is not present: {locator}")
    def is_not_element_present(self, locator: Tuple[By, str], timeout: Optional[int] = None) -> bool:
        """Legacy alias for is_element_absent."""
        return self.is_element_absent(locator, timeout)

    @allure.step("Wait for element to be clickable: {locator}")
    def wait_for_element_to_be_clickable(self, locator: Tuple[By, str], timeout: Optional[int] = None) -> None:
        """Legacy method - use wait_for_clickable instead."""
        self.wait_for_clickable(locator, timeout)

    @allure.step("Click on element (legacy): {locator}")
    def click_element(self, locator: Tuple[By, str], timeout: Optional[int] = None) -> None:
        """Legacy alias for click."""
        self.click(locator, timeout)

    @allure.step("Type text to element (legacy): {locator}")
    def type_text(self, locator: Tuple[By, str], text: str, timeout: Optional[int] = None) -> None:
        """Legacy alias for send_keys."""
        self.send_keys(locator, text, timeout)
