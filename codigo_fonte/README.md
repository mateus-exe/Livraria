# Aplicação Livraria

Esta é uma aplicação de gerenciamento de livraria desenvolvida em Python.
Possui interface gráfica (GUI) usando `customtkinter` e acesso a banco de dados PostgreSQL.

## Pré-requisitos

1. **Python 3.x** instalado.
2. **PostgreSQL** instalado e rodando.
3. Crie um banco de dados vazio chamado `livraria_db` no seu servidor PostgreSQL.

## Configuração do Banco de Dados

Abra o arquivo `database.py` e configure as credenciais do seu banco de dados PostgreSQL (usuário, senha, etc):

```python
DB_CONFIG = {
    'dbname': 'livraria_db',
    'user': 'postgres',      # Seu usuário
    'password': '123',       # Sua senha do Postgres
    'host': 'localhost',
    'port': '5432'
}
```

## Instalação das Dependências

Abra o terminal na pasta do projeto e execute:

```bash
pip install -r requirements.txt
```

## Como Executar

Para rodar a aplicação com Interface Gráfica, execute:

```bash
python app.py
```

