import allure
from allure_commons.types import Severity
from selene import have, be

from data.data_setup import create_product_request_data
from data.models import Product
from data.product_strings import AvailableProductId, ProductName
from pages.application import app
from utils.price_helpers import get_price_repr, get_total_cart_price


@allure.epic('Cart')
@allure.story('Edit cart')
@allure.feature('Edit items amount in cart')
@allure.title('[Edit cart] Change item quantity')
@allure.tag('New feature')
@allure.severity(Severity.NORMAL)
def test_edit_items_quantity(driver_with_cookies, common_session):
    product_name = ProductName.MACBOOK
    count = '2'
    updated_count = '1'
    product = Product(product_id=AvailableProductId.MACBOOK, quantity=count)
    data = create_product_request_data(product)

    with allure.step(f'Add {product_name} to cart and open Cart'):
        response = common_session.post('/index.php', params='route=checkout/cart/add', data=data)
        total_price = get_total_cart_price(response=response)
        total_price_repr = get_price_repr(float(total_price))
        app.cart_page.open_cart_page()

    with allure.step(f'Assert item count in cart is {count}'):
        app.cart_page.item_quantity.with_(timeout=7).should(have.value(count))

    with allure.step(f'Assert total price for {count} item(s) is correct'):
        app.cart_page.total_item_price.should(have.text(total_price_repr))

    app.cart_page.item_quantity.clear()
    app.cart_page.update_product_count(value=updated_count)

    with allure.step(f'Assert item count in cart after update is {updated_count}'):
        app.cart_page.item_quantity.with_(timeout=7).should(have.value(updated_count))
    new_price = total_price / 2
    new_price_repr = get_price_repr(float(new_price))

    with allure.step(f'Assert total price for {updated_count} item(s) is correct'):
        app.cart_page.total_item_price.should(have.text(new_price_repr))


@allure.epic('Cart')
@allure.story('Edit cart')
@allure.feature('Clear item position in cart')
@allure.title('[Edit cart] Delete the only item')
@allure.tag('Regression')
@allure.severity(Severity.CRITICAL)
def test_clear_cart(driver_with_cookies, common_session):
    product_name = ProductName.MACBOOK
    product = Product(product_id=AvailableProductId.MACBOOK, quantity='1')
    data = create_product_request_data(product)

    with allure.step(f'Add {product_name} to cart and open Cart'):
        common_session.post('/index.php', params='route=checkout/cart/add', data=data)
        app.cart_page.open_cart_page()

    app.cart_page.delete_the_only_item()

    with allure.step('Assert cart is now empty'):
        app.cart_page.cart_empty_pic.should(be.visible)


@allure.epic('Cart')
@allure.story('Edit cart')
@allure.feature('Apply discounts to order')
@allure.title('[Edit cart] Apply discounts. Invalid codes')
@allure.tag('Regression')
@allure.severity(Severity.CRITICAL)
def test_add_discounts_to_cart__invalid_codes(driver_with_cookies, common_session):
    product_name = ProductName.MACBOOK
    product = Product(product_id=AvailableProductId.MACBOOK, quantity='1')
    data = create_product_request_data(product)
    coupon_code = '123'
    voucher_code = '123'

    with allure.step(f'Add {product_name} to cart and open Cart'):
        common_session.post('/index.php', params='route=checkout/cart/add', data=data)
        app.cart_page.open_cart_page()

    app.cart_page.apply_coupon(code=coupon_code)

    with allure.step('Assert Invalid coupon banner shown'):
        app.cart_page.invalid_coupon_banner.should(be.visible)

    app.cart_page.close_coupon_banner()

    app.cart_page.apply_voucher(code=voucher_code)

    with allure.step('Assert Invalid voucher banner shown'):
        app.cart_page.invalid_voucher_banner.should(be.visible)

    app.cart_page.close_voucher_banner()
