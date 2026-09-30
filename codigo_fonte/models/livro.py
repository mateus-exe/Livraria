from database import get_connection

def criar(titulo, isbn, ano, preco, estoque, id_editora):
    with get_connection() as conn:
        with conn.cursor() as c:
            c.execute('INSERT INTO livros (titulo, isbn, ano_publicacao, preco, estoque, id_editora) VALUES (%s, %s, %s, %s, %s, %s) RETURNING id', (titulo, isbn, ano, preco, estoque, id_editora))
            return c.fetchone()[0]
        conn.commit()

def listar():
    with get_connection() as conn:
        with conn.cursor() as c:
            c.execute('SELECT * FROM livros')
            return c.fetchall()

def atualizar(id_livro, titulo, isbn, ano, preco, estoque, id_editora):
    with get_connection() as conn:
        with conn.cursor() as c:
            c.execute('UPDATE livros SET titulo=%s, isbn=%s, ano_publicacao=%s, preco=%s, estoque=%s, id_editora=%s WHERE id=%s', (titulo, isbn, ano, preco, estoque, id_editora, id_livro))
        conn.commit()

def deletar(id_livro):
    with get_connection() as conn:
        with conn.cursor() as c:
            c.execute('DELETE FROM livros WHERE id=%s', (id_livro,))
        conn.commit()


def atualizar_estoque(id_livro, novo_estoque):
    with get_connection() as conn:
        with conn.cursor() as c:
            c.execute('UPDATE livros SET estoque = %s WHERE id=%s', (novo_estoque, id_livro))
        conn.commit()
