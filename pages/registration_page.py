from allure import step
from selene import browser


class RegistrationPage:
    def __init__(self):
        self.url = url = '/index.php?route=account/register'

        # Registration form inputs
        self.first_name_input = browser.element('#input-firstname')
        self.last_name_input = browser.element('#input-lastname')
        self.email_input = browser.element('#input-email')
        self.phone_input = browser.element('#input-telephone')
        self.password_input = browser.element('#input-password')
        self.password_confirm_input = browser.element('#input-confirm')
        self.accept_terms_checkbox = browser.element('.custom-checkbox')

        self.register_success_banner = browser.element('.text-success')
        self.invalid_phone_error = browser.element('//*[text()="Telephone must be between 3 and 32 characters!"]')
        self.existing_email_error = browser.element('//*[contains(text(), "E-Mail Address is already registered!")]')
        self.continue_button = browser.element('[value="Continue"]')

    @step('Fill in registration form with '
          'first name: {first_name},\n last name: {last_name},\n email: {email},\n phone: {phone},\n password: {password}'
          )
    def register_user(self, first_name: str, last_name: str, email: str, phone: str, password: str):
        self.first_name_input.type(first_name)
        self.last_name_input.type(last_name)
        self.email_input.type(email)
        self.phone_input.type(phone)
        self.password_input.type(password)
        self.password_confirm_input.type(password)
        self.accept_terms_checkbox.click()
        self.continue_button.click()
