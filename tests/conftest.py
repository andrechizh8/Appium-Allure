import allure_commons
import pytest
from selene.support.shared import browser
from selene import support
from appium import webdriver
from utils import attach
import config


@pytest.fixture(scope='function', autouse=True)
def browser_config():
    browser.config._wait_decorator = support._logging.wait_with(context=allure_commons._allure.StepContext)
    browser.config.driver = webdriver.Remote(config.settings.remote_url, options=config.settings.driver_options)
    browser.config.timeout = config.settings.timeout

    yield

    attach.add_video(browser)
    attach.add_screenshot(browser)

