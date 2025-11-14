"""Module description"""

"""Basket Page Object Model"""

from pages.base_page import BasePage
from pages.locators import BasketPageLocators
from utils.helpers import parse_international_price
import logging
import re
import allure

from pages.product_page import BasketState

logger = logging.getLogger(__name__)


class BasketPage(BasePage):
    """Class representing the basket page of the e-commerce website."""

    def __init__(self, browser, url):
        super().__init__(browser, url)

    @allure.step("Verify basket contains product (enhanced): {test_product_name}")
    def should_contain_product(self, test_product_name):
        """Enhanced version using new parsing functions."""
        basket_items = self.get_basket_items_dict()
        assert test_product_name in basket_items, (
            f"Product '{test_product_name}' not found in basket. "
            f"Current products: {list(basket_items.keys())}"
        )
        logger.info(f"Product '{test_product_name}' is present in the basket.")

    @allure.step("Verify product price matches expected (enhanced): {test_product_name}")
    def should_match_price(self, test_product_name: str):
        """Enhanced version using new parsing functions."""
        expected_price = self.get_expected_price(test_product_name)
        product_data = self.get_product_data(test_product_name)

        if not product_data:
            raise AssertionError(f"Product '{test_product_name}' not found in basket")

        actual_price = product_data['unit_price']
        assert abs(actual_price - expected_price) <= 0.01, (
            f"Price mismatch for '{test_product_name}'. "
            f"Expected: {expected_price:.2f}, Actual: {actual_price:.2f}"
        )
        logger.info(f"Price for '{test_product_name}' matches the expected price: {expected_price:.2f}")

    @allure.step("Get expected price for product: {product_name}")
    def get_expected_price(self, product_name: str) -> float:
        """Get expected price for product from BasketState."""
        price = BasketState.get_item_price(product_name)
        logger.debug(f"Expected price for '{product_name}': {price}")
        return price

    @allure.step("Get all expected items from BasketState")
    def get_expected_items(self) -> dict:
        """Get all expected items from BasketState."""
        items = BasketState.get_items()
        logger.debug(f"Expected items from BasketState: {len(items)} items")
        return items


    @allure.step("Get actual product price: {product_name}")
    def get_actual_product_price(self, product_name: str) -> float:
        """Retrieve the actual price of the specified product from the basket page."""
        product_elements = self.wait_for_presence_of_all(BasketPageLocators.BASKET_ITEM)
        logger.debug(f"Found {len(product_elements)} product elements in basket")

        for element in product_elements:
            name = element.find_element(*BasketPageLocators.BASKET_ITEM_NAME).text
            if name == product_name:
                price_text = element.find_element(*BasketPageLocators.BASKET_ITEM_PRICE).text
                price = parse_international_price(price_text)
                logger.info(f"Actual price for '{product_name}': {price} (from text: '{price_text}')")
                return price

        raise AssertionError(f"Product '{product_name}' not found in basket for price retrieval.")

    # === NEW BASKET PARSING FUNCTIONS ===

    @allure.step("Get all basket items as list of dictionaries")
    def get_all_basket_items(self) -> list[dict]:
        """
        Get all items from basket as list of dictionaries.
        Returns: [{'name': str, 'unit_price': float, 'quantity': int, 'total_price': float}]
        """
        items = []
        item_rows = self.find_elements(BasketPageLocators.BASKET_ITEM_ROWS)

        for row in item_rows:
            item_data = self._parse_basket_row(row)
            if item_data:
                items.append(item_data)

        logger.info(f"Found {len(items)} items in basket")
        return items

    def _parse_basket_row(self, row_element) -> dict:
        """Parse single basket row into dictionary."""
        try:
            # Product name
            name_element = row_element.find_element(*BasketPageLocators.PRODUCT_NAME_IN_BASKET)
            name = name_element.text.strip()

            # Unit price
            unit_price_element = row_element.find_element(*BasketPageLocators.PRODUCT_PRICE_PER_UNIT)
            unit_price = parse_international_price(unit_price_element.text)

            # Total price
            total_price_element = row_element.find_element(*BasketPageLocators.PRODUCT_TOTAL_PRICE)
            total_price = parse_international_price(total_price_element.text)

            # Quantity
            quantity_element = row_element.find_element(*BasketPageLocators.PRODUCT_QUANTITY_INPUT)
            quantity = int(quantity_element.get_attribute('value'))

            item_data = {
                'name': name,
                'unit_price': unit_price,
                'quantity': quantity,
                'total_price': total_price
            }

            logger.debug(f"Parsed basket row: {item_data}")
            return item_data

        except Exception as e:
            logger.warning(f"Failed to parse basket row: {e}")
            return None

    @allure.step("Get basket items as dictionary")
    def get_basket_items_dict(self) -> dict:
        """
        Get all items from basket as dictionary keyed by product name.
        Returns: {product_name: {'unit_price': float, 'quantity': int, 'total_price': float}}
        """
        items_list = self.get_all_basket_items()
        items_dict = {item['name']: {k: v for k, v in item.items() if k != 'name'}
                      for item in items_list}
        logger.debug(f"Basket items as dictionary: {len(items_dict)} products")
        return items_dict


    @allure.step("Get product data: {product_name}")
    def get_product_data(self, product_name: str) -> dict:
        """
        Get specific product data from basket by name.
        """
        try:
            all_items = self.get_all_basket_items()
            for item in all_items:
                if item['name'] == product_name:
                    logger.debug(f"Product data for '{product_name}': {item}")
                    return item

            logger.error(f"Product '{product_name}' not found in basket")
            return None

        except Exception as e:
            logger.error(f"Error getting product data for '{product_name}': {e}")
            return None


    # === VERIFICATION FUNCTIONS ===

    @allure.step("Verify all product prices match expected prices")
    def verify_all_prices_match_expected(self):
        """Verify all product prices in basket match expected prices from BasketState."""
        expected_items = BasketState.get_items()
        basket_items = self.get_basket_items_dict()

        errors = []
        for product_name, expected_data in expected_items.items():
            if product_name not in basket_items:
                errors.append(f"Product '{product_name}' not found in basket")
                continue

            expected_price = expected_data['price']
            actual_unit_price = basket_items[product_name]['unit_price']

            if abs(actual_unit_price - expected_price) > 0.01:  # Allow small floating point differences
                errors.append(
                    f"Price mismatch for '{product_name}'. "
                    f"Expected: {expected_price:.2f}, Actual: {actual_unit_price:.2f}"
                )

        if errors:
            error_message = "\n".join(errors)
            logger.error(f"Price verification failed:\n{error_message}")
            raise AssertionError(error_message)

        logger.info("All product prices match expected prices")

    @allure.step("Verify quantities match expected")
    def verify_quantities_match_expected(self):
        """Verify quantities in basket match expected quantities from BasketState."""
        expected_items = BasketState.get_items()
        basket_items = self.get_basket_items_dict()

        errors = []
        for product_name, expected_data in expected_items.items():
            if product_name not in basket_items:
                errors.append(f"Product '{product_name}' not found in basket")
                continue

            expected_quantity = expected_data['quantity']
            actual_quantity = basket_items[product_name]['quantity']

            if actual_quantity != expected_quantity:
                errors.append(
                    f"Quantity mismatch for '{product_name}'. "
                    f"Expected: {expected_quantity}, Actual: {actual_quantity}"
                )

        if errors:
            error_message = "\n".join(errors)
            logger.error(f"Quantity verification failed:\n{error_message}")
            raise AssertionError(error_message)

        logger.info("All quantities match expected")


    @allure.step("Verify total prices are calculated correctly")
    def verify_total_prices_calculated_correctly(self):
        """Verify that total price = unit_price * quantity for each item."""
        basket_items = self.get_all_basket_items()

        errors = []
        for item in basket_items:
            calculated_total = item['unit_price'] * item['quantity']
            actual_total = item['total_price']

            # Allow small floating point differences
            if abs(calculated_total - actual_total) > 0.01:
                errors.append(
                    f"Total price calculation error for '{item['name']}'. "
                    f"Expected: {calculated_total:.2f}, Actual: {actual_total:.2f}"
                )

        if errors:
            error_message = "\n".join(errors)
            logger.error(f"Total price verification failed:\n{error_message}")
            raise AssertionError(error_message)

        logger.info("All total prices calculated correctly")


    @allure.step("Complete basket state verification")
    def verify_complete_basket_state(self):
        """Complete verification of basket state - prices, quantities and calculations."""
        self.verify_all_prices_match_expected()
        self.verify_quantities_match_expected()
        self.verify_total_prices_calculated_correctly()
        logger.info("Complete basket state verification passed")

    @allure.step("Verify basket is empty")
    def should_be_empty(self):
        """Verify that basket is empty - no items present."""
        assert self.is_not_element_present(BasketPageLocators.BASKET_ITEM_ROWS), \
            "Basket should be empty but items were found"

        # Additional check for empty basket message
        if self.is_element_present(BasketPageLocators.EMPTY_BASKET_MESSAGE):
            logger.info("Empty basket message found")
        else:
            logger.warning("Empty basket message not found, but no items present")

        logger.info("Basket is empty - verified")


    @allure.step("Proceed to checkout")
    def proceed_to_checkout(self):
        """Click the 'Proceed to Checkout' button to go to checkout page."""
        self.click(BasketPageLocators.CHECKOUT_BUTTON)
        success = self._wait_for_url_contains("/checkout")
        assert success, "Failed to navigate to checkout page"
        logger.info("Navigated to checkout page")


    def should_be_checkout_button(self):
        """Verify that the 'Proceed to Checkout' button is present."""
        assert self.is_element_present(BasketPageLocators.CHECKOUT_BUTTON), (
            "'Proceed to Checkout' button is not present on the basket page"
        )
        logger.info("'Proceed to Checkout' button is present on the basket page")



