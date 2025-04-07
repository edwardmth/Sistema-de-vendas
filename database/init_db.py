from db_config import create_connection

def init_database():
    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            
            # Tabela de Produtos
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS produtos (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    nome VARCHAR(100) NOT NULL,
                    preco DECIMAL(10,2) NOT NULL,
                    descricao TEXT,
                    estoque INT NOT NULL
                )
            """)
            
            # Tabela de Fornecedores
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS fornecedores (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    nome VARCHAR(100) NOT NULL,
                    cnpj VARCHAR(20) NOT NULL UNIQUE,
                    telefone VARCHAR(20)
                )
            """)
            
            # Tabela de Relação Produto-Fornecedor
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS produto_fornecedor (
                    produto_id INT,
                    fornecedor_id INT,
                    PRIMARY KEY (produto_id, fornecedor_id),
                    FOREIGN KEY (produto_id) REFERENCES produtos(id),
                    FOREIGN KEY (fornecedor_id) REFERENCES fornecedores(id)
                )
            """)
            
            # Tabela de Vendas
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS vendas (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    data_venda DATETIME NOT NULL,
                    endereco_entrega TEXT NOT NULL,
                    cep VARCHAR(10) NOT NULL,
                    rua VARCHAR(100),
                    bairro VARCHAR(100),
                    cidade VARCHAR(100),
                    estado VARCHAR(2),
                    total DECIMAL(10,2) NOT NULL
                )
            """)
            
            # Tabela de Itens de Venda
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS itens_venda (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    venda_id INT,
                    produto_id INT,
                    quantidade INT NOT NULL,
                    preco_unitario DECIMAL(10,2) NOT NULL,
                    FOREIGN KEY (venda_id) REFERENCES vendas(id),
                    FOREIGN KEY (produto_id) REFERENCES produtos(id)
                )
            """)
            
            conn.commit()
            print("Tabelas criadas com sucesso!")
        except Error as e:
            print(f"Erro ao criar tabelas: {e}")
        finally:
            conn.close()

if __name__ == "__main__":
    init_database()