"""Module description"""
from selenium.common import TimeoutException

from .base_page import BasePage
from .locators import CatalogPageLocators
import allure
import logging
from selenium.webdriver.common.by import By

logger = logging.getLogger(__name__)


class CatalogPage(BasePage):

    @allure.step("Verify catalog page elements")
    def should_be_catalog_page(self):
        self.should_be_catalog_url()
        self.should_be_product_list()
        self.should_have_category_sidebar()
        logger.info("Catalog page verification completed successfully")
        return self

    @allure.step("Check if current URL is catalog URL")
    def should_be_catalog_url(self):
        current_url = self.get_current_url()
        assert "catalogue" in current_url, (
            f"Current URL does not contain 'catalogue'. Current URL: {current_url}"
        )
        logger.debug("Catalog URL verified: %s", current_url)

    @allure.step("Check for category sidebar presence")
    def should_have_category_sidebar(self):
        assert self.is_element_present(CatalogPageLocators.SIDE_CATEGORIES), (
            "Category sidebar is not present on the catalog page"
        )
        logger.debug("Category sidebar verified")

    def get_available_product_titles(self) -> list:
        """Get list of all available product titles on page"""
        try:
            product_links = self.browser.find_elements(By.CSS_SELECTOR, "article.product_pod h3 a")
            titles = []
            for link in product_links:
                title = link.get_attribute("title")
                if title:
                    titles.append(title)
            logger.info(f"Found {len(titles)} available products: {titles}")
            return titles
        except Exception as e:
            logger.error(f"Error getting available products: {e}")
            return []

    @allure.step("Check for product list presence")
    def should_be_product_list(self):
        assert self.is_element_present(CatalogPageLocators.PRODUCT_LIST), (
            "Product list is not present on the catalog page"
        )
        logger.debug("Product list presence verified")

    def select_product(self, product_name: str, timeout=10):
        """Click product link to open product details page"""

        product_link_locator = self._get_product_link_locator_by_name(product_name)
        logger.debug("Selecting product '%s'", product_name)

        current_url_before = self.get_current_url()
        product_link = self.wait_for_clickable(product_link_locator, timeout)
        product_link.click()

        if self._wait_for_url_change(current_url_before, timeout):
            logger.info("Successfully navigated to product page for '%s'", product_name)
        else:
            raise TimeoutException(f"Product page navigation timeout for '{product_name}'")

    def add_product_to_basket_from_catalog(self, product_name: str):
        """Add product to basket directly from catalog page"""
        pass

    def _get_product_card_locator_by_name(self, product_name: str):
        """Generate locator for specific product card by name"""
        return (By.XPATH, f'//article[.//a[@title="{product_name}"]]')


    def _get_product_link_locator_by_name(self, product_name: str):
        """Generate locator for product link by name"""
        return (By.XPATH, f'//article[.//a[@title="{product_name}"]]//a')


    def _get_add_button_locator_by_name(self, product_name: str):
        """Generate locator for add to basket button by product name"""
        return By.XPATH, f'//article[.//a[@title="{product_name}"]]//button[contains(@class, "btn-add-to-basket")]'