from conftest import basket_url
from pages.basket_page import BasketPage
from pages.product_page import ProductPage, BasketState
import pytest
import allure
import logging

logger = logging.getLogger(__name__)


class TestBasketPage:

    @pytest.fixture(autouse=True)
    def setup(self, browser):
        """Setup before each test - clear basket state."""
        BasketState.clear()
        yield
        # Optional: cleanup after test if needed

    @pytest.mark.parametrize("test_product_name, product_url", [
        ("The shellcoder's handbook",
         "http://selenium1py.pythonanywhere.com/en-gb/catalogue/the-shellcoders-handbook_209/"),
        ("Coders at Work", "http://selenium1py.pythonanywhere.com/en-gb/catalogue/coders-at-work_207/"),
    ])
    @allure.title("Verify that basket contains added product: {test_product_name}")
    @allure.feature("Basket Functionality")
    @allure.story("Add product to basket")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_basket_should_contain_product(
            self,
            browser: object,
            basket_url: str,
            product_url: str,
            test_product_name: str
    ) -> None:
        """
        Test that verifies a product added to the basket is actually present in the basket.

        This test performs the following steps:
        1. Opens the product page
        2. Adds the product to the basket
        3. Opens the basket page
        4. Verifies the product is present in the basket

        Args:
            browser: Selenium WebDriver instance
            basket_url: URL of the basket page
            product_url: URL of the product page to test
            test_product_name: Expected name of the product to verify in basket

        Raises:
            AssertionError: If the product is not found in the basket
        """
        logger.info("Starting test: test_basket_should_contain_product")
        logger.info(f"Testing product: {test_product_name}")
        logger.info(f"Product URL: {product_url}")
        logger.info(f"Basket URL: {basket_url}")

        with allure.step("Open product page and add product to basket"):
            logger.info(f"Opening product page: {product_url}")
            product_page = ProductPage(browser, product_url)
            product_page.open()

            logger.info(f"Adding product '{test_product_name}' to basket")
            product_page.add_to_basket(test_product_name)
            logger.info("Product successfully added to basket")

        with allure.step("Open basket page and verify product presence"):
            logger.info(f"Opening basket page: {basket_url}")
            basket_page = BasketPage(browser, basket_url)
            basket_page.open()
            logger.info("Basket page opened successfully")

            logger.info(f"Verifying that basket contains product: {test_product_name}")
            basket_page.should_contain_product(test_product_name)
            logger.info(f"Product '{test_product_name}' successfully verified in basket")

        logger.info("Test test_basket_should_contain_product completed successfully")

    @pytest.mark.parametrize("test_product_name, product_url", [
        ("The shellcoder's handbook",
         "http://selenium1py.pythonanywhere.com/en-gb/catalogue/the-shellcoders-handbook_209/"),
        ("Coders at Work", "http://selenium1py.pythonanywhere.com/en-gb/catalogue/coders-at-work_207/"),
    ])
    @allure.title("Verify product price matches between product page and basket: {test_product_name}")
    @allure.feature("Basket Functionality")
    @allure.story("Price verification")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_should_match_price(
            self,
            browser: object,
            basket_url: str,
            product_url: str,
            test_product_name: str
    ) -> None:
        """
        Test that verifies the product price in basket matches the price from product page.

        This test performs the following steps:
        1. Opens the product page
        2. Adds the product to the basket (price is automatically saved in BasketState)
        3. Opens the basket page
        4. Verifies the price matches expected price from BasketState

        Args:
            browser: Selenium WebDriver instance
            basket_url: URL of the basket page
            product_url: URL of the product page to test
            test_product_name: Name of the product to verify price for
        """
        logger.info("Starting test: test_should_match_price")
        logger.info(f"Testing product: {test_product_name}")

        with allure.step("Open product page and add product to basket"):
            product_page = ProductPage(browser, product_url)
            product_page.open()

            # Get product price before adding to basket for logging
            product_price = product_page.get_product_price()
            logger.info(f"Product price on product page: {product_price}")

            product_page.add_to_basket(test_product_name)
            logger.info(f"Added '{test_product_name}' to basket. Expected price: {product_price}")

        with allure.step("Open basket page and verify price"):
            basket_page = BasketPage(browser, basket_url)
            basket_page.open()

            logger.info(f"Verifying price for '{test_product_name}'")
            basket_page.should_match_price(test_product_name)
            logger.info(f"Price verification passed for '{test_product_name}'")

        logger.info("Test test_should_match_price completed successfully")


    @pytest.mark.parametrize("test_product_name, product_url", [
        ("The shellcoder's handbook",
         "http://selenium1py.pythonanywhere.com/en-gb/catalogue/the-shellcoders-handbook_209/"),
        ("Coders at Work", "http://selenium1py.pythonanywhere.com/en-gb/catalogue/coders-at-work_207/"),
    ])
    @allure.title("Verify multiple products can be added to basket: {test_product_name}")
    @allure.feature("Basket Functionality")
    @allure.story("Multiple products")
    @allure.severity(allure.severity_level.NORMAL)
    def test_multiple_products_basket(
            self,
            browser: object,
            basket_url: str,
            product_url: str,
            test_product_name: str
    ) -> None:
        """
        Test adding multiple quantities of the same product to basket.
        """
        logger.info("Starting test: test_multiple_products_basket")

        with allure.step("Add multiple quantities of the same product"):
            product_page = ProductPage(browser, product_url)
            product_page.open()

            # Add product multiple times
            for i in range(3):
                product_page.add_to_basket(test_product_name)
                logger.info(f"Added product #{i + 1} to basket")

            expected_quantity = 3
            logger.info(f"Expected total quantity: {expected_quantity}")

        with allure.step("Verify basket contains correct quantity"):
            basket_page = BasketPage(browser, basket_url)
            basket_page.open()

            # Use enhanced verification
            basket_page.verify_quantities_match_expected()
            logger.info("Quantity verification passed")

        logger.info("Test test_multiple_products_basket completed successfully")

    @pytest.mark.parametrize("product1_name, product1_url, product2_name, product2_url", [
        ("The shellcoder's handbook",
         "http://selenium1py.pythonanywhere.com/en-gb/catalogue/the-shellcoders-handbook_209/",
         "Coders at Work",
         "http://selenium1py.pythonanywhere.com/en-gb/catalogue/coders-at-work_207/"),
    ])
    @allure.title("Verify multiple different products in basket")
    @allure.feature("Basket Functionality")
    @allure.story("Multiple different products")
    @allure.severity(allure.severity_level.NORMAL)
    def test_multiple_different_products_basket(
            self,
            browser: object,
            basket_url: str,
            product1_name: str,
            product1_url: str,
            product2_name: str,
            product2_url: str
    ) -> None:
        """
        Test adding multiple different products to basket and verify all prices.
        """
        logger.info("Starting test: test_multiple_different_products_basket")

        with allure.step("Add first product to basket"):
            product1_page = ProductPage(browser, product1_url)
            product1_page.open()
            product1_page.add_to_basket(product1_name)
            logger.info(f"Added first product: {product1_name}")

        with allure.step("Add second product to basket"):
            product2_page = ProductPage(browser, product2_url)
            product2_page.open()
            product2_page.add_to_basket(product2_name)
            logger.info(f"Added second product: {product2_name}")

        with allure.step("Verify all products and prices in basket"):
            basket_page = BasketPage(browser, basket_url)
            basket_page.open()

            # Verify both products are present
            basket_page.should_contain_product(product1_name)
            basket_page.should_contain_product(product2_name)
            logger.info("Both products found in basket")

            # Verify all prices match expected
            basket_page.verify_all_prices_match_expected()
            logger.info("All prices match expected values")

            # Verify quantities
            basket_page.verify_quantities_match_expected()
            logger.info("All quantities match expected")

        logger.info("Test test_multiple_different_products_basket completed successfully")

    @pytest.mark.parametrize("test_product_name, product_url", [
        ("The shellcoder's handbook",
         "http://selenium1py.pythonanywhere.com/en-gb/catalogue/the-shellcoders-handbook_209/"),
    ])
    @allure.title("Complete basket state verification: {test_product_name}")
    @allure.feature("Basket Functionality")
    @allure.story("Complete verification")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_complete_basket_verification(
            self,
            browser: object,
            basket_url: str,
            product_url: str,
            test_product_name: str
    ) -> None:
        """
        Complete verification of basket state including prices, quantities and calculations.
        """
        logger.info("Starting test: test_complete_basket_verification")

        with allure.step("Add products to basket"):
            product_page = ProductPage(browser, product_url)
            product_page.open()

            # Add multiple quantities
            for i in range(2):
                product_page.add_to_basket(test_product_name)
            logger.info(f"Added 2 quantities of '{test_product_name}' to basket")

        with allure.step("Perform complete basket verification"):
            basket_page = BasketPage(browser, basket_url)
            basket_page.open()

            # Single method that verifies everything
            basket_page.verify_complete_basket_state()
            logger.info("Complete basket state verification passed")

        logger.info("Test test_complete_basket_verification completed successfully")


    @allure.title("Verify empty basket behavior")
    @allure.feature("Basket Functionality")
    @allure.story("Empty basket")
    @allure.severity(allure.severity_level.NORMAL)
    def test_empty_basket(
            self,
            browser: object,
            basket_url: str
    ) -> None:
        """
        Test behavior when basket is empty.
        """
        logger.info("Starting test: test_empty_basket")

        with allure.step("Open empty basket"):
            basket_page = BasketPage(browser, basket_url)
            basket_page.open()

            logger.info("Verifying empty basket message is displayed")
            basket_page.should_be_empty()
            logger.info("Empty basket message verified successfully")