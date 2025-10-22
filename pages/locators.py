from selenium.webdriver.common.by import By


class BasePageLocators:
    """Locators common for all pages"""
    LOGIN_LINK = (By.CSS_SELECTOR, "#login_link")
    LOGIN_LINK_INVALID = (By.CSS_SELECTOR, "#login_link_inc")
    USER_ICON = (By.CSS_SELECTOR, "i.icon-user")
    SUCCESS_ALERT = (By.CSS_SELECTOR, ".alert-success")
    ERROR_ALERT = (By.CSS_SELECTOR, ".alert-danger")


class BasketPageLocators:
    """Locators for basket/cart page"""
    BASKET_CONTENT = (By.CSS_SELECTOR, 'div[id="content_inner"]')
    BASKET_ITEMS = (By.CSS_SELECTOR, 'div[id="content_inner"] form')


class MainPageLocators:
    """Locators for main page"""
    BASKET_LINK_IN_HEADER = (By.CSS_SELECTOR, 'div[class*="basket-mini"] > span.btn-group > a[href*="basket"]')


class LoginPageLocators:
    """Locators for login/registration page"""
    LOGIN_FORM = (By.CSS_SELECTOR, 'form[id*="login"]')
    REGISTER_FORM = (By.CSS_SELECTOR, 'form[id*="register"]')

    # Login form fields
    LOGIN_EMAIL_FIELD = (By.CSS_SELECTOR, 'input[name="login-username"]')
    LOGIN_PASSWORD_FIELD = (By.CSS_SELECTOR, 'input[name="login-password"]')
    LOGIN_SUBMIT_BUTTON = (By.CSS_SELECTOR, 'button[name="login_submit"]')
    # success message after login
    LOGIN_SUCCESS = (By.CSS_SELECTOR, ".alert-success")
    # message after incorrect login
    LOGIN_INCORRECT_MESSAGE = (By.CSS_SELECTOR, '[for="id_login-password"]')

    # Registration form fields
    REGISTER_EMAIL_FIELD = (By.CSS_SELECTOR, 'input[name="registration-email"]')
    REGISTER_PASSWORD_FIELD = (By.CSS_SELECTOR, 'input[name="registration-password1"]')
    REGISTER_CONFIRM_PASSWORD_FIELD = (By.CSS_SELECTOR, 'input[name="registration-password2"]')
    REGISTER_SUBMIT_BUTTON = (By.CSS_SELECTOR, 'button[name="registration_submit"]')

    # Additional links
    FORGOT_PASSWORD_LINK = (By.CSS_SELECTOR, 'a[href*="password-reset"]')

    # Form header
    LOGIN_HEADER = (By.CSS_SELECTOR, 'h1')

    # success message after registration
    REGISTRATION_SUCCESS = (By.CSS_SELECTOR, ".alert-success")





class ProductPageLocators:
    """Locators for product page"""

    # Action buttons
    ADD_TO_BASKET_BTN = (By.CSS_SELECTOR, '[class*="btn-add-to-basket"]')

    # Navigation
    BASKET_LINK_IN_HEADER = (By.CSS_SELECTOR, 'div[class*="basket-mini"] > span.btn-group > a[href*="basket"]')

    # Product info (same before/after adding to basket)
    PRODUCT_NAME = (By.CSS_SELECTOR, '[class*=product_main] h1')
    PRODUCT_PRICE = (By.CSS_SELECTOR, '[class*=price_color]')

    # Messages and notifications
    BASKET_MESSAGE_BOX = (By.CSS_SELECTOR, '[id="messages"]')
    MESSAGE_STRONG_TEXT = (By.CSS_SELECTOR, '[class*="alertinner"] strong')
    MESSAGE_TEXT = (By.CSS_SELECTOR, '[class*="alertinner"]')

    # Breadcrumbs
    BREADCRUMB_LAST_ITEM = (By.XPATH, '//ul[@class="breadcrumb"]//li[last()]')

    # Price elements
    PRODUCT_PRICE_INCLUDING_TAX = (By.XPATH, "//th[text()='Price (incl. tax)']/..//td")
    BASKET_TOTAL_NAVBAR = (By.XPATH, "//a[contains(@href, '/basket') and contains(., 'Total:')]")
    BASKET_TOTAL_MESSAGE = (By.XPATH, "//div[@id='messages']//p[contains(., 'basket total')]//strong")

    # Validation groups
    PRODUCT_TITLE_ELEMENTS = [PRODUCT_NAME, MESSAGE_STRONG_TEXT, BREADCRUMB_LAST_ITEM]
    ITEM_PRICE_ELEMENTS = [PRODUCT_PRICE, PRODUCT_PRICE_INCLUDING_TAX]
    BASKET_TOTAL_ELEMENTS = [BASKET_TOTAL_NAVBAR, BASKET_TOTAL_MESSAGE]