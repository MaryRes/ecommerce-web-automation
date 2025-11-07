"""Module description"""


import re

import allure

from pages.base_page import BasePage
from pages.locators import ProductPageLocators
import logging

logger = logging.getLogger(__name__)

class ProductPage(BasePage):
    """
    Minimal product page object used by the e2e tests.
    Expects a Selenium WebDriver instance (fixture named `browser` in tests).
    """

    @allure.step("Verify product page elements")
    def should_be_product_page(self, expected_name: str):
        """Check that we are on a product page by verifying the URL pattern."""
        self.should_be_add_to_basket_button()
        self.should_be_product_name(expected_name)
        self.should_be_product_price()

    @allure.step("Verify 'Add to Basket' button presence")
    def should_be_add_to_basket_button(self):
        """Check that the 'Add to Basket' button is present on the product page."""
        assert self.is_element_present(ProductPageLocators.ADD_TO_BASKET_BTN), (
            "'Add to Basket' button is not present on the product page"
        )
        logger.info("'Add to Basket' button presence verified")

    @allure.step("Verify product name")
    def should_be_product_name(self, expected_name: str):
        """Check that the product name on the page matches the expected name."""
        if self.is_element_present(ProductPageLocators.PRODUCT_NAME):
             logger.info("Product name element is not present on the product page")
        actual_name = self.get_text(ProductPageLocators.PRODUCT_NAME)
        assert actual_name == expected_name, (
            f"Product name mismatch: expected '{expected_name}', got '{actual_name}'"
        )

    @allure.step("Verify product price presence")
    def should_be_product_price(self):
        """Check that the product price element is present on the product page."""
        assert self.is_element_present(ProductPageLocators.PRODUCT_PRICE), (
            "Product price element is not present on the product page"
        )
        logger.info("Product price element presence verified")

    @allure.step("Add product to basket")
    def add_to_basket(self):
        """Click the 'Add to Basket' button to add the product to the shopping basket."""
        self.click(ProductPageLocators.ADD_TO_BASKET_BTN)
        logger.info("Clicked 'Add to Basket' button")

    @allure.step("Click basket link in header to go to basket page")
    def go_to_basket_from_header(self):
        """
        Click the basket link in the header to navigate to the basket page.
        """

        self.click(ProductPageLocators.BASKET_LINK_IN_HEADER)
        success = self._wait_for_url_contains("/basket")
        assert success, "Failed to navigate to basket page"
        logger.info("Navigated to basket page")



