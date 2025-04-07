import mysql.connector
from mysql.connector import Error
from datetime import datetime

class Venda:
    def __init__(self):
        """Inicializa a conexão com o banco de dados"""
        self.conn = self._criar_conexao()
        
    def _criar_conexao(self):
        """Cria e retorna uma conexão com o banco de dados"""
        try:
            conn = mysql.connector.connect(
                host='localhost',
                user='root',          # Substitua pelo seu usuário
                password='8077',       # Substitua pela sua senha
                database='vendas_db'   # Verifique se o banco existe
            )
            return conn
        except Error as e:
            print(f"Erro ao conectar ao MySQL: {e}")
            return None

    def registrar_venda(self, dados_venda):
        """
        Registra uma nova venda no banco de dados
        
        Args:
            dados_venda (dict): Dicionário contendo:
                - 'cliente' (str): Nome do cliente
                - 'endereco' (str): Endereço completo
                - 'cep' (str): CEP formatado
                - 'itens' (list): Lista de dicionários com:
                    - 'produto_id' (int)
                    - 'quantidade' (int)
                    - 'preco_unitario' (float)
        
        Returns:
            dict: {'status': bool, 'venda_id': int, 'mensagem': str}
        """
        if not self.conn:
            return {'status': False, 'mensagem': 'Sem conexão com o banco'}
        
        try:
            cursor = self.conn.cursor()
            
            # Calcula o total da venda
            total = sum(item['quantidade'] * item['preco_unitario'] for item in dados_venda['itens'])
            
            # Insere a venda principal
            cursor.execute("""
                INSERT INTO vendas 
                (data_venda, cliente, endereco_entrega, cep, total)
                VALUES (%s, %s, %s, %s, %s)
            """, (
                datetime.now(),
                dados_venda.get('cliente', ''),
                dados_venda['endereco'],
                dados_venda['cep'],
                total
            ))
            
            venda_id = cursor.lastrowid
            
            # Insere os itens da venda
            for item in dados_venda['itens']:
                cursor.execute("""
                    INSERT INTO itens_venda 
                    (venda_id, produto_id, quantidade, preco_unitario)
                    VALUES (%s, %s, %s, %s)
                """, (
                    venda_id,
                    item['produto_id'],
                    item['quantidade'],
                    item['preco_unitario']
                ))
                
                # Atualiza o estoque (opcional)
                cursor.execute("""
                    UPDATE produtos 
                    SET estoque = estoque - %s 
                    WHERE id = %s
                """, (item['quantidade'], item['produto_id']))
            
            self.conn.commit()
            return {
                'status': True,
                'venda_id': venda_id,
                'mensagem': 'Venda registrada com sucesso!'
            }
            
        except Error as e:
            self.conn.rollback()
            return {
                'status': False,
                'mensagem': f'Erro ao registrar venda: {e}'
            }
            
        finally:
            if cursor:
                cursor.close()

    def consultar_venda(self, venda_id):
        """Consulta uma venda pelo ID"""
        try:
            cursor = self.conn.cursor(dictionary=True)
            
            cursor.execute("""
                SELECT * FROM vendas 
                WHERE id = %s
            """, (venda_id,))
            
            venda = cursor.fetchone()
            
            if venda:
                cursor.execute("""
                    SELECT p.nome, i.quantidade, i.preco_unitario
                    FROM itens_venda i
                    JOIN produtos p ON i.produto_id = p.id
                    WHERE i.venda_id = %s
                """, (venda_id,))
                
                itens = cursor.fetchall()
                venda['itens'] = itens
            
            return venda
            
        except Error as e:
            print(f"Erro ao consultar venda: {e}")
            return None
            
        finally:
            if cursor:
                cursor.close()

    def listar_vendas(self, data_inicio=None, data_fim=None):
        """Lista todas as vendas no período especificado"""
        try:
            cursor = self.conn.cursor(dictionary=True)
            
            query = "SELECT * FROM vendas"
            params = []
            
            if data_inicio and data_fim:
                query += " WHERE data_venda BETWEEN %s AND %s"
                params.extend([data_inicio, data_fim])
            
            query += " ORDER BY data_venda DESC"
            
            cursor.execute(query, params)
            return cursor.fetchall()
            
        except Error as e:
            print(f"Erro ao listar vendas: {e}")
            return []
            
        finally:
            if cursor:
                cursor.close()

    def __del__(self):
        """Fecha a conexão quando o objeto é destruído"""
        if self.conn and self.conn.is_connected():
            self.conn.close()

# Teste da classe (executa apenas quando rodar este arquivo diretamente)
if __name__ == "__main__":
    print("Testando módulo de vendas...")
    
    venda = Venda()
    
    # Dados de teste
    dados_teste = {
        'cliente': 'Cliente Teste',
        'endereco': 'Rua Exemplo, 123',
        'cep': '01001000',
        'itens': [
            {'produto_id': 1, 'quantidade': 2, 'preco_unitario': 50.00},
            {'produto_id': 2, 'quantidade': 1, 'preco_unitario': 30.00}
        ]
    }
    
    # Teste de registro
    resultado = venda.registrar_venda(dados_teste)
    print("Resultado do registro:", resultado)
    
    if resultado['status']:
        # Teste de consulta
        venda_registrada = venda.consultar_venda(resultado['venda_id'])
        print("\nVenda registrada:")
        print(venda_registrada)
        
        # Teste de listagem
        print("\nÚltimas vendas:")
        print(venda.listar_vendas())