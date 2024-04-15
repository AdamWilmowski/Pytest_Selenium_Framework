import json
import mariadb
from TestData.Secrets import Secrets
from utilities.mariaDBqueries import MariaDBSQLQueries


class MariaDBConnector:
    def __init__(self, db_version):
        self.sql = mariadb.connect(
                    host="172.25.130.21",
                    port=3306,
                    user=Secrets.maria_db_user,
                    password=Secrets.maria_db_password,
                    database=db_version)
        self.cursor = self.sql.cursor(dictionary=True)
        self.queries = MariaDBSQLQueries()

    def get_basic_products(self):
        sql_query = MariaDBSQLQueries.basic_products_query()
        self.cursor.execute(sql_query)
        result = self.cursor.fetchall()
        with open("../JSON_files/products_data_raw.json", "w") as f:
            json.dump(result, f, indent=4)

    def get_heavy_products(self):
        sql_query = MariaDBSQLQueries.heavy_products_query()
        self.cursor.execute(sql_query)
        result = self.cursor.fetchall()
        with open("../JSON_files/products_data_raw.json", "w") as f:
            json.dump(result, f, indent=4)

    def get_expensive_products(self):
        sql_query = MariaDBSQLQueries.expensive_products_query()
        self.cursor.execute(sql_query)
        result = self.cursor.fetchall()
        with open("../JSON_files/products_data_raw.json", "w") as f:
            json.dump(result, f, indent=4)
