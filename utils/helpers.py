"""Module description"""

# utils/helpers.py
import re
import logging
from typing import Union

logger = logging.getLogger(__name__)


def parse_international_price(price_text: str) -> float:
    """
    Parse international price text to float.
    Handles different currencies and decimal separators.

    Examples:
    - "9,99 €" -> 9.99
    - "9.99$" -> 9.99
    - "1,000.50 £" -> 1000.50
    - "1.000,50 €" -> 1000.50
    - "£19.99" -> 19.99
    - "€19,99" -> 19.99

    Args:
        price_text: Raw price text from webpage

    Returns:
        Parsed price as float, or 0.0 if parsing fails
    """
    try:
        if not price_text or not price_text.strip():
            logger.warning(f"Empty price text: '{price_text}'")
            return 0.0

        # Remove all non-digit characters except commas, dots, and minus
        cleaned_text = re.sub(r'[^\d,\-.]', '', price_text.strip())

        if not cleaned_text:
            logger.warning(f"Empty price text after cleaning: '{price_text}'")
            return 0.0

        # Handle different decimal separators
        if ',' in cleaned_text and '.' in cleaned_text:
            # Format like "1.000,50" or "1,000.50"
            if cleaned_text.rfind('.') > cleaned_text.rfind(','):
                # "1,000.50" -> thousand_separator=',', decimal_separator='.'
                cleaned_text = cleaned_text.replace(',', '')
            else:
                # "1.000,50" -> thousand_separator='.', decimal_separator=','
                cleaned_text = cleaned_text.replace('.', '').replace(',', '.')
        elif ',' in cleaned_text:
            # Format like "9,99" - comma as decimal separator
            cleaned_text = cleaned_text.replace(',', '.')
        # else: format like "9.99" - dot as decimal separator (no changes needed)

        # Remove any remaining non-digit characters except dot and minus
        cleaned_text = re.sub(r'[^\d.\-]', '', cleaned_text)

        price = float(cleaned_text)
        logger.debug(f"Parsed price: '{price_text}' -> {price}")
        return price

    except ValueError as e:
        logger.error(f"Failed to parse price text '{price_text}'. Cleaned: '{cleaned_text}'. Error: {e}")
        return 0.0


# Можно добавить связанные хелперы для работы с ценами
def format_price(price: float, currency: str = "€") -> str:
    """Format float price back to display format."""
    return f"{price:.2f}{currency}"


def calculate_total(prices: list) -> float:
    """Calculate total from list of prices."""
    return sum(prices)
