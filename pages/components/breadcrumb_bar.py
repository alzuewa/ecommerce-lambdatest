from allure import step
from selene import browser


class BreadcrumbBar:
    def __init__(self):
        self.active_breadcrumb_item = browser.element('.breadcrumb-item.active')

    @step('Getting last breadcrumb part text')
    def get_active_breadcrumb_text(self):
        return self.active_breadcrumb_item.locate().text
