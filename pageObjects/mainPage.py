from selenium.common import NoSuchElementException
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from pageObjects import registrationPage, loginPage, accountPage, checkoutPage

class MainPage:
    def __init__(self, driver):
        self.driver = driver

    close_cookies_icon = (By.ID, "cookies-consent-close-icon")
    db_version = (By.CSS_SELECTOR, "div[class='site-footer__text']")
    register_button = (By.LINK_TEXT, '注册')
    login_button = (By.LINK_TEXT, "登录")
    main_header = (By.CSS_SELECTOR, 'div[class="header-security-dropdown-title d-flex align-items-center justify-content-between"]')
    account_dashboard_button = (By.LINK_TEXT, "帐户面板")
    search_product = (By.XPATH, "//input")
    product_name = (By.CSS_SELECTOR, 'a[class="product-name font-weight-bold m-t-5"]')
    add_to_cart_listing = (By.XPATH, '//button[normalize-space()="Add to cart"]')
    cart_button = (By.XPATH, "//nav/div/div/div[3]/div[1]")
    checkout_button = (By.LINK_TEXT, "前往结账")

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

    def get_to_login_page(self):
        self.driver.find_element(*MainPage.login_button).click()
        login_page = loginPage.LoginPage(self.driver)
        return login_page

    def get_page_header(self):
        return self.driver.find_element(*MainPage.main_header)

    def get_to_account_dashboard(self):
        self.driver.find_element(*MainPage.account_dashboard_button).click()
        account_page = accountPage.AccountPage(self.driver)
        return account_page

    def search_for_product(self, text):
        self.driver.find_element(*MainPage.search_product).send_keys(text)
        self.driver.find_element(*MainPage.search_product).send_keys(Keys.ENTER)

    def get_to_product_page(self, number: int = 0):
        self.driver.find_elements(*MainPage.product_name)[number].click()

    def add_product_to_cart_listing(self, number: int = 0):
        self.driver.find_element(*MainPage.add_to_cart_listing)[number].click()

    def wait_till_product_in_cart(self, text):
        WebDriverWait(self.driver, 5).until(
            EC.text_to_be_present_in_element(((By.XPATH, '//*[@id="sylius-cart-button"]/button')), text))

    def get_cart_button(self):
        return self.driver.find_element(*MainPage.cart_button)

    def get_to_checkout(self):
        self.driver.find_element(*MainPage.cart_button).click()
        self.driver.find_element(*MainPage.checkout_button).click()
        checkout_page = checkoutPage.CheckoutPage(self.driver)
        return checkout_page

