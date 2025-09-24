import math
import time
import logging
from typing import List, Tuple, Optional, Union
from selenium.common.exceptions import NoSuchElementException, NoAlertPresentException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from .locators import BasePageLocators

# Setup logger
logger = logging.getLogger(__name__)


class BasePage:
    """Base page class containing common methods for all pages."""

    def __init__(self, browser: WebDriver, url: str, timeout: int = 10, implicitly_wait: bool = True, poll_frequency: float = 0.5):
        """
        :param browser: WebDriver instance
        :param url: page URL
        :param timeout: element wait timeout
        :param implicitly_wait: if True, sets implicit wait for browser
        :param poll_frequency: how often to check for conditions
        """
        self.browser = browser
        self.url = url
        self.wait = WebDriverWait(browser, timeout=timeout, poll_frequency=poll_frequency)
        
        if implicitly_wait:
            self.browser.implicitly_wait(timeout)
        
        logger.info(f"Initialized BasePage for URL: {url}")

    def open(self) -> None:
        """Open the page."""
        self.browser.get(self.url)
        logger.debug(f"Opened page: {self.url}")

    def go_to_login_page(self) -> None:
        """Navigate to login page."""
        try:
            link = self.wait.until(EC.element_to_be_clickable(BasePageLocators.LOGIN_LINK))
            link.click()
            self.wait.until(EC.url_contains("login"))
            logger.info("Successfully navigated to login page")
        except Exception as e:
            logger.error(f"Error navigating to login page: {e}")
            raise

    def take_screenshot(self, name: str) -> str:
        """
        Take page screenshot.
        :param name: screenshot filename
        :return: path to saved file
        """
        filename = f"screenshots/{name}_{int(time.time())}.png"
        self.browser.save_screenshot(filename)
        logger.debug(f"Screenshot saved: {filename}")
        return filename

    # ====== ELEMENT PRESENCE METHODS ======

    def is_element_present(self, how: By, what: str) -> bool:
        """Check if element is present on page."""
        try:
            self.browser.find_element(how, what)
            return True
        except NoSuchElementException:
            return False

    def is_not_element_present(self, how: By, what: str, timeout: int = None) -> bool:
        """Check that element is NOT present on page."""
        wait = self.wait if timeout is None else WebDriverWait(self.browser, timeout)
        try:
            wait.until(EC.presence_of_element_located((how, what)))
            return False
        except TimeoutException:
            return True

    def is_element_visible(self, how: By, what: str, timeout: int = None) -> bool:
        """Check if element is visible."""
        wait = self.wait if timeout is None else WebDriverWait(self.browser, timeout)
        try:
            wait.until(EC.visibility_of_element_located((how, what)))
            return True
        except TimeoutException:
            return False

    def is_element_disappeared(self, how: By, what: str, timeout: int = None) -> bool:
        """Check that element has disappeared from page."""
        wait = self.wait if timeout is None else WebDriverWait(self.browser, timeout)
        try:
            wait.until_not(EC.presence_of_element_located((how, what)))
            return True
        except TimeoutException:
            return False

    def is_element_clickable(self, how: By, what: str, timeout: int = None) -> bool:
        """Check if element is clickable (works in headless)."""
        wait = self.wait if timeout is None else WebDriverWait(self.browser, timeout)
        try:
            wait.until(EC.element_to_be_clickable((how, what)))
            return True
        except TimeoutException:
            return False

    def is_element_in_dom(self, how: By, what: str) -> bool:
        """Check if element exists in DOM (most reliable)."""
        return self.is_element_present(how, what)

    def wait_for_element_present(self, locator: Tuple[By, str], timeout: int = None) -> bool:
        """Wait for element to be present in DOM."""
        wait = self.wait if timeout is None else WebDriverWait(self.browser, timeout)
        try:
            wait.until(EC.presence_of_element_located(locator))
            return True
        except TimeoutException:
            return False

    def wait_for_element_visible(self, locator: Tuple[By, str], timeout: int = None) -> bool:
        """Wait for element to be visible."""
        wait = self.wait if timeout is None else WebDriverWait(self.browser, timeout)
        try:
            wait.until(EC.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False

    # ====== INTERACTION METHODS ======

    def click_element(self, locator: Tuple[By, str], timeout: int = None) -> None:
        """Click on element with waiting."""
        wait = self.wait if timeout is None else WebDriverWait(self.browser, timeout)
        element = wait.until(EC.element_to_be_clickable(locator))
        element.click()
        logger.debug(f"Clicked element: {locator}")

    def type_text(self, locator: Tuple[By, str], text: str, timeout: int = None) -> None:
        """Type text into input field."""
        wait = self.wait if timeout is None else WebDriverWait(self.browser, timeout)
        element = wait.until(EC.element_to_be_clickable(locator))
        element.clear()
        element.send_keys(text)
        logger.debug(f"Typed text into {locator}")

    def get_text(self, locator: Tuple[By, str], timeout: int = None) -> str:
        """Get text from element."""
        wait = self.wait if timeout is None else WebDriverWait(self.browser, timeout)
        element = wait.until(EC.visibility_of_element_located(locator))
        return element.text.strip()

    def get_multiple_texts(self, locator: Tuple[By, str]) -> List[str]:
        """Get texts from multiple elements."""
        elements = self.browser.find_elements(*locator)
        return [element.text.strip() for element in elements]

    # ====== ALERT AND QUIZ METHODS ======

    def solve_quiz_and_get_code(self) -> None:
        """Solve math quiz from alert and accept result."""
        try:
            alert = self.browser.switch_to.alert
            x = alert.text.split(" ")[2]
            answer = str(math.log(abs(12 * math.sin(float(x)))))
            alert.send_keys(answer)
            alert.accept()
            
            try:
                alert = self.browser.switch_to.alert
                alert_text = alert.text
                logger.info(f"Quiz code: {alert_text}")
                alert.accept()
            except NoAlertPresentException:
                logger.debug("No second alert presented")
                
        except Exception as e:
            logger.error(f"Error solving quiz: {e}")
            raise

    # ====== VALIDATION METHODS ======

    def should_be_login_link(self) -> None:
        """Verify that login link is present."""
        assert self.is_element_present(*BasePageLocators.LOGIN_LINK), "Login link is not present"

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
        texts = []
        for locator in locators:
            if self.is_element_present(*locator):
                texts.append(self.get_text(locator))
        
        if not texts:
            raise AssertionError("No elements found for comparison")
        
        unique_texts = set(texts)
        assert len(unique_texts) == 1, f"Texts are not equal: {unique_texts}"

    # ====== UTILITY METHODS ======

    @staticmethod
    def wait_seconds(seconds: int) -> None:
        """Wait for specified number of seconds."""
        logger.debug(f"Waiting {seconds} seconds")
        time.sleep(seconds)

    def get_current_url(self) -> str:
        """Get current page URL."""
        return self.browser.current_url

    def refresh_page(self) -> None:
        """Refresh current page."""
        self.browser.refresh()
        logger.debug("Page refreshed")

    # ====== LEGACY METHODS (keep for compatibility) ======

    def check_same_value_in_different_sections(
        self,
        list_of_elements: List[Union[Tuple[By, str], List[Tuple[By, str]]]],
        expected_value: Optional[str] = None,
        flexible: bool = False
    ) -> Tuple[bool, str]:
        """Legacy method - use assert_all_texts_equal instead."""
        logger.warning("This method is deprecated. Use assert_all_texts_equal instead.")
        
        found_values: List[str] = []
        for element in list_of_elements:
            if isinstance(element, list):
                for sub_element in element:
                    elements = self.browser.find_elements(*sub_element)
                    found_values.extend([el.text.strip() for el in elements])
            else:
                elements = self.browser.find_elements(*element)
                found_values.extend([el.text.strip() for el in elements])

        if not found_values:
            return False, "No elements found for validation"

        if expected_value is None:
            expected_value = found_values[0]

        def to_float(val: str) -> Optional[float]:
            try:
                return float("".join(ch for ch in val if ch.isdigit() or ch in ".,").replace(",", "."))
            except ValueError:
                return None

        if flexible:
            expected_float = to_float(expected_value)
            mismatches = [val for val in found_values if to_float(val) != expected_float]
        else:
            mismatches = [val for val in found_values if val != expected_value]

        if mismatches:
            return False, f"Values don't match. Expected: '{expected_value}', Found: {found_values}"

        return True, ""