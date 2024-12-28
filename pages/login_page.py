from allure import step
from selene import browser


class LoginPage:
    def __init__(self):
        self.url = url = '/index.php?route=account/login'

        # Login form inputs
        self.email_input = browser.element('#input-email')
        self.password_input = browser.element('#input-password')

        self.login_button = browser.element('[value="Login"]')
        self.invalid_creds_error = browser.element(
            '//*[contains(text(), "No match for E-Mail Address and/or Password.")]')

        self.add_new_user_button = browser.element('//*[text()="New Customer"]/..//*[text()="Continue"]')


    @step('Fill in login form')
    def login_user(self, email: str, password: str):
        self.email_input.type(email)
        self.password_input.type(password)
        self.login_button.click()
