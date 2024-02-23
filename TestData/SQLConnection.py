import sqlite3


class SQLFunctions:
    def __init__(self):
        self.sql = sqlite3.connect('TMECN.db')
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
        email = "chinacustomertme" + str(email_value) + "@gmail.com"
        return email

    def confirmed_password(self, email_value):
        self.cursor.execute(f"UPDATE customers SET confirmed=1 WHERE email_id={email_value}")
        self.sql.commit()

    def add_customer_to_database(self, email_id, company_name, vat_number, registered_address, company_phone, bank_name,
                                 bank_number, send_to_detailed_address, send_to_phone, contact_person_name,
                                 contact_person_surname, contact_person_phone, email, db_version):
        insert_query = " INSERT INTO customers (email_id, company_name, vat_number, registered_address, company_phone, " \
                       "bank_name, bank_number, send_to_detailed_address, send_to_phone, contact_person_name, " \
                       "contact_person_surname, contact_person_phone, email, db_version, confirmed) " \
                       "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        self.cursor.execute(insert_query,
                            (email_id, company_name, str(vat_number), registered_address, str(company_phone), bank_name,
                             str(bank_number), send_to_detailed_address, str(send_to_phone), contact_person_name,
                             contact_person_surname, str(contact_person_phone), email, db_version, 0))
        self.sql.commit()

    def close_connection(self):
        self.sql.close()
