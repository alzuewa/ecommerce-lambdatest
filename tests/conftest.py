import os

import pytest
import requests
from dotenv import load_dotenv
from requests.utils import cookiejar_from_dict, dict_from_cookiejar
from selene import browser
from selenium import webdriver

from utils import attach
from utils.session import ApiSession

load_dotenv()
URL = os.getenv('URL')


@pytest.fixture(scope='function')
def get_session_cookies():
    response = requests.get(url=URL, allow_redirects=False)
    cookies = dict_from_cookiejar(response.cookies)
    yield cookies


@pytest.fixture(scope='function')
def driver(get_session_cookies):
    browser.config.driver_options = webdriver.ChromeOptions()
    browser.config.window_height = '1080'
    browser.config.window_width = '1920'
    browser.config.base_url = URL

    browser.open('/')
    browser.driver.delete_all_cookies()
    for name, value in get_session_cookies.items():
        browser.driver.add_cookie(dict(name=name, value=value))

    yield browser

    attach.add_screenshot(browser)
    attach.add_logs(browser)
    attach.add_page_source(browser)
    attach.add_video(browser)

    browser.quit()


@pytest.fixture(scope='function')
def no_cookie_driver():
    browser.config.driver_options = webdriver.ChromeOptions()
    browser.config.window_height = '1080'
    browser.config.window_width = '1920'
    browser.config.base_url = URL

    yield browser

    attach.add_screenshot(browser)
    attach.add_logs(browser)
    attach.add_page_source(browser)
    attach.add_video(browser)

    browser.quit()


@pytest.fixture(scope='function')
def session(get_session_cookies):
    cookies = cookiejar_from_dict(get_session_cookies)
    session = ApiSession(base_url=URL, cookies=cookies)

    yield session

@pytest.fixture(scope='function')
def no_cookie_session():
    session = ApiSession(base_url=URL)

    yield session
