from database import get_connection

def criar(nome, cargo, salario):
    with get_connection() as conn:
        with conn.cursor() as c:
            c.execute('INSERT INTO funcionarios (nome, cargo, salario) VALUES (%s, %s, %s)', (nome, cargo, salario))
        conn.commit()

def listar():
    with get_connection() as conn:
        with conn.cursor() as c:
            c.execute('SELECT * FROM funcionarios')
            return c.fetchall()

def atualizar(id_funcionario, nome, cargo, salario):
    with get_connection() as conn:
        with conn.cursor() as c:
            c.execute('UPDATE funcionarios SET nome=%s, cargo=%s, salario=%s WHERE id=%s', (nome, cargo, salario, id_funcionario))
        conn.commit()

def deletar(id_funcionario):
    with get_connection() as conn:
        with conn.cursor() as c:
            c.execute('DELETE FROM funcionarios WHERE id=%s', (id_funcionario,))
        conn.commit()
