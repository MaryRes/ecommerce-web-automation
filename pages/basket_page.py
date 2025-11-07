"""Module description"""

from pages.base_page import BasePage
from pages.locators import BasketPageLocators
import logging

class BasketPage(BasePage):
    """Class representing the basket page of the e-commerce website."""
    def should_contain_product(self, test_product_name):
        """Verify that the basket contains the specified product."""
        product_names_in_basket = self.get_all_texts(BasketPageLocators.BASKET_ITEM_NAME)
        assert test_product_name in product_names_in_basket, (
            f"Product '{test_product_name}' not found in basket. Current products: {product_names_in_basket}"
        )
        logging.info(f"Product '{test_product_name}' is present in the basket.")
