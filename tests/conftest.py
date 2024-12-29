import pytest
import requests
from requests.utils import cookiejar_from_dict, dict_from_cookiejar
from selene import browser
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as OptionsChrome
from selenium.webdriver.firefox.options import Options as OptionsFirefox

from config import config
from utils import attach
from utils.session import ApiSession

URL = config.url


def pytest_addoption(parser):
    parser.addoption('--local-run', action='store_true')


@pytest.fixture(scope='function')
def get_session_cookies():
    response = requests.get(url=URL, allow_redirects=False)
    cookies = dict_from_cookiejar(response.cookies)
    yield cookies


@pytest.fixture(scope='function')
def base_driver(request):
    browser_name = config.browser_name
    browser_version = config.browser_version
    local_run = request.config.getoption('--local-run')
    if local_run:
        if browser_name == 'chrome':
            browser.config.driver_options = webdriver.ChromeOptions()
        if browser_name == 'firefox':
            browser.config.driver_options = webdriver.FirefoxOptions()
        browser.config.window_height = config.window_height
        browser.config.window_width = config.window_width
    else:
        if browser_name == 'chrome':
            options = OptionsChrome()
        if browser_name == 'firefox':
            options = OptionsFirefox()
        selenoid_capabilities = {
            "browserName": browser_name,
            "browserVersion": browser_version,
            "selenoid:options": {
                "enableVNC": True,
                "enableVideo": True
            }
        }
        options.capabilities.update(selenoid_capabilities)

        user = config.selenoid_login
        password = config.selenoid_password
        driver = webdriver.Remote(
            command_executor=f'https://{user}:{password}@selenoid.autotests.cloud/wd/hub', options=options)
        browser.config.driver = driver

    browser.config.base_url = URL

    yield browser

    attach.add_screenshot(browser)
    if config.browser_name == 'chrome':
        attach.add_logs(browser)
    attach.add_page_source(browser)
    attach.add_video(browser)

    browser.quit()

@pytest.fixture(scope='function')
def driver(base_driver, get_session_cookies):
    base_driver.open('/')
    base_driver.driver.delete_all_cookies()
    for name, value in get_session_cookies.items():
        base_driver.driver.add_cookie(dict(name=name, value=value))

    yield base_driver


@pytest.fixture(scope='function')
def no_cookie_driver(base_driver):
    yield base_driver


@pytest.fixture(scope='function')
def session(get_session_cookies):
    cookies = cookiejar_from_dict(get_session_cookies)
    session = ApiSession(base_url=URL, cookies=cookies)

    yield session

@pytest.fixture(scope='function')
def no_cookie_session():
    session = ApiSession(base_url=URL)

    yield session
