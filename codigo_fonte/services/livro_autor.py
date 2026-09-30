from database import get_connection

def associar(id_livro, id_autor):
    with get_connection() as conn:
        with conn.cursor() as c:
            c.execute('INSERT INTO livro_autor (id_livro, id_autor) VALUES (%s, %s)', (id_livro, id_autor))
        conn.commit()

def listar_por_livro(id_livro):
    with get_connection() as conn:
        with conn.cursor() as c:
            c.execute('SELECT a.* FROM autores a JOIN livro_autor la ON a.id = la.id_autor WHERE la.id_livro = %s', (id_livro,))
            return c.fetchall()

def desassociar(id_livro, id_autor):
    with get_connection() as conn:
        with conn.cursor() as c:
            c.execute('DELETE FROM livro_autor WHERE id_livro = %s AND id_autor = %s', (id_livro, id_autor))
        conn.commit()
