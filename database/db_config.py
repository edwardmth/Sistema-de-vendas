import pymysql

def create_connection():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='8077',
        database='vendas_db',
        cursorclass=pymysql.cursors.Cursor
    )
