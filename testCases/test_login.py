from utilities.BaseClass import BaseClass
from pageObjects.mainPage import MainPage
from TestData.SQLConnection import SQLFunctions
from TestData.Secrets import Secrets


class TestLogin(BaseClass):
    def test_basic_login(self):
        main_page = MainPage(self.driver)
        self.close_cookies()
        db_version = main_page.get_db_version()
        login_page = main_page.get_to_login_page()
        sql_function = SQLFunctions()
        email = sql_function.get_random_customer(db_version)
        customer_name = sql_function.search_for_customer_data_by_email("contact_person_name", email)
        login_page.input_username(email)
        login_page.input_password(Secrets.default_password)
        login_page.get_login_button().click()
        assert customer_name in main_page.get_page_header().text
