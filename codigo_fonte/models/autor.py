from database import get_connection

def criar(nome, nacionalidade):
    with get_connection() as conn:
        with conn.cursor() as c:
            c.execute('INSERT INTO autores (nome, nacionalidade) VALUES (%s, %s)', (nome, nacionalidade))
        conn.commit()

def listar():
    with get_connection() as conn:
        with conn.cursor() as c:
            c.execute('SELECT * FROM autores')
            return c.fetchall()

def atualizar(id_autor, nome, nacionalidade):
    with get_connection() as conn:
        with conn.cursor() as c:
            c.execute('UPDATE autores SET nome=%s, nacionalidade=%s WHERE id=%s', (nome, nacionalidade, id_autor))
        conn.commit()

def deletar(id_autor):
    with get_connection() as conn:
        with conn.cursor() as c:
            c.execute('DELETE FROM autores WHERE id=%s', (id_autor,))
        conn.commit()
