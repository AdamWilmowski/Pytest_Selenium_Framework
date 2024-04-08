from selenium.webdriver.common.by import By
from TestData.SQLConnection import SQLFunctions


class LoginPage:

    def __init__(self, driver):
        self.driver = driver

    username = (By.ID, "_username")
    password = (By.ID, "_password")
    login_button = (By.CSS_SELECTOR, "button[class='button -primary -login m-t-30 m-b-45']")
    agreement_button = (By.CSS_SELECTOR, 'div[class="ui radio checkbox"]')
    agreements_agree_button = (By.CSS_SELECTOR, 'button[class="button -primary -medium -fullWidth"]')
    reset_password_button = (By.CSS_SELECTOR, "link -grey text-align-right")
    reset_password_email = (By.ID, "sylius_user_request_password_reset_email")
    send_reset_email_button = (By.ID, "button -primary -login m-t-30 m-b-10")
    reset_password_first_password = (By.ID, "sylius_user_reset_password_password_first")
    reset_password_second_password = (By.ID, "sylius_user_reset_password_password_second")

    def input_username(self, text):
        self.driver.find_element(*LoginPage.username).send_keys(text)

    def input_password(self, text):
        self.driver.find_element(*LoginPage.password).send_keys(text)

    def get_login_button(self):
        return self.driver.find_element(*LoginPage.login_button)

    def accept_after_login_agreement(self):
        buttons = self.driver.find_elements(*LoginPage.agreement_button)
        for i in range(len(buttons)):
            if i % 2 == 0:
                buttons[i].click()
        self.driver.find_element(*LoginPage.agreements_agree_button).click()

    def get_to_main_with_random_login(self, version):
        sql_function = SQLFunctions()
        email = sql_function.get_random_customer(version)
        sql_function.close_connection()
        self.driver.find_element(*LoginPage.username).send_keys(email)
        self.driver.find_element(*LoginPage.password).send_keys("1qaz@WSX")
        self.driver.find_element(*LoginPage.login_button).click()

    def get_to_reset_password(self):
        self.driver.find_element(*LoginPage.reset_password_button).click()

    def input_reset_password_email(self, text):
        self.driver.find_element(*LoginPage.reset_password_email).send_keys(text)

    def reset_password(self):
        self.driver.find_element(*LoginPage.reset_password_button).click()

    def input_reset_password_first_password(self, text):
        self.driver.find_element(*LoginPage.reset_password_first_password).send_keys(text)

    def input_reset_password_second_password(self, text):
        self.driver.find_element(*LoginPage.reset_password_first_password).send_keys(text)