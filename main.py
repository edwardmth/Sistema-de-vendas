from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs
import os
import mysql.connector
from jinja2 import Environment, FileSystemLoader
from database.db_config import create_connection
import json
import requests

env = Environment(loader=FileSystemLoader('templates'))

PRODUTOS = [
    {"id": 1, "nome": "Produto A", "preco": 199.90, "fornecedor": "Fornecedor X"},
    {"id": 2, "nome": "Produto B", "preco": 349.90, "fornecedor": "Fornecedor Y"},
    {"id": 3, "nome": "Produto C", "preco": 499.90, "fornecedor": "Fornecedor Z"}
]

def consultar_cep(cep):
    try:
        response = requests.get(f'https://viacep.com.br/ws/{cep}/json/', timeout=5)
        data = response.json()
        if 'erro' in data:
            return None
        return {
            'rua': data.get('logradouro', ''),
            'bairro': data.get('bairro', ''),
            'cidade': data.get('localidade', ''),
            'estado': data.get('uf', '')
        }
    except:
        return None

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/login':
            self.render_template('login.html')
        elif self.path == '/vendas':
            template = env.get_template('vendas.html')
            html = template.render(produtos=PRODUTOS)
            self.send_html(html)
        elif self.path == '/registro':
            conn = create_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT v.data, v.rua, v.bairro, v.cidade, v.estado, v.cep, v.subtotal
                FROM vendas v ORDER BY v.id DESC
            """)
            vendas = cursor.fetchall()
            conn.close()
            template = env.get_template('registro.html')
            html = template.render(vendas=vendas)
            self.send_html(html)
        elif self.path.startswith('/static/'):
            self.serve_static()
        else:
            self.send_error(404, "Página não encontrada.")

    def do_POST(self):
        if self.path == '/login':
            length = int(self.headers['Content-Length'])
            data = parse_qs(self.rfile.read(length).decode())
            login = data.get('login', [''])[0]
            senha = data.get('senha', [''])[0]

            conn = create_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM usuarios WHERE login = %s AND senha = %s", (login, senha))
            user = cursor.fetchone()
            conn.close()

            if user:
                self.send_response(303)
                self.send_header('Location', '/vendas')
                self.end_headers()
            else:
                self.send_response(303)
                self.send_header('Location', '/login')
                self.end_headers()

        elif self.path == '/registro':
            length = int(self.headers['Content-Length'])
            body = self.rfile.read(length).decode()
            data = parse_qs(body)

            data_venda = data.get('data', [''])[0]
            cep = data.get('cep', [''])[0]
            subtotal = data.get('subtotal', [''])[0]

            endereco = consultar_cep(cep)
            if not endereco:
                self.send_error(400, "CEP inválido.")
                return

            conn = create_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO vendas (data, rua, bairro, cidade, estado, cep, subtotal)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                data_venda,
                endereco['rua'],
                endereco['bairro'],
                endereco['cidade'],
                endereco['estado'],
                cep,
                subtotal
            ))
            conn.commit()
            conn.close()

            self.send_response(303)
            self.send_header('Location', '/registro')
            self.end_headers()
        else:
            self.send_error(404, "Rota POST não encontrada.")

    def render_template(self, filename, context={}):
        template = env.get_template(filename)
        html = template.render(context)
        self.send_html(html)

    def send_html(self, html):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html.encode('utf-8'))

    def serve_static(self):
        path = self.path.lstrip('/')
        if os.path.exists(path):
            self.send_response(200)
            if path.endswith('.css'):
                self.send_header('Content-type', 'text/css')
            elif path.endswith('.js'):
                self.send_header('Content-type', 'application/javascript')
            elif path.endswith('.png'):
                self.send_header('Content-type', 'image/png')
            else:
                self.send_header('Content-type', 'application/octet-stream')
            self.end_headers()
            with open(path, 'rb') as file:
                self.wfile.write(file.read())
        else:
            self.send_error(404, "Arquivo não encontrado.")

def run():
    server = HTTPServer(('localhost', 8000), RequestHandler)
    print("Servidor rodando em http://localhost:8000")
    server.serve_forever()

if __name__ == '__main__':
    run()
