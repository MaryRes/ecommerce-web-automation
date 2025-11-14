"""Module description"""


import re
import allure
from pages.base_page import BasePage
from pages.locators import ProductPageLocators
from utils.helpers import parse_international_price
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
    def add_to_basket(self, product_name: str = None):
        """Click the 'Add to Basket' button to add the product to the shopping basket
        and remember the price in BasketState."""
        # If product_name is not provided, retrieve it from the page
        if product_name is None:
            product_name = self.get_product_name()

        # Get the product price and store it in BasketState
        price = self.get_product_price()
        BasketState.add_item(product_name, price)

        self.click(ProductPageLocators.ADD_TO_BASKET_BTN)
        logger.info(f"Added product '{product_name}' to basket. Price: {price}")

    @allure.step("Click basket link in header to go to basket page")
    def go_to_basket_from_header(self):
        """
        Click the basket link in the header to navigate to the basket page.
        """

        self.click(ProductPageLocators.BASKET_LINK_IN_HEADER)
        success = self._wait_for_url_contains("/basket")
        assert success, "Failed to navigate to basket page"
        logger.info("Navigated to basket page")

    def get_product_price(self) -> float:
        """Retrieve the product price from the product page."""
        price_text = self.get_text(ProductPageLocators.PRODUCT_PRICE)
        return parse_international_price(price_text)


    def get_product_name(self) -> str:
        """Retrieve the product name from the product page."""
        return self.get_text(ProductPageLocators.PRODUCT_NAME).strip()


class BasketState:
    """
    Simple basket state storage to remember product prices between pages.
    """
    _items = {}  # {product_name: {'price': float, 'quantity': int}}

    @classmethod
    def add_item(cls, product_name: str, price: float, quantity: int = 1):
        """Add item to basket state or update quantity if exists."""
        if product_name in cls._items:
            cls._items[product_name]['quantity'] += quantity
        else:
            cls._items[product_name] = {'price': price, 'quantity': quantity}
        logger.debug(f"Added to basket state: {product_name} - {price} x {quantity}")

    @classmethod
    def get_items(cls) -> dict:
        """Get all items in basket state."""
        return cls._items.copy()

    @classmethod
    def get_item_price(cls, product_name: str) -> float:
        """Get price for specific product from basket state."""
        return cls._items.get(product_name, {}).get('price', 0.0)

    @classmethod
    def get_total_price(cls) -> float:
        """Calculate total price of all items in basket state."""
        return sum(item['price'] * item['quantity'] for item in cls._items.values())

    @classmethod
    def clear(cls):
        """Clear basket state (useful for tests)."""
        cls._items.clear()
        logger.debug("Basket state cleared")


