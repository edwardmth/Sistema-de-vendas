Sistema de Vendas
Este é um sistema de vendas desenvolvido em Python. Ele permite registrar vendas, consultar CEPs e gerenciar o histórico de vendas.
Requisitos
Antes de rodar o sistema, você precisa garantir que as dependências necessárias estão instaladas.
Instalando Dependências

Clone o repositório:
bashCopiargit clone https://github.com/edwardmth/Sistema-de-vendas.git
cd Sistema-de-vendas

Crie um ambiente virtual (opcional, mas recomendado):
bashCopiarpython -m venv venv
source venv/bin/activate  # No Linux/MacOS
venv\Scripts\activate     # No Windows

Instale as dependências:
bashCopiarpip install -r requirements.txt
Nota: Se o arquivo requirements.txt não existir, instale manualmente as dependências que o projeto usa, como o PyMySQL:
bashCopiarpip install PyMySQL jinja2


Rodando o Sistema
Após instalar as dependências, inicie o servidor com o seguinte comando:
bashCopiarpython main.py
O servidor será iniciado e estará disponível em http://localhost:8000.
Realizando Testes
Se você tiver testes automatizados no seu projeto (por exemplo, usando unittest), pode rodá-los com o seguinte comando:
bashCopiarpython -m unittest discover tests/
Isso irá procurar pelos testes na pasta tests/ e executá-los.

<!-- Atualização de teste -->
## Atualização 2025-04-07
Este projeto está em desenvolvimento ativo.
