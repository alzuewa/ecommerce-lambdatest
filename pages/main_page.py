from allure import step
from selene import browser


class MainPage:

    def __init__(self):
        self.url = '/'

        self.success_popup = browser.element('#notification-box-top')
        self.cart_icon = browser.element('.cart-icon')
        self.cart_drawer = browser.element('#cart-total-drawer')
        self.edit_cart_button = browser.element('[data-id="217850"] .btn-primary')
        self.search_input = browser.element('#entry_217822 [name="search"]')

    @step('Enter search query: {product}')
    def search_product(self, product: str):
        self.search_input.type(product).submit()

    @step('Open cart')
    def open_cart(self):
        self.cart_icon.click()

    @step('Click [Edit cart] button')
    def edit_cart(self):
        self.edit_cart_button.click()
