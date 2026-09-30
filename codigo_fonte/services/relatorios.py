from database import get_connection

def vendas_por_periodo_e_funcionario(data_inicio, data_fim, id_funcionario):
    with get_connection() as conn:
        with conn.cursor() as c:
            c.execute("""
                SELECT v.id, v.data_venda, cl.nome, sum(i.quantidade * i.preco_unitario) 
                FROM vendas v
                JOIN clientes cl ON v.id_cliente = cl.id
                JOIN itens_venda i ON v.id = i.id_venda
                WHERE v.id_funcionario = %s AND v.data_venda BETWEEN %s AND %s
                GROUP BY v.id, cl.nome
            """, (id_funcionario, data_inicio, data_fim))
            return c.fetchall()

def livros_mais_vendidos():
    with get_connection() as conn:
        with conn.cursor() as c:
            c.execute("""
                SELECT l.titulo, SUM(i.quantidade) as total_vendido
                FROM itens_venda i
                JOIN livros l ON i.id_livro = l.id
                GROUP BY l.id, l.titulo
                ORDER BY total_vendido DESC
            """)
            return c.fetchall()

def faturamento_por_cliente():
    with get_connection() as conn:
        with conn.cursor() as c:
            c.execute("""
                SELECT cl.nome, SUM(i.quantidade * i.preco_unitario) as faturamento
                FROM vendas v
                JOIN clientes cl ON v.id_cliente = cl.id
                JOIN itens_venda i ON v.id = i.id_venda
                GROUP BY cl.id, cl.nome
                ORDER BY faturamento DESC
            """)
            return c.fetchall()
