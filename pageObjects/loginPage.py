from selenium.webdriver.common.by import By
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from pageObjects import registrationPage
from TestData.SQLConnection import SQLFunctions

class LoginPage:

    def __init__(self, driver):
        self.driver = driver

    username = (By.ID, "_username")
    password = (By.ID, "_password")
    login_button = (By.CSS_SELECTOR, "button[class='button -primary -login m-t-30 m-b-45']")

    def input_username(self, text):
        self.driver.find_element(*LoginPage.username).send_keys(text)

    def input_password(self, text):
        self.driver.find_element(*LoginPage.password).send_keys(text)

    def get_login_button(self):
        return self.driver.find_element(*LoginPage.login_button)

    def get_to_main_with_random_login(self, version):
        sql_function = SQLFunctions()
        email = sql_function.get_random_customer(version)
        sql_function.close_connection()
        self.driver.find_element(*LoginPage.username).send_keys(email)
        self.driver.find_element(*LoginPage.password).send_keys("1qaz@WSX")
        self.driver.find_element(*LoginPage.login_button).click()