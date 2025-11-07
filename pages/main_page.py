"""Module description"""
import allure
import logging
from .base_page import BasePage
from .locators import MainPageLocators
from selenium.common.exceptions import TimeoutException

logger = logging.getLogger(__name__)


class MainPage(BasePage):

    @allure.step("Navigate to catalog page")
    def go_to_catalog(self):
        """Navigate to the catalog page."""
        current_url = self.get_current_url()
        self.click(MainPageLocators.CATALOG_LINK_IN_HEADER)

        if self._wait_for_url_change(current_url):
            logger.info("Successfully navigated to catalog page")
        else:
            raise TimeoutException("Catalog page navigation timeout")