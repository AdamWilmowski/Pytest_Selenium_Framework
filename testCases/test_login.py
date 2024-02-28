from utilities.BaseClass import BaseClass
from pageObjects.mainPage import MainPage
from TestData.SQLConnection import SQLFunctions


class TestLogin(BaseClass):
    def test_basic_login(self):
        main_page = MainPage(self.driver)
        self.close_cookies()
        db_version = main_page.get_db_version()
        login_page = main_page.get_to_login_page()
        sql_function = SQLFunctions()
        email = sql_function.get_random_customer(db_version)
        login_page.input_username(email)
        login_page.input_password("1qaz@WSX")
        login_page.get_login_button()