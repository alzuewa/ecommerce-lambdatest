import allure
from selene import be, browser, have
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from data.product_constants import ProductName
from pages.application import app


def test_add_available_product(driver):
    product_name = ProductName.IPOD_NANO
    increased_count = 2

    with allure.step('Open Main page'):
        browser.open(app.main_page.url)

    app.main_page.search_product(product=product_name)
    app.goods_page.choose_item(item_name=product_name)
    app.item_page.increase_item_count(to_value=increased_count)
    app.item_page.add_to_cart()

    with allure.step('Assert success popup shown on product added'):
        app.main_page.success_popup.should(be.visible)

    app.main_page.open_cart()

    with allure.step('Assert cart drawer opened on click by cart icon'):
        app.main_page.cart_drawer.should(be.visible)

    app.main_page.edit_cart()
    cart_product = By.LINK_TEXT, product_name

    with allure.step('Assert added product present in cart'):
        assert WebDriverWait(driver.driver, timeout=6).until(EC.presence_of_element_located(cart_product))


def test_add_unavailable_product(driver):
    product_name = ProductName.PALM_TREO_PRO
    with allure.step('Open Main page'):
        browser.open(app.main_page.url)

    app.main_page.search_product(product=product_name)
    app.goods_page.choose_item(item_name=product_name)

    with allure.step('Assert unavailable product has label [Out Of Stock]'):
        app.item_page.item_label.should(be.visible)
        app.item_page.item_label.should(have.exact_text('Out Of Stock'))

    with allure.step('Assert [Add to cart] button disabled'):
        assert app.item_page.add_to_cart_button.should(be.disabled)
    with allure.step('Assert [Buy now] button disabled'):
        assert app.item_page.buy_now_button.should(be.disabled)
