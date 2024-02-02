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
        self.driver.get("https://betacn-new.tme.hk/en/")

    def back(self):
        self.driver.back()

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


    def get_hyperlinks_from_first_email(self, username, password, server, mailbox="INBOX", subject="Welcome to TME"):
        try:
            mail = imaplib.IMAP4_SSL(server)
            mail.login(username, password)

            mail.select(mailbox)

            _, data = mail.search(None, 'ALL')
            email_ids = data[0].split()

            if not email_ids:
                print("No emails found in the mailbox.")
                return []

            first_email_id = email_ids[-1]
            _, msg_data = mail.fetch(first_email_id, "(RFC822)")
            raw_email = msg_data[0][1]
            msg = email.message_from_bytes(raw_email)

            hyperlinks = []

            for part in msg.walk():
                if part.get_content_type() == "text/html":
                    email_content = part.get_payload(decode=True).decode("utf-8")

                    links = re.findall(r"\b(https?://\S+)\b", email_content)
                    hyperlinks.extend(links)

            return hyperlinks

        except Exception as e:
            print("Error:", e)

        finally:
            mail.logout()
