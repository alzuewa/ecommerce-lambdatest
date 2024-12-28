from allure import step
from selene import browser, command


class GoodsPage:

    @staticmethod
    @step('Choose item from list. Item: {item_name}')
    def choose_item(item_name: str):
        item_element = (browser.all(f'.carousel-item > [title="{item_name}"]').with_(timeout=10).first.
                        perform(command.js.scroll_into_view))
        item_element.with_(timeout=20).click()
