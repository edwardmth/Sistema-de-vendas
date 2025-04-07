import mysql.connector
from mysql.connector import Error

print("🔍 Iniciando teste de conexão passo a passo...")

try:
    print("⏳ Etapa 1: Criando conexão com timeout explícito...")
    conexao = mysql.connector.connect(
        host='127.0.0.1',
        port=3306,
        user='root',
        password='8077',
        database='vendas_db',
        connection_timeout=5  # 🔧 Força timeout de 5 segundos
    )

    if conexao.is_connected():
        print("✅ Conexão com o banco de dados estabelecida com sucesso!")
        conexao.close()
    else:
        print("🚫 Não foi possível conectar ao banco de dados.")

except Error as e:
    print(f"🚨 Erro ao conectar: {e}")

except Exception as e:
    print(f"🧨 Erro inesperado: {e}")
