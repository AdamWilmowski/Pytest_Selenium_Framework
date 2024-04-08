import time
import pytest
from selenium.common import NoSuchElementException
from pageObjects.mainPage import MainPage
from pageObjects.registrationPage import RegistrationPage
from utilities.BaseClass import BaseClass
from TestData.TestData import RandomData
from TestData.SQLConnection import SQLFunctions
from pageObjects.loginPage import LoginPage
from TestData.Secrets import Secrets


class TestCompanyUser(BaseClass):
    @pytest.mark.parametrize("role", ["admin", "user"])
    def test_add_company_user_admin(self, role):
        main_page = MainPage(self.driver)
        main_page.close_cookies()
        db_version = main_page.get_db_version()
        random_data = RandomData()
        customer_data = random_data.generate_random_chinese_info()
        sql_function = SQLFunctions()
        parent_email, parent_email_id = sql_function.get_random_customer_email_and_id(db_version)
        email_value = sql_function.get_email_value()
        email = "chinacustomertme+" + str(email_value) + "@gmail.com"
        login_page = main_page.get_to_login_page()
        login_page.input_username(parent_email)
        login_page.input_password(Secrets.default_password)
        login_page.get_login_button().click()
        self.get_to_main()
        main_page.get_page_header().click()
        account_page = main_page.get_to_account_dashboard()
        account_page.get_to_company_users()
        account_page.add_new_company_user()
        if role == "user":
            account_page.change_from_admin_to_default_user()
        account_page.input_customer_name(customer_data['name'])
        account_page.input_customer_surname(customer_data['surname'])
        account_page.input_customer_emil(email)
        account_page.input_customer_phone(customer_data['phone_number'])
        account_page.add_company_user()
        company_user_email_list = account_page.get_company_users_data_list("emails")
        assert company_user_email_list[0] == email
        company_user_roles = account_page.get_company_users_data_list("roles")
        if role == "admin":
            assert company_user_roles[0] == "公司管理员"
            is_admin = 1
        else:
            assert company_user_roles[0] == "默认用户"
            is_admin = 0
        company_user_statuses_list = account_page.get_company_users_data_list("statuses")
        assert company_user_statuses_list[0] == "未验证电子邮件"
        sql_function.add_company_user_to_database(is_admin, customer_data['name'], customer_data['surname'],
                                                  customer_data['phone_number'], int(email_value), email,
                                                  int(parent_email_id), db_version)
        self.get_to_main()
        main_page.logout_customer()
        self.refresh()
        time.sleep(25)
        hyperlink = self.get_hyperlink_from_message()
        self.get_to(hyperlink)
        registration_page = RegistrationPage(self.driver)
        registration_page.input_first_password()
        registration_page.input_second_password()
        registration_page.get_save_password_button().click()
        sql_function.confirm_company_user(email_value)
        login_page.input_username(email)
        login_page.input_password(Secrets.default_password)
        login_page.get_login_button().click()
        current_url = self.get_current_url()
        if "account/agreements" in current_url:
            try:
                login_page.accept_after_login_agreement()
            except NoSuchElementException:
                pass
        assert customer_data["name"] in main_page.get_page_header().text
        main_page.get_page_header().click()
        main_page.get_to_account_dashboard()
        account_page.get_to_company_users()
        company_user_email_list = account_page.get_company_users_data_list("emails")
        assert company_user_email_list[0] == parent_email
        company_user_roles_list = account_page.get_company_users_data_list("roles")
        assert company_user_roles_list[0] == "公司管理员"
        company_user_statuses_list = account_page.get_company_users_data_list("statuses")
        assert company_user_statuses_list[0] == "活跃"
        if role == "admin":
            account_page.add_new_company_user()
            url = self.get_current_url()
            assert url == "https://betacn-new.tme.hk/account/company/users/add"
        else:
            try:
                account_page.add_new_company_user()
                raise "Default company user can register new account"
            except NoSuchElementException:
                pass

    def test_company_user_validations(self):
        main_page = MainPage(self.driver)
        main_page.close_cookies()
        db_version = main_page.get_db_version()
        login_page = main_page.get_to_login_page()
        login_page.get_to_main_with_random_login(db_version)
        main_page.get_page_header().click()
        account_page = main_page.get_to_account_dashboard()
        account_page.get_to_company_users()
        account_page.add_new_company_user()
        account_page.add_company_user()
        validations = account_page.get_list_of_company_user_validations()
        assert len(validations) == 4
        for validation in validations:
            assert validation == "该字段为强制性"
        account_page.input_customer_name("Abc")
        account_page.input_customer_surname("Abc")
        account_page.input_customer_emil("Abc")
        account_page.input_customer_phone("Abc")
        account_page.add_company_user()
        validations = account_page.get_list_of_company_user_validations()
        assert validations[0] == "仅限汉字输入"
        assert validations[1] == "仅限汉字输入"
        assert validations[2] == "格式无效，请输入有效的电子邮件地址，例如smith@domain.cn"
        assert validations[3] == "电话号码无效"
        self.refresh()
        account_page.clear_all_input_fields()
        account_page.input_customer_name("输"*36)
        account_page.input_customer_surname("输"*36)
        account_page.input_customer_emil("a"*62+"@b.c")
        account_page.input_customer_phone("1"*10)
        account_page.add_company_user()
        validations = account_page.get_list_of_company_user_validations()
        assert validations[0] == "名称”字段的最大长度为 35 个字符。"
        assert validations[1] == "名称”字段的最大长度为 35 个字符。"
        assert validations[2] == "“电子邮件”字段的最大长度为64个字符"
        assert validations[3] == "该字段必须包含最少 11 位数字，最多包含 15 位数字。"
        self.refresh()





