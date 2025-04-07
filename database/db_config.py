import mysql.connector

print("🔌 Iniciando tentativa de conexão...")

try:
    print("📡 Tentando conectar ao MySQL...")
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="8077",  # <-- Substitua pela sua senha do MySQL
        database="vendas_db"
    )
    print("✅ Conexão estabelecida com sucesso!")

    cursor = conn.cursor()
    cursor.execute("SHOW TABLES")
    tabelas = cursor.fetchall()
    print("📋 Tabelas encontradas:", tabelas)

    conn.close()
except mysql.connector.Error as err:
    print(f"❌ Erro do MySQL: {err}")
except Exception as e:
    print(f"⚠️ Erro inesperado: {e}")
