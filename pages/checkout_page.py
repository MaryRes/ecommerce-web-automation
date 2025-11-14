"""Module description"""

from .base_page import BasePage

import logging


logger = logging.getLogger(__name__)

class CheckoutPage(BasePage):
    def should_be_checkout_page(self):
        """Verify that the current page is the checkout page."""
        self.should_be_checkout_url()
        # TODO: Additional checks for checkout page elements should be added here


    def should_be_checkout_url(self):
        """Check that the current URL contains 'checkout'."""
        current_url = self.browser.current_url
        assert "checkout" in current_url, f"Current URL '{current_url}' does not contain 'checkout'"
        logger.info("Checkout page URL verified")
