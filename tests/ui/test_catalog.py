"""Module description"""
from pages.catalog_page import CatalogPage
from pages.main_page import MainPage
from pages.product_page import ProductPage
import pytest


class TestCatalogPage:

    def test_navigate_from_main_page_to_catalog(self, browser, main_page_url):
        main_page = MainPage(browser, main_page_url)
        main_page.open()
        main_page.go_to_catalog()

        catalog_page = CatalogPage(browser, browser.current_url)
        catalog_page.should_be_catalog_page()

    @pytest.mark.parametrize("product_name", ["The shellcoder's handbook", "Coders at Work"])
    def test_select_product(self, browser, catalog_url, product_name):
        catalog_page = CatalogPage(browser, catalog_url)
        catalog_page.open()

        catalog_page.should_be_catalog_page()

        catalog_page.select_product(product_name)

        product_page = ProductPage(browser, browser.current_url)
        product_page.should_be_product_page(product_name)



