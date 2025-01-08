import random
import string

import allure
import pytest
from allure_commons.types import Severity
from selene import be

from data.data_setup import create_user, create_user_request_data
from pages.application import app


@allure.epic('User account')
@allure.story('Register account')
@allure.feature('Register account')
@allure.title('[Account] Create. Valid data')
@allure.tag('Regression')
@allure.severity(Severity.BLOCKER)
def test_register__valid_data(driver_with_cookies):
    user = create_user()
    driver_with_cookies.open(app.registration_page.url)
    app.registration_page.register_user(
        first_name=user.firstname,
        last_name=user.lastname,
        email=user.email,
        phone=user.telephone,
        password=user.password
    )

    with allure.step('Assert registration success banner shown'):
        app.registration_page.register_success_banner.should(be.visible)


@allure.epic('User account')
@allure.story('Register account')
@allure.feature('Register account')
@allure.title('[Account] Create. Invalid phone number')
@allure.tag('Regression')
@allure.severity(Severity.BLOCKER)
@pytest.mark.parametrize('phone',
                         [
                             '',
                             ''.join(random.choice(string.digits) for _ in range(2)),
                             ''.join(random.choice(string.digits) for _ in range(33))
                         ]
                         )
def test_register__invalid_phone(driver_with_cookies, phone):
    user = create_user()
    driver_with_cookies.open(app.registration_page.url)
    app.registration_page.register_user(
        first_name=user.firstname,
        last_name=user.lastname,
        email=user.email,
        phone=phone,
        password=user.password
    )

    with allure.step('Assert invalid phone tip shown'):
        app.registration_page.invalid_phone_error.should(be.visible)


@allure.epic('User account')
@allure.story('Register account')
@allure.feature('Register account')
@allure.title('[Account] Register. Existing user')
@allure.tag('Regression')
@allure.severity(Severity.CRITICAL)
def test_register__existing_user(no_cookie_driver, no_cookie_session):
    user = create_user()
    data = create_user_request_data(user)

    with allure.step(f'Create user with API request'):
        no_cookie_session.post('/index.php', params='route=account/register', data=data)

    no_cookie_driver.open(app.registration_page.url)
    app.registration_page.register_user(
        first_name=user.firstname,
        last_name=user.lastname,
        email=user.email,
        phone=user.telephone,
        password=user.password
    )

    with allure.step('Assert email exists error shown'):
        app.registration_page.existing_email_error.should(be.visible)


@allure.epic('User account')
@allure.story('Login to account')
@allure.feature('Login')
@allure.title('[Account] Login. Valid credentials')
@allure.tag('Regression')
@allure.severity(Severity.BLOCKER)
def test_login__existing_user(no_cookie_driver, no_cookie_session):
    user = create_user()
    data = create_user_request_data(user)

    with allure.step(f'Create user with API request'):
        no_cookie_session.post('/index.php', params='route=account/register', data=data)

    no_cookie_driver.open(app.login_page.url)
    app.login_page.login_user(
        email=user.email,
        password=user.password
    )

    with allure.step('Assert user account page opened'):
        assert app.breadcrumb_bar.get_active_breadcrumb_text() == 'Account'


@allure.epic('User account')
@allure.story('Login to account')
@allure.feature('Login')
@allure.title('[Account] Login. Incorrect email and password')
@allure.tag('Regression')
@allure.severity(Severity.BLOCKER)
def test_login__non_existing_user(driver_with_cookies):
    user = create_user()

    driver_with_cookies.open(app.login_page.url)
    app.login_page.login_user(
        email=user.email,
        password=user.password
    )

    with allure.step('Assert invalid email or password error shown'):
        app.login_page.invalid_creds_error.should(be.visible)


@allure.epic('User account')
@allure.story('Login to account')
@allure.feature('Login')
@allure.title('[Account] Login. Incorrect password')
@allure.tag('Regression')
@allure.severity(Severity.BLOCKER)
def test_login__incorrect_password(no_cookie_driver, no_cookie_session):
    user = create_user()
    data = create_user_request_data(user)

    with allure.step(f'Create user with API request'):
        no_cookie_session.post('/index.php', params='route=account/register', data=data)

    no_cookie_driver.open(app.login_page.url)
    app.login_page.login_user(
        email=user.email,
        password=(string.printable for _ in range(12))
    )

    with allure.step('Assert invalid email or password error shown'):
        app.login_page.invalid_creds_error.should(be.visible)
