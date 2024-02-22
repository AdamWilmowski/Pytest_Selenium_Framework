from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


class CheckoutPage:
    def __init__(self, driver):
        self.driver = driver

    grand_total = (By.ID, "sylius-summary-grand-total")
    checkout_next_step = (By.ID, "next-step")
    place_order = (By.ID, "place-order")
    payment_gate_title = (By.TAG_NAME, 'h1')
    payment_gate_amount = (By.TAG_NAME, 'h3')
    payment_gate_yes_button = (By.CSS_SELECTOR, 'input[class="ui button green"]')
    thank_you_values = (By.CSS_SELECTOR, 'span[class="font-weight-light"]')

    # Unregistered checkout

    zhu_fapiao = (By.CSS_SELECTOR, 'label[for="app_checkout_company_data_customer_companyUser_company_fapiaoType_0"]')
    company_name = (By.ID, "app_checkout_company_data_customer_companyUser_company_name")
    vat_number = (By.ID, "app_checkout_company_data_customer_companyUser_company_vatNumber")
    registered_address_of_company = (By.ID, "app_checkout_company_data_customer_companyUser_company_registeredCompanyAddress")
    company_office_number = (By.ID, "app_checkout_company_data_customer_companyUser_company_landlinePhoneNumber")
    bank_name = (By.ID, "app_checkout_company_data_customer_companyUser_company_bankName")
    bank_number = (By.ID, "app_checkout_company_data_customer_companyUser_company_bankAccountNumber")
    surname = (By.ID, "app_checkout_company_data_customer_lastName")
    name = (By.ID, "app_checkout_company_data_customer_firstName")
    phone_number = (By.ID, "app_checkout_company_data_customer_phoneNumber")
    email = (By.ID, "app_checkout_company_data_customer_email")
    same_as_fapiao = (By.CSS_SELECTOR, 'label[for="app_checkout_company_data_customer_sameFapiaoEmail"]')
    company_name_shipping = (By.ID, "app_checkout_shipping_shippingAddress_company")
    detailed_address = (By.ID, "app_checkout_shipping_shippingAddress_street")
    phone_number_shipping = (By.ID, "app_checkout_shipping_shippingAddress_phoneNumber")
    agreement_radio = (By.CSS_SELECTOR, 'div[class="ui radio checkbox"]')


    def get_checkout_grand_total(self):
        total_raw = self.driver.find_element(*CheckoutPage.grand_total).text
        total = float(total_raw.split()[1])
        return total

    def get_to_next_step(self):
        self.driver.find_element(*CheckoutPage.grand_total).click()

    def get_to_place_order(self):
        self.driver.find_element(*CheckoutPage.place_order).click()

    def wait_for_payment_gate(self):
        WebDriverWait(self.driver, 60*6).until(
            EC.visibility_of_element_located((By.TAG_NAME, 'h1'))
        )

    def get_payment_gate_title(self):
        return self.driver.find_element(*CheckoutPage.payment_gate_title).text

    def get_payment_gate_amount(self):
        return float(self.driver.find_element(*CheckoutPage.payment_gate_amount).text.split()[1])

    def accept_payment(self):
        self.driver.find_element(*CheckoutPage.payment_gate_yes_button).click()

    def get_thank_you_values(self):
        elements_list_raw = self.driver.find_elements(*CheckoutPage.thank_you_values)
        elements_dict = {
            "order_number": elements_list_raw[0].text,
            "total": elements_list_raw[1].text.split()[1],
            "payment_type": elements_list_raw[4].text
        }
        return elements_dict

    # UNREGISTERED CHECKOUT

    def select_zhu_fapiao(self):
        self.driver.find_element(*CheckoutPage.zhu_fapiao).click()

    def input_company_name(self, text):
        self.driver.find_element(*CheckoutPage.company_name).send_keys(text)

    def input_vat_number(self, text):
        self.driver.find_element(*CheckoutPage.vat_number).send_keys(text)

    def input_register_address_of_company(self, text):
        self.driver.find_element(*CheckoutPage.registered_address_of_company).send_keys(text)

    def input_office_number(self, text):
        self.driver.find_element(*CheckoutPage.company_office_number).send_keys(text)

    def input_bank_name(self, text):
        self.driver.find_element(*CheckoutPage.bank_name).send_keys(text)

    def input_bank_number(self, text):
        self.driver.find_element(*CheckoutPage.bank_number).send_keys(text)

    def input_surname(self, text):
        self.driver.find_element(*CheckoutPage.surname).send_keys(text)

    def input_name(self, text):
        self.driver.find_element(*CheckoutPage.name).send_keys(text)

    def input_phone_number(self, text):
        self.driver.find_element(*CheckoutPage.phone_number).send_keys(text)

    def input_email(self, text):
        self.driver.find_element(*CheckoutPage.email).send_keys(text)

    def select_same_as_fapiao(self):
        self.driver.find_element(*CheckoutPage.same_as_fapiao).click()

    def input_company_name_shipping(self, text):
        self.driver.find_element(*CheckoutPage.company_name_shipping).send_keys(text)

    def select_province(self):
        self.driver.find_element(
            By.CSS_SELECTOR,
            "div[class='china-addressing-province ui dropdown selection']"
        ).click()
        time.sleep(1)
        self.driver.find_element(
            By.XPATH,
            "//form/div[1]/div/div[2]/div[1]/div[2]/div/div[2]/div[8]"
        ).click()
        time.sleep(3)
        self.driver.find_element(
            By.CSS_SELECTOR,
            "div[class='js-autoload-field china-addressing-city ui dropdown selection']"
        ).click()
        time.sleep(1)
        self.driver.find_element(
            By.XPATH,
            "//form/div[1]/div/div[2]/div[1]/div[3]/div/div/div/div[2]/div[8]"
        ).click()
        time.sleep(3)
        self.driver.find_element(
            By.CSS_SELECTOR,
            "div[class='js-autoload-field china-addressing-district ui dropdown selection']"
        ).click()
        time.sleep(1)
        self.driver.find_element(
            By.XPATH,
            "//form/div[1]/div/div[2]/div[1]/div[4]/div/div[2]/div[8]"
        ).click()
        time.sleep(3)

    def input_detailed_address_shipping(self, text):
        self.driver.find_element(CheckoutPage.detailed_address).send_keys(text)

    def input_phone_number_shipping(self, text):
        self.driver.find_element(CheckoutPage.phone_number_shipping).send_keys(text)

    def select_all_agreements(self):
        radio_buttons = self.driver.find_elements(*CheckoutPage.agreement_radio)
        for i in range(len(radio_buttons)):
            if i != 0:
                if i % 2 != 0:
                    radio_buttons[i].click()




