import pytest
import json

import email
import imaplib
import inspect
import logging

import re
import time

from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By

from TestData.Secrets import Secrets


@pytest.mark.usefixtures("setup")
class BaseClass:

    @staticmethod
    def get_logger():
        logger_name = inspect.stack()[1][3]
        logger = logging.getLogger(logger_name)
        filehandler = logging.FileHandler('logfile.log')
        formatter = logging.Formatter("%(asctime)s :%(levelname)s : %(name)s :%(message)s")
        filehandler.setFormatter(formatter)

        logger.addHandler(filehandler)  # filehandler object

        logger.setLevel(logging.DEBUG)
        return logger

    def refresh(self):
        self.driver.refresh()

    def get_to(self, url):
        self.driver.get(url)

    def get_to_main(self):
        current_url = self.get_current_url()
        if current_url not in ["https://betacn-new.tme.hk/", "https://testcn-new.tme.hk/", "https://www.tme.cn/"]:
            url_list = current_url.split("/")
            main_url = "https://" + url_list[2]
            self.get_to(main_url)

    def get_to_admin(self):
        current_url = self.get_current_url()
        admin_url = current_url + "tme-office"
        self.get_to(admin_url)

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

    @staticmethod
    def get_hyperlink_from_message(subject="TME", search_pattern="set-password", wait_time=60):
        email_user = Secrets.email_user
        email_password = Secrets.python_email_password
        specific_subject = subject

        with open("../JSON_files/emails.json", "r") as email_file:
            email_data = json.load(email_file)

        last_email_value = email_data[search_pattern]

        def search_for_hyperlink(mail, specific_subject, search_pattern):
            mail.select("inbox")
            resp, items = mail.search(None, f'SUBJECT "{specific_subject}"')
            items = items[0].split()

            if items:
                last_two_emails = items[-2:]
                for email_id in last_two_emails:
                    resp, data = mail.fetch(email_id, "(BODY[TEXT])")
                    raw_email = data[0][1]
                    email_message = email.message_from_bytes(raw_email)
                    if email_message.is_multipart():
                        for part in email_message.get_payload():
                            if part.get_content_type() == "text/plain":
                                body = part.get_payload(decode=True)
                                email_content = body.decode()
                                match = re.search(rf"\b(https?://\S*{search_pattern}/\S*)\b", email_content)
                                if match:
                                    return match.group(1)
                    else:
                        email_content = email_message.get_payload(decode=True).decode()
                        match = re.search(rf"\b(https?://\S*{search_pattern}/\S*)\b", email_content)
                        if match:
                            return match.group(1)

        mail = imaplib.IMAP4_SSL('imap.gmail.com')
        mail.login(email_user, email_password)

        number_of_seconds = 0
        while number_of_seconds < wait_time:
            found_email = search_for_hyperlink(mail, specific_subject, search_pattern)
            if found_email != last_email_value and found_email is not None:
                mail.logout()
                email_data[search_pattern] = found_email
                with open("../JSON_files/emails.json", "w") as email_file:
                    json.dump(email_data, email_file, indent=4)
                return found_email
            number_of_seconds += 1
            time.sleep(1)

        raise TimeoutError(f"Email not received within {wait_time} seconds")
