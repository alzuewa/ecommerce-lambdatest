from allure import step
from selene import browser
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait


class CartPage:
    def __init__(self):
        self.url = '/index.php?route=checkout/cart'

        self.cart_empty_pic = browser.element('.fa-exclamation-triangle')

        # item summary table locators
        self.total_item_price = browser.element('//*[@class="table-responsive"]/table/tbody//td[6]')
        self.item_quantity = browser.element('//*[@class="table-responsive"]/table/tbody//td[4]//input')
        self.update_quantity_icon = browser.element('.fa-sync-alt')
        self.delete_item_icon = browser.element('.fa-times-circle')

        # coupon section locators
        self.add_coupon_button = browser.element('[data-target="#collapse-coupon"]')
        self.coupon_field = browser.element('#input-coupon')
        self.apply_coupon_button = browser.element('//*[text()="Apply Coupon"]')
        self.invalid_coupon_banner = browser.element('#collapse-coupon .alert-danger')
        self.close_coupon_banner = browser.element('#collapse-coupon .close')

        # voucher section locators
        self.add_voucher_button = browser.element('[data-target="#collapse-voucher"]')
        self.voucher_field = browser.element('#input-voucher')
        self.apply_voucher_button = browser.element('[value="Apply Gift Certificate"]')
        self.invalid_voucher_banner = browser.element('#collapse-voucher .alert-danger')
        self.close_voucher_banner = browser.element('#collapse-voucher .close')

    @step('Open cart page')
    def open_cart_page(self):
        browser.open(self.url)

    @step('Clear product count field')
    def clear_product_count_field(self):
        self.item_quantity.clear()

    @step('Update product count to value: {value}')
    def update_product_count(self, value: str):
        self.item_quantity.type(value)
        self.update_quantity_icon.click()

    @step('Delete the only item from cart')
    def delete_the_only_item(self):
        self.delete_item_icon.click()

    @step('Apply coupon with code: {code}')
    def apply_coupon(self, code: str):
        self.add_coupon_button.click()
        self.coupon_field.type(code)
        self.apply_coupon_button.click()

    @step('Apply voucher with code: {code}')
    def apply_voucher(self, code: str):
        self.add_voucher_button.click()
        self.voucher_field.type(code)
        self.apply_voucher_button.click()

    @step('Close coupon banner')
    def close_coupon_banner(self):
        self.close_coupon_banner.click()

    @step('Close voucher banner')
    def close_voucher_banner(self):
        self.close_voucher_banner.click()

    @step('Search link for product: {product_name}')
    def get_product_link(self, product_name: str):
        cart_product = By.LINK_TEXT, product_name
        return WebDriverWait(browser.driver, timeout=6).until(ec.presence_of_element_located(cart_product))
