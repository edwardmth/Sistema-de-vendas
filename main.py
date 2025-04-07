import os
import urllib.parse
import json
from http.server import SimpleHTTPRequestHandler, HTTPServer
from jinja2 import Environment, FileSystemLoader
from database.db_config import create_connection
from modules.cep_api import consultar_cep

env = Environment(loader=FileSystemLoader('templates'))

class ServidorHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.redirect('/login')
        elif self.path == '/login':
            self.render_template('login.html')
        elif self.path == '/vendas':
            self.render_template('vendas.html')
        elif self.path == '/registro':
            self.exibir_historico()
        elif self.path.startswith('/static/'):
            self.serve_static()
        else:
            self.send_error(404, "Rota não encontrada")

    def do_POST(self):
        if self.path == '/login':
            self.tratar_login()
        elif self.path == '/registro':
            self.tratar_registro()
        elif self.path == '/consultar-cep':
            self.tratar_cep()
        else:
            self.send_error(404, "Rota POST não encontrada.")

    def tratar_login(self):
        length = int(self.headers['Content-Length'])
        body = self.rfile.read(length).decode()
        data = urllib.parse.parse_qs(body)

        usuario = data.get('usuario', [''])[0]
        senha = data.get('senha', [''])[0]

        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE login = %s AND senha = %s", (usuario, senha))
        resultado = cursor.fetchone()
        conn.close()

        if resultado:
            self.send_response(303)
            self.send_header('Location', '/vendas')
            self.end_headers()
        else:
            self.render_template('login.html', {'erro': 'Credenciais inválidas'})

    def tratar_cep(self):
        length = int(self.headers['Content-Length'])
        body = self.rfile.read(length).decode()
        data = urllib.parse.parse_qs(body)
        cep = data.get('cep', [''])[0]

        endereco = consultar_cep(cep)
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(endereco or {}).encode())

    def tratar_registro(self):
        length = int(self.headers['Content-Length'])
        body = self.rfile.read(length).decode()
        data = urllib.parse.parse_qs(body)

        nome = data.get('nome', [''])[0]
        produto = data.get('produto', [''])[0]
        preco = float(data.get('preco', ['0'])[0])
        data_venda = data.get('data_venda', [''])[0]
        cep = data.get('cep', [''])[0]
        rua = data.get('rua', [''])[0]
        bairro = data.get('bairro', [''])[0]
        cidade = data.get('cidade', [''])[0]
        estado = data.get('estado', [''])[0]

        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO vendas (nome, produto, preco, data_venda, cep, rua, bairro, cidade, estado)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (nome, produto, preco, data_venda, cep, rua, bairro, cidade, estado))
        conn.commit()
        conn.close()

        self.send_response(303)
        self.send_header('Location', '/registro')
        self.end_headers()

    def exibir_historico(self):
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT nome, produto, preco, data_venda FROM vendas ORDER BY id DESC")
        vendas = cursor.fetchall()
        conn.close()
        self.render_template('registro.html', {'vendas': vendas})

    def serve_static(self):
        file_path = self.path.lstrip('/')
        if os.path.exists(file_path):
            self.send_response(200)
            if file_path.endswith('.css'):
                self.send_header('Content-type', 'text/css')
            elif file_path.endswith('.js'):
                self.send_header('Content-type', 'application/javascript')
            elif file_path.endswith('.png'):
                self.send_header('Content-type', 'image/png')
            elif file_path.endswith('.jpg') or file_path.endswith('.jpeg'):
                self.send_header('Content-type', 'image/jpeg')
            else:
                self.send_header('Content-type', 'application/octet-stream')
            self.end_headers()
            with open(file_path, 'rb') as file:
                self.wfile.write(file.read())
        else:
            self.send_error(404, 'Arquivo não encontrado')

    def render_template(self, template_name, context=None):
        if context is None:
            context = {}
        template = env.get_template(template_name)
        content = template.render(context)
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(content.encode('utf-8'))

    def redirect(self, location):
        self.send_response(303)
        self.send_header('Location', location)
        self.end_headers()

if __name__ == '__main__':
    host = 'localhost'
    port = 8000
    with HTTPServer((host, port), ServidorHandler) as server:
        print(f"Servidor rodando em http://{host}:{port}")
        server.serve_forever()
