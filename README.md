# 🛒 Sistema de Vendas

Sistema completo de gerenciamento de vendas, com autenticação de usuários, controle de produtos, registro de vendas e histórico de transações.

## Tecnologias Utilizadas

- **Python (puro)** – Backend com manipulação direta de rotas, sem frameworks.
- **HTML + CSS** – Interfaces modernas com design responsivo e profissional.
- **MySQL** – Banco de dados relacional com integração via PyMySQL.
- **Jinja2** – Template engine para renderização dinâmica das páginas.

## Funcionalidades

- Autenticação com verificação de login e senha via banco de dados.
- Página de vendas com:
  - Seleção de produtos com preço.
  - Cálculo automático do subtotal.
  - Busca de endereço via CEP (integração com a API ViaCEP).
  - Registro da data da venda e endereço de entrega.
- Página de histórico de vendas (registro).
- Botões de navegação fluida entre páginas.
- Layout unificado e consistente com CSS embutido.

## Estrutura do Projeto

Sistema-de-vendas/ ├── main.py # Backend principal com rotas e integração ao banco ├── module/ │ └── cep_api.py # Módulo para consulta de CEP via API ├── templates/ │ ├── login.html │ ├── vendas.html │ └── registro.html ├── vendas_db (MySQL) # Banco de dados com tabelas: usuarios, vendas

markdown
Copiar
Editar

## Como Executar

1. Clone este repositório:
git clone https://github.com/edwardmth/Sistema-de-vendas.git

csharp
Copiar
Editar

2. Instale as dependências:
pip install PyMySQL Jinja2

markdown
Copiar
Editar

3. Configure o banco de dados MySQL com as tabelas esperadas.

4. Execute o sistema:
python main.py

yaml
Copiar
Editar

Acesse o sistema via navegador: [http://localhost:8000/login](http://localhost:8000/login)

## Observações

- Este projeto foi desenvolvido do zero, sem uso de frameworks, com foco total na compreensão da lógica por trás de cada etapa.
- Ideal para fins didáticos, acadêmicos ou para empresas que desejam uma solução simples e eficiente.

---

### Desenvolvido por
[Matheus Duarte](https://github.com/edwardmth)