from database import get_connection
import datetime

def registrar_venda(id_cliente, id_funcionario, itens):
    """
    itens: lista de tuplas (id_livro, quantidade)
    """
    with get_connection() as conn:
        with conn.cursor() as c:
            data_venda = datetime.date.today().isoformat()
            
            # Registra venda e retorna o ID inserido
            c.execute('INSERT INTO vendas (id_cliente, id_funcionario, data_venda) VALUES (%s, %s, %s) RETURNING id', (id_cliente, id_funcionario, data_venda))
            id_venda = c.fetchone()[0]
            
            for id_livro, qtde in itens:
                c.execute('SELECT preco, estoque FROM livros WHERE id=%s', (id_livro,))
                livro = c.fetchone()
                if not livro or livro[1] < qtde:
                    raise ValueError(f"Estoque insuficiente ou livro {id_livro} não encontrado.")
                preco = livro[0]
                
                c.execute('INSERT INTO itens_venda (id_venda, id_livro, quantidade, preco_unitario) VALUES (%s, %s, %s, %s)', (id_venda, id_livro, qtde, preco))
                # Atualiza estoque
                c.execute('UPDATE livros SET estoque = estoque - %s WHERE id=%s', (qtde, id_livro))
            
            # Commit automático ao sair do with conn
        conn.commit()
        return id_venda
