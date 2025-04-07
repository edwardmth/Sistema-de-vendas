import mysql.connector
from mysql.connector import Error

def create_connection():
    try:
        print("🔌 Tentando conectar ao banco de dados...")
        connection = mysql.connector.connect(
            host='localhost',         # ou outro host, se não for local
            user='root',              # substitua pelo usuário do seu MySQL
            password='8077', # substitua pela senha do seu MySQL
            database='vendas_db', # substitua pelo nome do banco
            connection_timeout=5      # evita travamento eterno
        )
        if connection.is_connected():
            print("✅ Conexão com o banco de dados estabelecida!")
            return connection
    except Error as e:
        print(f"❌ Erro ao conectar ao banco: {e}")
        return None
