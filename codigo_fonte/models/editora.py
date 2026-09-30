from database import get_connection

def criar(nome, endereco, telefone):
    with get_connection() as conn:
        with conn.cursor() as c:
            c.execute('INSERT INTO editoras (nome, endereco, telefone) VALUES (%s, %s, %s)', (nome, endereco, telefone))
        conn.commit()

def listar():
    with get_connection() as conn:
        with conn.cursor() as c:
            c.execute('SELECT * FROM editoras')
            return c.fetchall()

def atualizar(id_editora, nome, endereco, telefone):
    with get_connection() as conn:
        with conn.cursor() as c:
            c.execute('UPDATE editoras SET nome=%s, endereco=%s, telefone=%s WHERE id=%s', (nome, endereco, telefone, id_editora))
        conn.commit()

def deletar(id_editora):
    with get_connection() as conn:
        with conn.cursor() as c:
            c.execute('DELETE FROM editoras WHERE id=%s', (id_editora,))
        conn.commit()
