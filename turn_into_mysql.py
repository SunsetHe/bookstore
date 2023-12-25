import sqlite3
import mysql.connector

# 原始数据库文件路径
original_db_path = r'D:\desktop\lesson\bookstore\fe\data\book_lx.db'

# 新的数据库文件路径
new_db_path = r'D:\desktop\lesson\bookstore\fe\data\new.db'

# 连接到原始数据库
connection = sqlite3.connect(original_db_path)
cursor = connection.cursor()

# 创建新表格，只包含你需要的列
cursor.execute(
    'CREATE TABLE new_table AS SELECT id, title, author, publisher, original_title, translator, pub_year, pages, price, currency_unit, binding, isbn, author_intro, book_intro, tags FROM book;')

# 提交更改
connection.commit()

# 关闭连接
connection.close()

# SQLite database file path
sqlite_file = r'D:\desktop\lesson\bookstore\fe\data\book_lx.db'

# MySQL database connection parameters
mysql_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'kKk20030108',
    'database': 'book_test',
    'charset': 'utf8mb4',  # Explicitly set character set to UTF-8
    'collation': 'utf8mb4_unicode_ci',  # Set collation
    'raise_on_warnings': True
}

# Connect to SQLite database
sqlite_conn = sqlite3.connect(sqlite_file)
sqlite_cursor = sqlite_conn.cursor()

# Connect to MySQL database
mysql_conn = mysql.connector.connect(**mysql_config)
mysql_cursor = mysql_conn.cursor()

# Select data from SQLite table
sqlite_cursor.execute("SELECT * FROM new_table")
sqlite_data = sqlite_cursor.fetchall()

# Insert data into MySQL table
for row in sqlite_data:
    mysql_cursor.execute("""
        INSERT INTO book (id, title, author, publisher, original_title, translator, pub_year, pages, 
                          price, currency_unit, binding, isbn, author_intro, book_intro, tags)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, row)

# Commit changes and close connections
mysql_conn.commit()
mysql_conn.close()
sqlite_conn.close()

print("Data successfully transferred from SQLite to MySQL.")
