from pydantic_settings import BaseSettings

from utils.env_path_getter import get_resource_path


class Config(BaseSettings):
    url: str = 'https://ecommerce-playground.lambdatest.io'
    selenoid_url: str = 'selenoid.autotests.cloud/wd/hub'
    browser_name: str
    browser_version: str = '125.0'
    selenoid_login: str
    selenoid_password: str
    window_width: str = '1920'
    window_height: str = '1080'


config = Config(_env_file=get_resource_path('.env'))
