import pytest
import requests
from requests.utils import cookiejar_from_dict, dict_from_cookiejar
from selene import browser
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as OptionsChrome
from selenium.webdriver.firefox.options import Options as OptionsFirefox

from config.test_run_config import config
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
def driver_config_setup(request):
    browser_name = config.browser_name
    browser_version = config.browser_version
    local_run = request.config.getoption('--local-run')
    if local_run:
        if browser_name == 'chrome':
            browser.config.driver_options = webdriver.ChromeOptions()
        if browser_name == 'firefox':
            browser.config.driver_options = webdriver.FirefoxOptions()
    else:
        if browser_name == 'chrome':
            options = OptionsChrome()
        else:
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
        selenoid_url = config.selenoid_url
        driver = webdriver.Remote(
            command_executor=f'https://{user}:{password}@{selenoid_url}', options=options)
        browser.config.driver = driver

    browser.config.window_height = config.window_height
    browser.config.window_width = config.window_width
    browser.config.base_url = URL

    yield browser

    attach.add_screenshot(browser)
    if config.browser_name == 'chrome':
        attach.add_logs(browser)
    attach.add_page_source(browser)
    attach.add_video(browser)

    browser.quit()


@pytest.fixture(scope='function')
def driver_with_cookies(driver_config_setup, get_session_cookies):
    driver_config_setup.open('/')
    driver_config_setup.driver.delete_all_cookies()
    for name, value in get_session_cookies.items():
        driver_config_setup.driver.add_cookie(dict(name=name, value=value))

    yield driver_config_setup


@pytest.fixture(scope='function')
def no_cookie_driver(driver_config_setup):
    yield driver_config_setup


@pytest.fixture(scope='function')
def common_session(get_session_cookies):
    cookies = cookiejar_from_dict(get_session_cookies)
    session = ApiSession(base_url=URL, cookies=cookies)

    yield session


@pytest.fixture(scope='function')
def no_cookie_session():
    session = ApiSession(base_url=URL)

    yield session
