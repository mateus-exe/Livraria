import psycopg2

# COLOQUE SUAS CREDENCIAIS DO POSTGRESQL AQUI:
# Obs: O banco de dados 'livraria_db' já precisa estar criado no seu servidor Postgres.
DB_CONFIG = {
    'dbname': 'livraria_db',
    'user': 'postgres',
    'password': '123',  # Mude para sua senha
    'host': 'localhost',
    'port': '5432'
}

def get_connection():
    return psycopg2.connect(**DB_CONFIG)

def init_db():
    with get_connection() as conn:
        with conn.cursor() as c:
            c.execute("""
                CREATE TABLE IF NOT EXISTS autores (id SERIAL PRIMARY KEY, nome TEXT, nacionalidade TEXT);
                CREATE TABLE IF NOT EXISTS editoras (id SERIAL PRIMARY KEY, nome TEXT, endereco TEXT, telefone TEXT);
                CREATE TABLE IF NOT EXISTS livros (id SERIAL PRIMARY KEY, titulo TEXT, isbn TEXT, ano_publicacao INTEGER, preco NUMERIC, estoque INTEGER, id_editora INTEGER REFERENCES editoras(id));
                CREATE TABLE IF NOT EXISTS clientes (id SERIAL PRIMARY KEY, nome TEXT, cpf TEXT, email TEXT, telefone TEXT);
                CREATE TABLE IF NOT EXISTS funcionarios (id SERIAL PRIMARY KEY, nome TEXT, cargo TEXT, salario NUMERIC);
                
                CREATE TABLE IF NOT EXISTS livro_autor (id_livro INTEGER REFERENCES livros(id), id_autor INTEGER REFERENCES autores(id), PRIMARY KEY(id_livro, id_autor));
                CREATE TABLE IF NOT EXISTS vendas (id SERIAL PRIMARY KEY, id_cliente INTEGER REFERENCES clientes(id), id_funcionario INTEGER REFERENCES funcionarios(id), data_venda DATE);
                CREATE TABLE IF NOT EXISTS itens_venda (id SERIAL PRIMARY KEY, id_venda INTEGER REFERENCES vendas(id), id_livro INTEGER REFERENCES livros(id), quantidade INTEGER, preco_unitario NUMERIC);
            """)
        conn.commit()
