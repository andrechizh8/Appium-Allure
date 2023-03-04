import allure
from appium.webdriver.common.appiumby import AppiumBy
from selene import have, be
from selene.support.shared import browser
from model import app
from allure import step, title


@allure.title('owner')
def test_wikipedia():
    with allure.step("skip start window"):
        app.given_opened()

    with allure.step("search info"):
        browser.element((AppiumBy.ID, "org.wikipedia.alpha:id/search_container")).click()
        browser.element((AppiumBy.ID, "org.wikipedia.alpha:id/search_src_text")).type('Krasnodar')

    with allure.step("assert info"):
        browser.all((AppiumBy.ID, "org.wikipedia.alpha:id/page_list_item_title")).should(have.size_greater_than(0))

    with allure.step("go to page"):
        browser.all((AppiumBy.ID, "org.wikipedia.alpha:id/page_list_item_title")).element_by(have.text("Airport")).click()
        browser.element((AppiumBy.ID, "org.wikipedia.alpha:id/view_page_header_image")).should(be.visible)

    with allure.step("change language"):
        browser.element((AppiumBy.ID, "org.wikipedia.alpha:id/page_language")).click()
        browser.element((AppiumBy.ACCESSIBILITY_ID, "Search for a language")).click()
        browser.element((AppiumBy.ID, "org.wikipedia.alpha:id/search_src_text")).type("Russian")

    with allure.step("assert language changing"):
        browser.element((AppiumBy.ID, "org.wikipedia.alpha:id/localized_language_name")).should(have.text("Русский")).click()

    with allure.step("search info"):
        browser.element((AppiumBy.ID, "org.wikipedia.alpha:id/page_toolbar_button_search")).click()
        browser.element((AppiumBy.ID, "org.wikipedia.alpha:id/search_src_text")).type('Universe')
        browser.all((AppiumBy.ID, "org.wikipedia.alpha:id/page_list_item_description")).element_by(have.text("Everything in space and time")).click()

    with allure.step("assert page visible"):
        browser.element((AppiumBy.ID, "org.wikipedia.alpha:id/view_page_header_image")).should(be.visible)
