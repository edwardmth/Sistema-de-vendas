import pymysql

print("🔍 Testando conexão via PyMySQL...")

try:
    conexao = pymysql.connect(
        host='127.0.0.1',
        user='root',
        password='8077',
        database='vendas_db',
        port=3306,
        connect_timeout=5
    )
    print("✅ Conectado com sucesso via PyMySQL!")
    conexao.close()
except Exception as e:
    print(f"🚨 Erro ao conectar com PyMySQL: {e}")
