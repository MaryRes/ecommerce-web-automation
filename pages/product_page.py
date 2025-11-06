"""Module description"""


import re
from pages.base_page import BasePage
from pages.locators import ProductPageLocators
import logging

logger = logging.getLogger(__name__)

class ProductPage(BasePage):
    """
    Minimal product page object used by the e2e tests.
    Expects a Selenium WebDriver instance (fixture named `browser` in tests).
    """

    def should_be_product_page(self, expected_name: str):
        """Check that we are on a product page by verifying the URL pattern."""
        self.should_be_add_to_basket_button()
        self.should_be_product_name(expected_name)
        self.should_be_product_price()

    def should_be_add_to_basket_button(self):
        """Check that the 'Add to Basket' button is present on the product page."""
        assert self.is_element_present(ProductPageLocators.ADD_TO_BASKET_BTN), (
            "'Add to Basket' button is not present on the product page"
        )
        logger.info("'Add to Basket' button presence verified")

    def should_be_product_name(self, expected_name: str):
        """Check that the product name on the page matches the expected name."""
        if self.is_element_present(ProductPageLocators.PRODUCT_NAME):
             logger.info("Product name element is not present on the product page")
        actual_name = self.get_text(ProductPageLocators.PRODUCT_NAME)
        assert actual_name == expected_name, (
            f"Product name mismatch: expected '{expected_name}', got '{actual_name}'"
        )

    def should_be_product_price(self):
        """Check that the product price element is present on the product page."""
        assert self.is_element_present(ProductPageLocators.PRODUCT_PRICE), (
            "Product price element is not present on the product page"
        )
        logger.info("Product price element presence verified")


