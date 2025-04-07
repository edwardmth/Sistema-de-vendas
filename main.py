import os
import json
import urllib.request
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs
from jinja2 import Environment, FileSystemLoader
import pymysql

# Configuração do Jinja2
env = Environment(loader=FileSystemLoader('templates'))

# Conexão com o banco de dados
try:
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='8077',
        database='vendas_db',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    print("✅ Conexão com banco de dados OK!")
except Exception as e:
    print("❌ Erro de conexão com o banco de dados:", e)

# Classe principal do servidor
class RequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == '/' or self.path == '/login':
            self.render_template('login.html')
        elif self.path == '/vendas':
            self.render_template('vendas.html')
        elif self.path == '/registro':
            self.exibir_registro()
        elif self.path.startswith('/static/'):
            self.serve_static_file()
        else:
            self.send_error(404, 'Página não encontrada')

    def do_POST(self):
        if self.path == '/login':
            self.processar_login()
        elif self.path == '/registro':
            self.registrar_venda()
        elif self.path == '/consultar-cep':
            self.consultar_cep()

    def render_template(self, filename, context={}):
        template = env.get_template(filename)
        content = template.render(context).encode()
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(content)

    def serve_static_file(self):
        try:
            filepath = self.path.lstrip('/')
            with open(filepath, 'rb') as file:
                content = file.read()
                self.send_response(200)
                if filepath.endswith('.css'):
                    self.send_header('Content-Type', 'text/css')
                elif filepath.endswith('.jpg') or filepath.endswith('.jpeg'):
                    self.send_header('Content-Type', 'image/jpeg')
                elif filepath.endswith('.png'):
                    self.send_header('Content-Type', 'image/png')
                self.end_headers()
                self.wfile.write(content)
        except FileNotFoundError:
            self.send_error(404, 'Arquivo não encontrado')

    def processar_login(self):
        length = int(self.headers['Content-Length'])
        data = self.rfile.read(length).decode()
        params = parse_qs(data)
        login = params.get('login', [''])[0]
        senha = params.get('senha', [''])[0]

        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM usuarios WHERE login=%s AND senha=%s", (login, senha))
                user = cursor.fetchone()
                if user:
                    self.send_response(303)
                    self.send_header('Location', '/vendas')
                    self.end_headers()
                else:
                    self.render_template('login.html', {'erro': 'Credenciais inválidas'})
        except Exception as e:
            print("Erro no login:", e)
            self.render_template('login.html', {'erro': 'Erro interno no servidor'})

    def consultar_cep(self):
        length = int(self.headers['Content-Length'])
        data = self.rfile.read(length).decode()
        params = parse_qs(data)
        cep = params.get('cep', [''])[0]
        try:
            with urllib.request.urlopen(f'https://viacep.com.br/ws/{cep}/json/') as response:
                result = response.read()
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(result)
        except Exception as e:
            print("Erro ao buscar CEP:", e)
            self.send_error(500, 'Erro ao consultar o CEP')

    def registrar_venda(self):
        length = int(self.headers['Content-Length'])
        data = self.rfile.read(length).decode()
        params = parse_qs(data)

        nome = params.get('nome', [''])[0]
        produto = params.get('produto', [''])[0]
        data_venda = params.get('data_venda', [''])[0]
        cep = params.get('cep', [''])[0]
        rua = params.get('rua', [''])[0]
        bairro = params.get('bairro', [''])[0]
        cidade = params.get('cidade', [''])[0]
        estado = params.get('estado', [''])[0]

        endereco = f"{rua}, {bairro}, {cidade} - {estado} ({cep})"

        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO vendas (cliente_nome, produto, data_venda, endereco_entrega)
                    VALUES (%s, %s, %s, %s)
                """, (nome, produto, data_venda, endereco))
                connection.commit()
                self.send_response(303)
                self.send_header('Location', '/registro')
                self.end_headers()
        except Exception as e:
            print("Erro ao registrar venda:", e)
            self.render_template('vendas.html', {'erro': 'Erro ao registrar venda'})

    def exibir_registro(self):
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM vendas ORDER BY id DESC")
                vendas = cursor.fetchall()
                self.render_template('registro.html', {'vendas': vendas})
        except Exception as e:
            print("Erro ao exibir registro:", e)
            self.render_template('registro.html', {'vendas': []})

# Inicialização do servidor
if __name__ == '__main__':
    server = HTTPServer(('localhost', 8000), RequestHandler)
    print("🚀 Servidor rodando em http://localhost:8000")
    server.serve_forever()