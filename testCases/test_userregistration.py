import time
import pytest
from selenium.common import NoSuchElementException
from pageObjects.mainPage import MainPage
from utilities.BaseClass import BaseClass
from TestData.TestData import RandomData
from TestData.SQLConnection import SQLFunctions
from pageObjects.loginPage import LoginPage


class TestUserRegistration(BaseClass):

    def test_register_user_manual_helper(self):
        main_page = MainPage(self.driver)
        main_page.close_cookies()
        sql_function = SQLFunctions()
        registration_page = main_page.get_to_registration_page()
        random_data = RandomData()
        customer_data = random_data.generate_random_chinese_info()
        email_value = sql_function.get_email_value()
        customer_email = "chinacustomertme+" + str(email_value) + "@gmail.com"
        registration_page.get_zhu_fapiao()
        registration_page.input_company_name(customer_data["company"])
        registration_page.input_vat_number(customer_data["vat_number"])
        registration_page.input_registered_address(customer_data["registered_address"])
        registration_page.input_company_phone(customer_data["office_phone"])
        registration_page.input_bank_name(customer_data["bank_name"])
        registration_page.input_bank_number(customer_data["bank_number"])
        registration_page.input_send_to_company(customer_data["company"])
        registration_page.select_province()
        registration_page.input_send_to_detailed_address(customer_data["detailed_address"])
        registration_page.input_send_to_phone(customer_data["phone_number"])
        registration_page.input_contact_person_surname(customer_data["surname"])
        registration_page.input_contact_person_name(customer_data["name"])
        registration_page.input_contact_person_phone(customer_data["phone_number"])
        registration_page.input_contact_person_email(customer_email)
        registration_page.same_fapiao_email_switch()
        registration_page.select_all_agreements()


        time.sleep(20)

    @pytest.mark.registration
    def test_register_user_basic(self):
        main_page = MainPage(self.driver)
        main_page.close_cookies()
        db_version = main_page.get_db_version()
        sql_function = SQLFunctions()
        registration_page = main_page.get_to_registration_page()
        random_data = RandomData()
        customer_data = random_data.generate_random_chinese_info()
        email_value = sql_function.get_email_value()
        customer_email = "chinacustomertme+" + str(email_value) + "@gmail.com"
        registration_page.get_zhu_fapiao()
        registration_page.input_company_name(customer_data["company"])
        registration_page.input_vat_number(customer_data["vat_number"])
        registration_page.input_registered_address(customer_data["registered_address"])
        registration_page.input_company_phone(customer_data["office_phone"])
        registration_page.input_bank_name(customer_data["bank_name"])
        registration_page.input_bank_number(customer_data["bank_number"])
        registration_page.input_send_to_company(customer_data["company"])
        registration_page.select_province()
        registration_page.input_send_to_detailed_address(customer_data["detailed_address"])
        registration_page.input_send_to_phone(customer_data["phone_number"])
        registration_page.input_contact_person_surname(customer_data["surname"])
        registration_page.input_contact_person_name(customer_data["name"])
        registration_page.input_contact_person_phone(customer_data["phone_number"])
        registration_page.input_contact_person_email(customer_email)
        registration_page.same_fapiao_email_switch()
        registration_page.select_all_agreements()
        registration_page.register_customer()
        sql_function.add_customer_to_database(
            email_value, customer_data["company"], customer_data["vat_number"], customer_data["registered_address"],
            customer_data["office_phone"], customer_data["bank_name"], customer_data["bank_number"],
            customer_data["detailed_address"], customer_data["phone_number"], customer_data["name"],
            customer_data["surname"], customer_data["phone_number"], customer_email, db_version
        )
        list_to_compare = [
            customer_data["company"], str(customer_data["vat_number"]), customer_data["registered_address"],
            str(customer_data["office_phone"]), customer_email, customer_email, str(customer_data["phone_number"]),
            customer_data["name"], customer_data["surname"]
        ]
        welcome_page_items = registration_page.get_welcome_page_items_list()
        for i in range(len(list_to_compare)):
            assert list_to_compare[i] == welcome_page_items[i]
        set_password_link = self.get_hyperlink_from_message()
        self.get_to(set_password_link)
        registration_page.input_first_password()
        registration_page.input_second_password()
        registration_page.get_save_password_button().click()
        sql_function.confirmed_password(email_value)
        sql_function.close_connection()
        login_page = LoginPage(self.driver)
        login_page.input_username(customer_email)
        login_page.input_password("1qaz@WSX")
        login_page.get_login_button().click()
        assert customer_data["name"] in main_page.get_page_header().text
        current_url = self.get_current_url()
        if "account/agreements" in current_url:
            try:
                login_page.accept_after_login_agreement()
            except NoSuchElementException:
                pass
        main_page.get_page_header().click()
        account_page = main_page.get_to_account_dashboard()
        account_values_company = account_page.get_account_dashboard_values_dict("company")
        for data in account_values_company:
            assert account_values_company[data] == str(customer_data[data])

    def test_registration_validation(self):
        main_page = MainPage(self.driver)
        main_page.close_cookies()
        registration_page = main_page.get_to_registration_page()
        time.sleep(15)
        registration_page.register_customer()
        validations = registration_page.return_list_of_all_validations()
        assert len(validations) == 16
        for validation in validations:
            assert validation == "该字段为强制性"
        self.refresh()
        registration_page.input_text_to_all_input_fields("a")
        validations = registration_page.return_list_of_all_validations()
        chinese_only_validations_one = [validations[0], validations[3], validations[5]]
        chinese_only_validations_two = [validations[8], validations[9], validations[13]]
        number_length_validations = [validations[2], validations[6], validations[10]]
        for validation in chinese_only_validations_one:
            assert validation == "仅限汉字、括号和中划线（半角输入法/英文, 即”-“）"
        for validation in chinese_only_validations_two:
            assert validation == "仅限汉字输入"
        for validation in number_length_validations:
            assert validation == "该字段必须至少包含11个数字"
        assert validations[1] == "该字段必须至少包含15个数字"
        assert validations[4] == "请输入数字"
        assert validations[7] == "该字段为强制性"
        assert validations[11] == "格式无效，请输入有效的电子邮件地址，例如smith@domain.cn"
        assert validations[12] == "格式无效，请输入有效的电子邮件地址，例如smith@domain.cn"
        self.refresh()
        registration_page.input_text_to_all_input_fields("请"*65)
        validations = registration_page.return_list_of_all_validations()
        assert len(validations) == 16
        validations_64 = [validations[0], validations[4], validations[6]]
        for validation in validations_64:
            assert validation == "字段的最大长度为64个字符"
        assert validations[1] == "字段的最大长度为20个字符"
        assert validations[2] == "字段的最大长度为60个字符"
        validations_15 = [validations[3], validations[8], validations[12]]
        for validation in validations_15:
            assert validation == "字段的最大长度为15个字符"
        assert validations[5] == "字段的最大长度为30个字符"
        validations_35 = [validations[7], validations[10], validations[11]]
        for validation in validations_35:
            assert validation == "字段的最大长度为35个字符"
        self.refresh()
        registration_page.input_text_to_all_input_fields("1"*21)
        validations = registration_page.return_list_of_all_validations()
        assert validations[1] == "字段的最大长度为20个字符"
        assert validations[2] == "字段的最大长度为15个字符"
        assert validations[5] == "字段的最大长度为15个字符"
        assert validations[6] == "该字段必须包含6数字"
        assert validations[9] == "字段的最大长度为15个字符"
