import sqlite3

from sqlalchemy.exc import OperationalError


class SQLFunctions:
    db_path = r'..\testCases\TMECN.db'

    def __init__(self):
        self.sql = sqlite3.connect(SQLFunctions.db_path)
        self.cursor = self.sql.cursor()

    def get_email_value(self):
        self.cursor.execute("SELECT value FROM get_values WHERE parameter='email';")
        email_value = self.cursor.fetchone()[0]
        self.cursor.execute(f"UPDATE get_values SET value = {email_value + 1}")
        self.sql.commit()
        return email_value

    def get_random_customer(self, version):
        self.cursor.execute(f"SELECT email_id FROM customers "
                            f"WHERE db_version='{version}' "
                            f"AND confirmed=1 "
                            f"ORDER BY RANDOM()")
        email_value = self.cursor.fetchone()[0]
        email = "chinacustomertme+" + str(email_value) + "@gmail.com"
        return email

    def get_random_customer_email_and_id(self, version):
        self.cursor.execute(f"SELECT email_id FROM customers "
                            f"WHERE db_version='{version}' "
                            f"AND confirmed=1 "
                            f"ORDER BY RANDOM()")
        email_value = self.cursor.fetchone()[0]
        email = "chinacustomertme+" + str(email_value) + "@gmail.com"
        return email, email_value

    def confirmed_password(self, email_value):
        self.cursor.execute(f"UPDATE customers SET confirmed=1 WHERE email_id={email_value}")
        self.sql.commit()

    def add_customer_to_database(self, email_id, company_name, vat_number, registered_address, company_phone, bank_name,
                                 bank_number, send_to_detailed_address, send_to_phone, contact_person_name,
                                 contact_person_surname, contact_person_phone, email, db_version):
        insert_query = "INSERT INTO customers (email_id, company_name, vat_number, registered_address, company_phone, " \
                       "bank_name, bank_number, send_to_detailed_address, send_to_phone, contact_person_name, " \
                       "contact_person_surname, contact_person_phone, email, db_version, confirmed) " \
                       "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        self.cursor.execute(insert_query,
                            (email_id, company_name, str(vat_number), registered_address, str(company_phone), bank_name,
                             str(bank_number), send_to_detailed_address, str(send_to_phone), contact_person_name,
                             contact_person_surname, str(contact_person_phone), email, db_version, 0))
        self.sql.commit()

    def add_company_user_to_database(self, is_admin, contact_person_name, contact_person_surname, contact_person_phone,
                                     email_id, email, parent_email_id, db_version):
        try:
            insert_query = "INSERT INTO company_user (is_admin, contact_person_name, contact_person_surname, " \
                           "contact_person_phone, email_id, email, parent_email_id, confirmed, db_version) " \
                           "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"
            self.cursor.execute(insert_query,
                                (is_admin, contact_person_name, contact_person_surname, contact_person_phone, email_id,
                                 email, parent_email_id, 0, db_version))
            self.sql.commit()
        except OperationalError as e:
            print(f"OperationalError: {e}")

    def confirm_company_user(self, email_value):
        self.cursor.execute(f"UPDATE company_user SET confirmed=1 WHERE email_id={email_value}")
        self.sql.commit()

    def search_for_customer_data_by_email(self, data, email):
        self.cursor.execute(f"SELECT {data} FROM customers "
                            f"WHERE email='{email}'")
        customer_information = self.cursor.fetchone()[0]
        return customer_information

    def close_connection(self):
        self.sql.close()
