from selenium.webdriver.common.by import By


class BasePageLocators:
    """Locators common for all pages"""
    HOME_PAGE_LINK = (By.XPATH, "//a[text()='Oscar']")
    LOGIN_LINK = (By.CSS_SELECTOR, "#login_link")
    LOGIN_LINK_INVALID = (By.CSS_SELECTOR, "#login_link_inc")
    USER_ICON = (By.CSS_SELECTOR, "i.icon-user")
    SUCCESS_ALERT = (By.CSS_SELECTOR, ".alert-success")
    ERROR_ALERT = (By.CSS_SELECTOR, ".alert-danger")
    LOGOUT_LINK = (By.CSS_SELECTOR, '#logout_link')
    HEADER = (By.CSS_SELECTOR, '.header')
    BODY = (By.CSS_SELECTOR, 'body')


class BasketPageLocators:
    """Locators for basket/cart page"""
    BASKET_ITEM = (By.CLASS_NAME, "basket-items")
    BASKET_ITEM_NAME = (By.CSS_SELECTOR, ".basket-items h3 a")
    BASKET_ITEM_PRICE = (By.CSS_SELECTOR, ".basket-items .price_color")

    BASKET_ITEM_ROWS = (By.CSS_SELECTOR, "div.basket-items > div.row")
    PRODUCT_NAME_IN_BASKET = (By.CSS_SELECTOR, "div.col-sm-4 h3 a")
    PRODUCT_PRICE_PER_UNIT = (By.CSS_SELECTOR, "div.col-sm-1 p.price_color")
    PRODUCT_TOTAL_PRICE = (By.CSS_SELECTOR, "div.col-sm-2 p.price_color")
    PRODUCT_QUANTITY_INPUT = (By.CSS_SELECTOR, "input[name*='quantity']")

    PRODUCT_ROW_BY_NAME = lambda name: (By.XPATH,
    f"//div[contains(@class, 'basket-items')]//a[contains(., '{name}')]/ancestor::div[@class='row']")
    EMPTY_BASKET_MESSAGE = (By.XPATH, "//div[@id='content_inner']//p[contains(text(), 'Your basket is empty')]")
    CHECKOUT_BUTTON = (By.CSS_SELECTOR, 'a.btn-primary[href*="checkout"]')

class MainPageLocators:
    """Locators for main page"""
    BASKET_LINK_IN_HEADER = (By.CSS_SELECTOR, 'div[class*="basket-mini"] > span.btn-group > a[href*="basket"]')
    CATALOG_LINK_IN_HEADER = (By.XPATH, '//ul[@class="dropdown-menu"]//a[contains(@href, "catalogue") and text()="All products"]')

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

    # message after incorrect registration
    REGISTER_INCORRECT_MESSAGE = (By.CSS_SELECTOR, '.alert-danger')
    # Password strength indicator
    WEAK_PASSWORD_INDICATOR = (By.XPATH, "//div[input[@id='id_registration-password2']]//span[@class='error-block']")

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
    PRODUCT_PRICE = (By.CSS_SELECTOR, ".product_main .price_color")

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


class CatalogPageLocators:
    """Locators for catalog page"""
    SIDE_CATEGORIES = (By.CSS_SELECTOR, '.side_categories')
    PRODUCT_LIST = (By.CSS_SELECTOR, 'ol.row')
    ALL_PRODUCT_CARDS = (By.CSS_SELECTOR, 'article.product_pod')
    ALL_PRODUCT_LINKS = (By.CSS_SELECTOR, 'article.product_pod a')
    ALL_ADD_TO_BASKET_BUTTONS = (By.CSS_SELECTOR, 'article.product_pod button.btn-add-to-basket')
    PRODUCT_TITLE_IN_CARD = (By.CSS_SELECTOR, 'h3 a')
    # Navigation
    NEXT_PAGE_BUTTON = (By.CSS_SELECTOR, 'li.next a')