import socket

print("Testando conexão com porta 3306 em localhost...")

s = socket.socket()
try:
    s.settimeout(5)
    s.connect(("localhost", 3306))
    print("✅ Conexão com a porta 3306 estabelecida.")
except Exception as e:
    print(f"❌ Não foi possível conectar: {e}")
finally:
    s.close()
