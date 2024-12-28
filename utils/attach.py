import allure
from allure_commons.types import AttachmentType


def add_screenshot(browser):
    screenshot = browser.driver.get_screenshot_as_png()
    allure.attach(
        body=screenshot,
        name='screenshot',
        attachment_type=AttachmentType.PNG,
        extension='.png'
    )


def add_page_source(browser):
    page_source = browser.driver.page_source
    allure.attach(
        body=page_source,
        name='screen html dump',
        attachment_type=AttachmentType.HTML,
        extension='.html'
    )


def add_logs(browser):
    log = "".join(f'{line}\n' for line in browser.driver.get_log(log_type='browser'))
    allure.attach(
        body=log,
        name='browser_logs',
        attachment_type=AttachmentType.TEXT,
        extension='.log'
    )


def add_video(browser):
    video_url = "https://selenoid.autotests.cloud/video/" + browser.driver.session_id + ".mp4"
    html = "<html><body><video width='100%' height='100%' controls autoplay><source src='" \
           + video_url \
           + "' type='video/mp4'></video></body></html>"
    allure.attach(
        body=html,
        name='video_' + browser.driver.session_id,
        attachment_type=AttachmentType.HTML,
        extension='.html'
    )
