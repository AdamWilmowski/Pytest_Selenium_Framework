import time

from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


class RegistrationPage:
    def __init__(self, driver):
        self.driver = driver

    # REGISTRATION FORM

    zhu_fapiao = (By.CSS_SELECTOR, "label[for='app_company_user_company_fapiaoType_0']")
    company_name = (By.ID, "app_company_user_company_name")
    VAT_number = (By.ID, "app_company_user_company_vatNumber")
    registered_address = (By.ID, "app_company_user_company_registeredCompanyAddress")
    company_phone = (By.ID, "app_company_user_company_landlinePhoneNumber")
    bank_name = (By.ID, "app_company_user_company_bankName")
    bank_number = (By.ID, "app_company_user_company_bankAccountNumber")
    send_to_company = (By.ID, "app_company_user_company_shipToDetails_company")
    send_to_detailed_address = (By.ID, "app_company_user_company_shipToDetails_street")
    send_to_phone = (By.ID, "app_company_user_company_shipToDetails_phoneNumber")
    send_to_zip = (By.ID, "app_company_user_company_shipToDetails_postcode")
    contact_person_surname = (By.ID, "app_company_user_customer_lastName")
    contact_person_name = (By.ID, "app_company_user_customer_firstName")
    contact_person_phone = (By.ID, "app_company_user_customer_phoneNumber")
    contact_person_email = (By.ID, "app_company_user_customer_email")
    same_as_fapiao_email = (By.CSS_SELECTOR, "label[for='app_company_user_customer_sameFapiaoEmail']")
    contact_person_position = (By.ID, "app_company_user_customer_position")
    agreements_i_agree = (By.ID, "//div[3]/div/div[1]/div/label")
    register_button = (By.CSS_SELECTOR, "button[class='button -primary -register']")

    # WELCOME PAGE

    welcome_page_items = (By.CSS_SELECTOR, 'span[class="item-value"]')

    # SET PASSWORD PAGE

    set_first_password = (By.ID, "app_user_set_password_password_first")
    set_second_password = (By.ID, "app_user_set_password_password_second")
    submit_password_button = (By.CSS_SELECTOR, "button[class='button -primary -login m-t-30 m-b-10']")



    def get_zhu_fapiao(self):
        return self.driver.find_element(*RegistrationPage.zhu_fapiao)

    def input_company_name(self, text):
        self.driver.find_element(*RegistrationPage.company_name).send_keys(text)

    def input_vat_number(self, text):
        self.driver.find_element(*RegistrationPage.VAT_number).send_keys(text)

    def input_registered_address(self, text):
        self.driver.find_element(*RegistrationPage.registered_address).send_keys(text)

    def input_company_phone(self, text):
        self.driver.find_element(*RegistrationPage.company_phone).send_keys(text)

    def input_bank_name(self, text):
        self.driver.find_element(*RegistrationPage.bank_name).send_keys(text)

    def input_bank_number(self, text):
        self.driver.find_element(*RegistrationPage.bank_number).send_keys(text)

    def input_send_to_company(self, text):
        self.driver.find_element(*RegistrationPage.send_to_company).send_keys(text)

    def input_send_to_detailed_address(self, text):
        self.driver.find_element(*RegistrationPage.send_to_detailed_address).send_keys(text)

    def input_send_to_phone(self, text):
        self.driver.find_element(*RegistrationPage.send_to_phone).send_keys(text)

    def input_contact_person_surname(self, text):
        self.driver.find_element(*RegistrationPage.contact_person_surname).send_keys(text)

    def input_contact_person_name(self, text):
        self.driver.find_element(*RegistrationPage.contact_person_name).send_keys(text)

    def input_contact_person_phone(self, text):
        self.driver.find_element(*RegistrationPage.contact_person_phone).send_keys(text)

    def input_contact_person_email(self, text):
        self.driver.find_element(*RegistrationPage.contact_person_email).send_keys(text)

    def get_same_fapiao_email_switch(self):
        return self.driver.find_element(*RegistrationPage.same_as_fapiao_email)

    def input_contact_person_position(self, text):
        self.driver.find_element(*RegistrationPage.contact_person_email).send_keys(text)

    def select_all_agreements(self):
        agreements = self.driver.find_elements(*RegistrationPage.contact_person_email)
        for agreement in agreements:
            agreement.click()

    def get_register_button(self):
        return self.driver.find_element(*RegistrationPage.register_button)

    def get_welcome_page_items_list(self):
        elements = self.driver.find_elements(*RegistrationPage.welcome_page_items)
        list_of_items = []
        for element in elements:
            list_of_items.append(element.txt)
        return list_of_items

    def select_province(self):
        self.driver.find_element(
            By.CSS_SELECTOR,
            "div[class='china-addressing-province ui dropdown selection']"
        ).click()
        time.sleep(1)
        self.driver.find_element(
            By.XPATH,
            "//form/div[2]/div[2]/div[2]/div/div[2]/div[1]"
        ).click()
        time.sleep(3)
        self.driver.find_element(
            By.CSS_SELECTOR,
            "div[class='js-autoload-field china-addressing-city ui dropdown selection']"
        ).click()
        time.sleep(1)
        self.driver.find_element(
            By.XPATH,
            "//form/div[2]/div[2]/div[3]/div/div[2]/div"
        ).click()
        time.sleep(3)
        self.driver.find_element(
            By.CSS_SELECTOR,
            "div[class='js-autoload-field china-addressing-district ui dropdown selection']"
        ).click()
        time.sleep(1)
        self.driver.find_element(
            By.XPATH,
            "//form/div[2]/div[2]/div[4]/div/div[2]/div[6]"
        ).click()
        time.sleep(3)
    # SET PASSWORD PAGE

    def input_first_password(self):
        self.driver.find_element(*RegistrationPage.set_first_password).send_keys("!QAZ2wsx")

    def input_second_password(self):
        self.driver.find_element(*RegistrationPage.set_second_password).send_keys("!QAZ2wsx")

    def get_save_password_button(self):
        return self.driver.find_element(*RegistrationPage.submit_password_button)

