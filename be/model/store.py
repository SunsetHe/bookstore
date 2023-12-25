import logging
import os
import threading
import mysql.connector

class Store:
    database: str

    def __init__(self, db_host, db_user, db_password, db_name):
        self.database = {
            'host': db_host,
            'user': db_user,
            'password': db_password,
            'database': db_name
        }
        self.init_tables()

    def init_tables(self):
        conn = self.get_db_conn()
        cursor = conn.cursor()

        cursor.execute(
            "CREATE TABLE IF NOT EXISTS user ("
            "user_id VARCHAR(255) PRIMARY KEY, password VARCHAR(255) NOT NULL, "
            "balance INTEGER NOT NULL, token VARCHAR(255), terminal VARCHAR(255));"
        )

        cursor.execute(
            "CREATE TABLE IF NOT EXISTS user_store ("
            "user_id VARCHAR(255), store_id VARCHAR(255), PRIMARY KEY(user_id, store_id));"
        )

        cursor.execute(
            "CREATE TABLE IF NOT EXISTS store ("
            "store_id VARCHAR(255), book_id VARCHAR(255), book_info TEXT, stock_level INTEGER,"
            " PRIMARY KEY(store_id, book_id));"
        )

        cursor.execute(
            "CREATE TABLE IF NOT EXISTS new_order ("
            "order_id VARCHAR(255) PRIMARY KEY, user_id VARCHAR(255), store_id VARCHAR(255));"
        )

        cursor.execute(
            "CREATE TABLE IF NOT EXISTS new_order_detail ("
            "order_id VARCHAR(255), book_id VARCHAR(255), count INTEGER, price INTEGER,  "
            "PRIMARY KEY(order_id, book_id));"
        )

        conn.commit()
        cursor.close()

    def get_db_conn(self) -> mysql.connector.connection.MySQLConnection:
        return mysql.connector.connect(**self.database)


database_instance: Store = None
# global variable for database sync
init_completed_event = threading.Event()


def init_database():
    global database_instance
    database_instance = Store('localhost','root','kKk20030108','book_test')


def get_db_conn():
    global database_instance
    return database_instance.get_db_conn()
