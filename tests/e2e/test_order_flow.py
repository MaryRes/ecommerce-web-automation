"""Module description"""
# TODO screenshots on failure!!!


import pytest

from conftest import catalog_url
from pages.main_page import MainPage
from pages.catalog_page import CatalogPage
from pages.product_page import ProductPage
from pages.basket_page import BasketPage
from pages.checkout_page import CheckoutPage
from utils.api_client import ApiClient
from config.settings import CATALOG_URL


@pytest.mark.skip(reason="🚧 E2E TESTS UNDER DEVELOPMENT - Page Objects not implemented")
@pytest.mark.e2e
class TestE2EOrderFlow:
    """
    End-to-End tests for main user scenarios:
    - Guest completes an order
    - Logged-in user uses a saved address
    - Order fails when product is out of stock
    """

    @pytest.mark.skip(reason="Page Objects not implemented yet - E2E development in progress")
    @pytest.mark.critical
    @pytest.mark.parametrize("test_product_name", ["The shellcoder's handbook", "Coders at Work"])
    def test_guest_order_flow(self, browser, main_page_url, test_product_name):
        """
        E2E: Guest user can add a product to basket and complete checkout.
        Steps:
            1. Open main page
            2. Navigate to catalog
            3. Select a product
            4. Add the product to the basket
            5. Verify product and total price in basket
            6. Proceed to checkout
            7. Verify successful order confirmation
        """
        main_page = MainPage(browser, main_page_url)
        catalog_page = CatalogPage(browser, catalog_url)
        product_page = ProductPage(browser)
        basket_page = BasketPage(browser)
        checkout_page = CheckoutPage(browser)

        main_page.open()
        main_page.go_to_catalog()
        catalog_page.select_product(test_product_name)
        product_page.add_to_basket()  # click Add to basket
        product_page.go_to_basket_from_header()  # navigate to basket page
        basket_page.should_contain_product(test_product_name)  # TODO: verify product is in basket
        basket_page.should_match_price("Test Product")  # TODO: verify correct price
        basket_page.proceed_to_checkout()  # TODO: click "Proceed to checkout"
        checkout_page.should_display_confirmation()  # TODO: verify confirmation page is shown

    @pytest.mark.skip(reason="Page Objects not implemented yet - E2E development in progress")
    @pytest.mark.critical
    def test_logged_in_checkout_with_saved_address(self, browser, user):
        """
        E2E: Logged-in user can place an order using a saved address.
        Steps:
            1. Log in to account
            2. Ensure saved shipping address exists
            3. Add product to basket
            4. Proceed to checkout
            5. Verify saved address is pre-filled
            6. Complete the order
        """
        account_page = user.account_page
        catalog_page = CatalogPage(browser)
        product_page = ProductPage(browser)
        basket_page = BasketPage(browser)
        checkout_page = CheckoutPage(browser)

        account_page.login("test_user", "secure_password")  # TODO: implement login()
        account_page.ensure_saved_address_exists()  # TODO: verify or create address
        catalog_page.select_product("Test Product")  # TODO: select product
        product_page.add_to_basket()  # TODO: add to basket
        basket_page.proceed_to_checkout()  # TODO: proceed to checkout
        checkout_page.should_display_saved_address()  # TODO: verify saved address is shown
        checkout_page.place_order()  # TODO: place the order
        checkout_page.should_display_confirmation()  # TODO: verify confirmation page


    @pytest.mark.skip(reason="Page Objects not implemented yet - E2E development in progress")
    @pytest.mark.negative
    def test_out_of_stock_prevents_order(self, browser):
        """
        E2E (Negative): User cannot place an order when product is out of stock.
        Steps:
            1. Set stock = 0 via API
            2. Open product page
            3. Verify "Add to basket" button is disabled
            4. Attempt checkout — ensure order is not completed
        """
        api = ApiClient()
        product_page = ProductPage(browser)
        basket_page = BasketPage(browser)
        checkout_page = CheckoutPage(browser)

        api.set_stock("SKU-12345", 0)  # TODO: implement API method to modify stock
        product_page.open("SKU-12345")  # TODO: open product by SKU
        product_page.should_have_disabled_add_button()  # TODO: verify button is disabled
        basket_page.proceed_to_checkout()  # TODO: try to proceed to checkout
        checkout_page.should_fail_due_to_out_of_stock()  # TODO: verify failure message
