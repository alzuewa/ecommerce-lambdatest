import allure
from allure_commons.types import Severity
from selene import be, have

from data.product_strings import ProductName
from pages.application import app


@allure.epic('Cart')
@allure.story('Add product to cart')
@allure.feature('Add product from search page')
@allure.title('[Add to cart] Item available in stock')
@allure.tag('Regression')
@allure.severity(Severity.CRITICAL)
def test_add_available_product(driver_with_cookies):
    product_name = ProductName.IPOD_NANO
    increased_count = 2

    app.main_page.open_main_page()

    app.main_page.search_product(product=product_name)
    app.goods_page.choose_item(item_name=product_name)
    app.item_page.increase_item_count(to_value=increased_count)
    app.item_page.add_to_cart()

    with allure.step('Assert success toast shown on product added'):
        app.main_page.success_popup.should(be.visible)

    with allure.step('Wait until success toast disappears'):
        app.main_page.success_popup.with_(timeout=12).should(be.not_.visible)

    app.main_page.open_cart()

    with allure.step('Assert cart drawer opened on click by cart icon'):
        app.main_page.cart_drawer.should(be.visible)

    app.main_page.edit_cart()

    with allure.step('Assert added product present in cart'):
        assert app.cart_page.get_product_link(product_name=product_name)


@allure.epic('Cart')
@allure.story('Add product to cart')
@allure.feature('Add product from search page')
@allure.title('[Add to cart] Item unavailable in stock')
@allure.tag('Regression')
@allure.severity(Severity.CRITICAL)
def test_add_unavailable_product(driver_with_cookies):
    product_name = ProductName.PALM_TREO_PRO
    app.main_page.open_main_page()

    app.main_page.search_product(product=product_name)
    app.goods_page.choose_item(item_name=product_name)

    with allure.step('Assert unavailable product has label [Out Of Stock]'):
        app.item_page.item_label.should(be.visible)
        app.item_page.item_label.should(have.exact_text('Out Of Stock'))

    with allure.step('Assert [Add to cart] button disabled'):
        assert app.item_page.add_to_cart_button.should(be.disabled)
    with allure.step('Assert [Buy now] button disabled'):
        assert app.item_page.buy_now_button.should(be.disabled)
