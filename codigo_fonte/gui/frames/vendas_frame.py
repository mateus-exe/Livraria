import customtkinter as ctk
from tkinter import ttk
from gui.widgets.components import DataTable, Toast, ConfirmDialog, EntityComboBox
from models import livro, cliente, funcionario
from services import venda

class VendasFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        self.carrinho = [] # Lista de tuplas (id_livro, titulo, preco, qtde, subtotal)
        
        # Header
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", pady=(0, 10))
        ctk.CTkLabel(header, text="Registrar Venda", font=("", 28, "bold")).pack(side="left")
        
        # Layout principal
        content = ctk.CTkFrame(self, fg_color="transparent")
        content.pack(fill="both", expand=True)
        
        # Left Panel (Inputs)
        left_panel = ctk.CTkFrame(content, width=350)
        left_panel.pack(side="left", fill="y", padx=(0, 10))
        
        ctk.CTkLabel(left_panel, text="1. Identificação", font=("", 16, "bold")).pack(pady=10, padx=10, anchor="w")
        
        ctk.CTkLabel(left_panel, text="Funcionário:").pack(padx=10, anchor="w")
        self.combo_func = EntityComboBox(left_panel)
        self.combo_func.pack(fill="x", padx=10, pady=(0, 10))
        
        ctk.CTkLabel(left_panel, text="Cliente:").pack(padx=10, anchor="w")
        self.combo_cli = EntityComboBox(left_panel)
        self.combo_cli.pack(fill="x", padx=10, pady=(0, 20))
        
        ctk.CTkLabel(left_panel, text="2. Adicionar Livro", font=("", 16, "bold")).pack(pady=10, padx=10, anchor="w")
        
        ctk.CTkLabel(left_panel, text="Selecione o Livro:").pack(padx=10, anchor="w")
        self.combo_livro = EntityComboBox(left_panel)
        self.combo_livro.pack(fill="x", padx=10, pady=(0, 10))
        
        ctk.CTkLabel(left_panel, text="Quantidade:").pack(padx=10, anchor="w")
        self.spin_qtde = ctk.CTkEntry(left_panel)
        self.spin_qtde.insert(0, "1")
        self.spin_qtde.pack(fill="x", padx=10, pady=(0, 10))
        
        self.btn_add = ctk.CTkButton(left_panel, text="Adicionar ao Carrinho", command=self.add_to_cart, fg_color="transparent", border_width=1, border_color="#38bdf8", text_color="#38bdf8", hover_color="#16213e")
        self.btn_add.pack(fill="x", padx=10, pady=10)
        
        # Right Panel (Cart)
        right_panel = ctk.CTkFrame(content)
        right_panel.pack(side="right", fill="both", expand=True)
        
        ctk.CTkLabel(right_panel, text="📋 Carrinho de Compras", font=("", 16, "bold")).pack(pady=10, padx=10, anchor="w")
        
        self.table = DataTable(right_panel, columns=("ID", "Título", "Qtd", "Preço Un.", "Subtotal"))
        self.table.column("ID", width=40, stretch=False)
        self.table.column("Qtd", width=50, stretch=False)
        self.table.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.btn_rem = ctk.CTkButton(right_panel, text="Remover Selecionado", command=self.rem_from_cart, fg_color="transparent", text_color="#ef4444", hover_color="#1e293b")
        self.btn_rem.pack(anchor="e", padx=10, pady=5)
        
        # Footer (Total & Confirm)
        footer = ctk.CTkFrame(right_panel)
        footer.pack(fill="x", padx=10, pady=10)
        
        self.lbl_total = ctk.CTkLabel(footer, text="TOTAL: R$ 0,00", font=("", 24, "bold"), text_color="#34d399")
        self.lbl_total.pack(side="left", padx=20, pady=20)
        
        self.btn_confirm = ctk.CTkButton(footer, text="CONFIRMAR VENDA", fg_color="#38bdf8", text_color="#0f0f23", hover_color="#0ea5e9", font=("", 16, "bold"), height=40, command=self.confirmar_venda)
        self.btn_confirm.pack(side="right", padx=20, pady=20)
        
        self.load_data()
        
    def load_data(self):
        try:
            funcs = funcionario.listar()
            self.combo_func.set_values(funcs, lambda f: f"{f[1]} ({f[2]})") # Nome (Cargo)
            
            clis = cliente.listar()
            self.combo_cli.set_values(clis, lambda c: f"{c[1]} - {c[2]}") # Nome - CPF
            
            self.refresh_books()
        except Exception as e:
            print("Erro ao carregar dados vendas:", e)

    def refresh_books(self):
        livros_bd = livro.listar()
        # id, titulo, isbn, ano_publicacao, preco, estoque, id_editora
        self.livros_dict = {l[0]: l for l in livros_bd}
        
        # Filtra apenas livros com estoque > 0
        livros_disp = [l for l in livros_bd if l[5] > 0]
        self.combo_livro.set_values(livros_disp, lambda l: f"{l[1]} - R${float(l[4]):.2f} (Estoque: {l[5]})")
            
    def update_cart_view(self):
        for row in self.table.get_children():
            self.table.delete(row)
            
        total = 0.0
        for item in self.carrinho:
            # id_livro, titulo, qtde, preco_un, subtotal
            total += item[4]
            self.table.insert("", "end", values=(item[0], item[1], item[2], f"R$ {item[3]:.2f}", f"R$ {item[4]:.2f}"))
            
        self.lbl_total.configure(text=f"TOTAL: R$ {total:.2f}")

    def add_to_cart(self):
        id_livro = self.combo_livro.get_selected_id()
        if not id_livro: return
        
        try:
            qtde = int(self.spin_qtde.get())
            if qtde <= 0: raise ValueError()
        except ValueError:
            Toast.show(self.winfo_toplevel(), "Quantidade inválida!", is_error=True)
            return
            
        l_bd = self.livros_dict[id_livro]
        titulo = l_bd[1]
        preco = float(l_bd[4])
        estoque = l_bd[5]
        
        # Verifica se já está no carrinho
        qtde_carrinho = sum(item[2] for item in self.carrinho if item[0] == id_livro)
        if qtde_carrinho + qtde > estoque:
            Toast.show(self.winfo_toplevel(), f"Estoque insuficiente! Disponível: {estoque}", is_error=True)
            return
            
        # Adiciona ou mescla
        encontrado = False
        for i, item in enumerate(self.carrinho):
            if item[0] == id_livro:
                nova_qtde = item[2] + qtde
                self.carrinho[i] = (id_livro, titulo, nova_qtde, preco, nova_qtde * preco)
                encontrado = True
                break
                
        if not encontrado:
            self.carrinho.append((id_livro, titulo, qtde, preco, qtde * preco))
            
        self.update_cart_view()
        self.spin_qtde.delete(0, 'end')
        self.spin_qtde.insert(0, "1")

    def rem_from_cart(self):
        sel = self.table.selection()
        if not sel: return
        
        id_livro = int(self.table.item(sel[0])['values'][0])
        self.carrinho = [item for item in self.carrinho if item[0] != id_livro]
        self.update_cart_view()
        
    def confirmar_venda(self):
        if not self.carrinho:
            Toast.show(self.winfo_toplevel(), "Carrinho vazio!", is_error=True)
            return
            
        id_func = self.combo_func.get_selected_id()
        id_cli = self.combo_cli.get_selected_id()
        
        if not id_func or not id_cli:
            Toast.show(self.winfo_toplevel(), "Selecione o Funcionário e o Cliente!", is_error=True)
            return
            
        dialog = ConfirmDialog(self.winfo_toplevel(), "Confirmar Venda", f"Deseja finalizar a venda no valor de {self.lbl_total.cget('text')}?")
        if dialog.result:
            try:
                # Prepara os itens: lista de (id_livro, qtde)
                itens = [(item[0], item[2]) for item in self.carrinho]
                venda.registrar_venda(id_cli, id_func, itens)
                
                Toast.show(self.winfo_toplevel(), "Venda registrada com sucesso! Estoque atualizado.")
                self.carrinho = []
                self.update_cart_view()
                self.refresh_books() # Atualiza estoque nos comboboxes
            except Exception as e:
                Toast.show(self.winfo_toplevel(), f"Erro ao registrar venda: {e}", is_error=True)
