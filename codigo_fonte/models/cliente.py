from database import get_connection

def criar(nome, cpf, email, telefone):
    with get_connection() as conn:
        with conn.cursor() as c:
            c.execute('INSERT INTO clientes (nome, cpf, email, telefone) VALUES (%s, %s, %s, %s)', (nome, cpf, email, telefone))
        conn.commit()

def listar():
    with get_connection() as conn:
        with conn.cursor() as c:
            c.execute('SELECT * FROM clientes')
            return c.fetchall()

def atualizar(id_cliente, nome, cpf, email, telefone):
    with get_connection() as conn:
        with conn.cursor() as c:
            c.execute('UPDATE clientes SET nome=%s, cpf=%s, email=%s, telefone=%s WHERE id=%s', (nome, cpf, email, telefone, id_cliente))
        conn.commit()

def deletar(id_cliente):
    with get_connection() as conn:
        with conn.cursor() as c:
            c.execute('DELETE FROM clientes WHERE id=%s', (id_cliente,))
        conn.commit()
