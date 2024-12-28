from selene import browser


class BreadcrumbBar:
    def __init__(self):
        self.active_breadcrumb_item = browser.element('.breadcrumb-item.active')
