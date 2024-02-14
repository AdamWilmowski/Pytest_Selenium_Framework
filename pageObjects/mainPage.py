from selenium.common import NoSuchElementException
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from pageObjects import registrationPage
from pageObjects import accountPage
from TestData.SQLConnection import SQLFunctions


class MainPage:
    def __init__(self, driver):
        self.driver = driver

    close_cookies_icon = (By.ID, "cookies-consent-close-icon")
    db_version = (By.CSS_SELECTOR, "div[class='site-footer__text']")
    register_button = (By.LINK_TEXT, '注册')
    main_header = (By.CSS_SELECTOR, 'div[class="header-security-dropdown-title d-flex align-items-center justify-content-between"]')
    account_dashboard_button = (By.LINK_TEXT, "帐户面板")

    def close_cookies(self):
        try:
            self.driver.find_element(*MainPage.close_cookies_icon).click()
        except NoSuchElementException:
            pass

    def get_db_version(self):
        footer_list = self.driver.find_element(*MainPage.db_version).text
        db_version = footer_list.split()[6]
        return db_version

    def get_to_registration_page(self):
        self.driver.find_element(*MainPage.register_button).click()
        registration_page = registrationPage.RegistrationPage(self.driver)
        return registration_page

    def get_page_header(self):
        return self.driver.find_element(*MainPage.main_header)

    def get_to_account_dashboard(self):
        self.driver.find_element(*MainPage.account_dashboard_button).click()
        account_page = accountPage.AccountPage(self.driver)
        return account_page


