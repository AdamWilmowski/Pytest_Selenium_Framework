import time

from utilities.BaseClass import BaseClass
from pageObjects.mainPage import MainPage
from TestData.SQLConnection import SQLFunctions
from TestData.Secrets import Secrets
from pageObjects.accountPage import AccountPage


class TestLogin(BaseClass):
    def test_basic_login(self):
        main_page = MainPage(self.driver)
        self.close_cookies()
        db_version = main_page.get_db_version()
        login_page = main_page.get_to_login_page()
        sql_function = SQLFunctions()
        email = sql_function.get_random_customer(db_version)
        customer_name = sql_function.search_for_customer_data_by_email("contact_person_name", email)
        sql_function.close_connection()
        login_page.input_username(email)
        login_page.input_password(Secrets.default_password)
        login_page.get_login_button().click()
        assert customer_name in main_page.get_page_header().text

    def test_reset_password(self):
        main_page = MainPage(self.driver)
        self.close_cookies()
        db_version = main_page.get_db_version()
        login_page = main_page.get_to_login_page()
        sql_function = SQLFunctions()
        email = sql_function.get_random_customer(db_version)
        customer_name = sql_function.search_for_customer_data_by_email("contact_person_name", email)
        sql_function.close_connection()
        login_page.get_to_reset_password()
        login_page.input_reset_password_email(email)
        login_page.reset_password()
        time.sleep(20)
        url = self.get_hyperlink_from_message(subject="重置密码", search_pattern="forgotten-password")
        self.get_to(url)
        login_page.input_reset_password_first_password(Secrets.default_password + "1")
        login_page.input_reset_password_second_password(Secrets.default_password + "1")
        login_page.input_username(email)
        login_page.input_password(Secrets.default_password + "1")
        login_page.get_login_button().click()
        assert customer_name in main_page.get_page_header().text
        url = self.get_current_url()
        if "dashboard" in url:
            account_page = AccountPage(self.driver)
            account_page.get_to_reset_password()
        else:
            main_page.get_page_header().click()
            account_page = main_page.get_to_account_dashboard()
            account_page.get_to_reset_password()
        account_page.input_reset_password_current_password(Secrets.default_password + "1")
        account_page.input_reset_password_new_password(Secrets.default_password)
        account_page.input_reset_password_new_password_confirm(Secrets.default_password)
        account_page.reset_password()
        self.get_to_main()
        main_page.logout_customer()
        self.refresh()
        main_page.get_to_login_page()
        login_page.input_username(email)
        login_page.input_password()
        login_page.get_login_button().click()
        assert customer_name in main_page.get_page_header().text
