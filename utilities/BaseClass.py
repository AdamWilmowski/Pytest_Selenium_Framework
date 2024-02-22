import email
import imaplib
import inspect
import logging
import random
import re
import pytest
from selenium.common import NoSuchElementException
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from faker import Faker
from TestData.Secrets import Secrets


@pytest.mark.usefixtures("setup")
class BaseClass:

    def getLogger(self):
        loggerName = inspect.stack()[1][3]
        logger = logging.getLogger(loggerName)
        fileHandler = logging.FileHandler('logfile.log')
        formatter = logging.Formatter("%(asctime)s :%(levelname)s : %(name)s :%(message)s")
        fileHandler.setFormatter(formatter)

        logger.addHandler(fileHandler)  # filehandler object

        logger.setLevel(logging.DEBUG)
        return logger

    def refresh(self):
        self.driver.refresh()

    def get_to(self, url):
        self.driver.get(url)

    def get_to_main(self):
        current_url = self.get_current_url()
        main_url = current_url.split("/")
        self.driver.get(main_url[0])

    def back(self):
        self.driver.back()

    def get_to_by_link_text(self, text):
        self.driver.find_element(By.LINK_TEXT, text).click()

    def check_page(self, link):
        if self.driver.current_url != link:
            self.closeCookies()
            self.driver.get(link)
        else:
            self.driver.refresh()

    def get_current_url(self):
        return self.driver.current_url

    def close_cookies(self):
        try:
            self.driver.find_element(By.ID, "cookies-consent-close-icon").click()
        except NoSuchElementException:
            pass

    def stop_load(self):
        self.driver.execute_script("window.stop();")

    def open_new_window(self):
        self.driver.switch_to.new_window('window')


    def get_hyperlinks_from_message(self, subject="TME"):
        email_user = Secrets.email_user
        email_password = Secrets.python_email_password
        specific_subject = subject

        mail = imaplib.IMAP4_SSL('imap.gmail.com')

        mail.login(email_user, email_password)

        mail.select("inbox")

        resp, items = mail.search(None, f'SUBJECT "{specific_subject}"')

        items = items[0].split()

        if items:
            last_email_id = items[-1]
            resp, data = mail.fetch(last_email_id, "(BODY[TEXT])")
            raw_email = data[0][1]
            email_message = email.message_from_bytes(raw_email)
            hyperlinks = []
            if email_message.is_multipart():
                for part in email_message.get_payload():
                    if part.get_content_type() == "text/plain":
                        body = part.get_payload(decode=True)
                        email_content = body.decode()
                        links = re.findall(r"\b(https?://\S+)\b", email_content)
                        hyperlinks.extend(links)
                        return hyperlinks
            else:
                email_content = email_message.get_payload(decode=True).decode()
                links = re.findall(r"\b(https?://\S+)\b", email_content)
                hyperlinks.extend(links)
                return hyperlinks

        mail.logout()
