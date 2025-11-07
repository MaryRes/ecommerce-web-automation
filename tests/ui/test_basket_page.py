from conftest import basket_url
from pages.basket_page import BasketPage
from pages.product_page import ProductPage
from pages.locators import BasketPageLocators
import pytest
import allure
import logging
from typing import Tuple

logger = logging.getLogger(__name__)


class TestBasketPage:
    @pytest.mark.parametrize("test_product_name, product_url", [
        ("The shellcoder's handbook",
         "http://selenium1py.pythonanywhere.com/en-gb/catalogue/the-shellcoders-handbook_209/"),
        ("Coders at Work", "http://selenium1py.pythonanywhere.com/fi/catalogue/coders-at-work_207/"),
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
            product_page.add_to_basket()
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