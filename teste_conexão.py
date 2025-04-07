import mysql.connector
import logging

logging.basicConfig(level=logging.DEBUG)

print("Iniciando teste de conexão...")

try:
    print("-> Import OK")
    print("-> Preparando conexão...")

    conn = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="8077",
        database="vendas_db",
        connection_timeout=5
    )

    print("✅ Conectado com sucesso.")
    conn.close()

except mysql.connector.Error as err:
    print(f"❌ Erro ao conectar: {err}")
except Exception as e:
    print(f"❌ Erro inesperado: {e}")