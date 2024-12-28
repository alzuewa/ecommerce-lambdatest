from allure import step
from selene import browser


class ItemPage:
    def __init__(self):
        self.add_to_cart_button = browser.element('[data-id="216842"] .button-cart')
        self.buy_now_button = browser.element('[data-id="216843"] .button-buynow')
        self.item_label = browser.element('.badge-danger')

        self.increase_button = browser.element('#entry_216841 [aria-label="Increase quantity"]')

    @step('Click [Add to cart] button')
    def add_to_cart(self):
        self.add_to_cart_button.click(xoffset=10, yoffset=10)

    @step('Increase item count up to {to_value}')
    def increase_item_count(self, to_value: int):
        for _ in range(to_value - 1):
            self.increase_button.click()
