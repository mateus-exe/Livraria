import customtkinter as ctk
from tkinter import ttk
from decimal import Decimal
from gui.widgets.components import FormField, DataTable, Toast, ConfirmDialog, EntityComboBox
from models import livro, editora, autor
from services import livro_autor

class LivrosFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        self.selected_id = None
        
        # Header
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", pady=(0, 10))
        ctk.CTkLabel(header, text="Livros", font=("", 28, "bold")).pack(side="left")
        
        self.search_entry = ctk.CTkEntry(header, placeholder_text="Buscar título...", width=200)
        self.search_entry.pack(side="right")
        self.search_entry.bind("<KeyRelease>", self.filter_data)
        
        # Content Split
        content = ctk.CTkFrame(self, fg_color="transparent")
        content.pack(fill="both", expand=True)
        
        # --- Left Form ---
        form_frame = ctk.CTkScrollableFrame(content, width=320)
        form_frame.pack(side="left", fill="y", padx=(0, 10))
        
        self.field_titulo = FormField(form_frame, "Título:")
        self.field_titulo.pack(fill="x", padx=10, pady=5)
        self.field_isbn = FormField(form_frame, "ISBN:")
        self.field_isbn.pack(fill="x", padx=10, pady=5)
        self.field_ano = FormField(form_frame, "Ano de Publicação:")
        self.field_ano.pack(fill="x", padx=10, pady=5)
        self.field_preco = FormField(form_frame, "Preço (R$):")
        self.field_preco.pack(fill="x", padx=10, pady=5)
        self.field_estoque = FormField(form_frame, "Estoque (unidades):")
        self.field_estoque.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(form_frame, text="Editora:", anchor="w").pack(fill="x", padx=10, pady=(5,0))
        self.combo_editora = EntityComboBox(form_frame)
        self.combo_editora.pack(fill="x", padx=10, pady=(0, 10))
        
        # Buttons Form
        self.btn_save = ctk.CTkButton(form_frame, text="Salvar", command=self.save, fg_color="#38bdf8", text_color="#0f0f23", hover_color="#0ea5e9")
        self.btn_save.pack(fill="x", padx=10, pady=(15, 5))
        self.btn_delete = ctk.CTkButton(form_frame, text="Remover", command=self.delete, fg_color="transparent", text_color="#ef4444", hover_color="#1e293b", state="disabled")
        self.btn_delete.pack(fill="x", padx=10, pady=5)
        ctk.CTkButton(form_frame, text="Limpar", command=self.clear_form, fg_color="transparent", border_width=1, border_color="#1e293b", text_color="#f1f5f9", hover_color="#16213e").pack(fill="x", padx=10, pady=5)
        
        # --- Authors Section (Only active when editing) ---
        self.authors_section = ctk.CTkFrame(form_frame)
        self.authors_section.pack(fill="x", padx=10, pady=20)
        
        ctk.CTkLabel(self.authors_section, text="Autores Associados", font=("", 14, "bold")).pack(pady=5)
        self.combo_autor = EntityComboBox(self.authors_section)
        self.combo_autor.pack(fill="x", padx=10, pady=5)
        self.btn_add_autor = ctk.CTkButton(self.authors_section, text="Adicionar Autor", command=self.add_author, fg_color="transparent", border_width=1, border_color="#38bdf8", text_color="#38bdf8", hover_color="#16213e")
        self.btn_add_autor.pack(fill="x", padx=10, pady=5)
        
        # List of authors for the selected book
        self.authors_list = DataTable(self.authors_section, columns=("ID", "Nome"), height=4)
        self.authors_list.column("ID", width=30)
        self.authors_list.pack(fill="x", padx=10, pady=5)
        self.btn_rem_autor = ctk.CTkButton(self.authors_section, text="Remover Selecionado", command=self.remove_author, fg_color="transparent", text_color="#ef4444", hover_color="#1e293b")
        self.btn_rem_autor.pack(fill="x", padx=10, pady=(0,10))
        
        # --- Right Table ---
        table_frame = ctk.CTkFrame(content)
        table_frame.pack(side="right", fill="both", expand=True)
        
        self.table = DataTable(table_frame, columns=("ID", "Título", "Editora", "Preço", "Estoque"))
        self.table.column("ID", width=40, stretch=False)
        self.table.column("Preço", width=80, stretch=False)
        self.table.column("Estoque", width=70, stretch=False)
        self.table.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.table.yview)
        self.table.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y", pady=5)
        
        self.table.bind("<<TreeviewSelect>>", self.on_select)
        
        # Initial Loads
        self.all_data = []
        self.load_editoras_and_autores()
        self.load_data()
        self.set_authors_state("disabled")
        
    def set_authors_state(self, state):
        self.combo_autor.configure(state=state)
        self.btn_add_autor.configure(state=state)
        self.btn_rem_autor.configure(state=state)
        
    def load_editoras_and_autores(self):
        try:
            eds = editora.listar()
            self.combo_editora.set_values(eds, lambda x: f"{x[1]}")
            auts = autor.listar()
            self.combo_autor.set_values(auts, lambda x: f"{x[1]}")
        except Exception as e:
            print("Erro ao carregar combos:", e)

    def load_data(self):
        for row in self.table.get_children():
            self.table.delete(row)
        self.all_data = livro.listar()
        eds = {e[0]: e[1] for e in editora.listar()} # dict de id_editora -> nome_editora
        
        for row_data in self.all_data:
            # (id, titulo, isbn, ano_publicacao, preco, estoque, id_editora)
            ed_nome = eds.get(row_data[6], "Desconhecida")
            preco_fmt = f"R$ {float(row_data[4]):.2f}"
            display = (row_data[0], row_data[1], ed_nome, preco_fmt, row_data[5])
            self.table.insert("", "end", values=display, tags=(repr(row_data),))
            
    def filter_data(self, event=None):
        query = self.search_entry.get().lower()
        for row in self.table.get_children():
            self.table.delete(row)
        eds = {e[0]: e[1] for e in editora.listar()}
        
        for row_data in self.all_data:
            if query in str(row_data[1]).lower():
                ed_nome = eds.get(row_data[6], "Desconhecida")
                preco_fmt = f"R$ {float(row_data[4]):.2f}"
                display = (row_data[0], row_data[1], ed_nome, preco_fmt, row_data[5])
                self.table.insert("", "end", values=display, tags=(repr(row_data),))

    def load_authors_for_book(self):
        for row in self.authors_list.get_children():
            self.authors_list.delete(row)
        if not self.selected_id: return
        
        auts = livro_autor.listar_por_livro(self.selected_id)
        for a in auts:
            self.authors_list.insert("", "end", values=(a[0], a[1]))

    def on_select(self, event):
        selection = self.table.selection()
        if selection:
            item = self.table.item(selection[0])
            row_data = eval(item['tags'][0]) # Recupera os dados originais brutos
            
            self.selected_id = row_data[0]
            self.field_titulo.set(row_data[1])
            self.field_isbn.set(row_data[2])
            self.field_ano.set(row_data[3])
            self.field_preco.set(row_data[4])
            self.field_estoque.set(row_data[5])
            self.combo_editora.set_by_id(row_data[6])
            
            self.btn_save.configure(text="Atualizar")
            self.btn_delete.configure(state="normal")
            
            self.set_authors_state("normal")
            self.load_authors_for_book()
            
    def clear_form(self):
        self.selected_id = None
        self.field_titulo.clear()
        self.field_isbn.clear()
        self.field_ano.clear()
        self.field_preco.clear()
        self.field_estoque.clear()
        
        self.btn_save.configure(text="Salvar")
        self.btn_delete.configure(state="disabled")
        if self.table.selection():
            self.table.selection_remove(self.table.selection())
            
        for row in self.authors_list.get_children():
            self.authors_list.delete(row)
        self.set_authors_state("disabled")
        
    def save(self):
        titulo = self.field_titulo.get()
        isbn = self.field_isbn.get()
        id_ed = self.combo_editora.get_selected_id()
        
        if not titulo or not id_ed:
            Toast.show(self.winfo_toplevel(), "Título e Editora são obrigatórios!", is_error=True)
            return
            
        try:
            ano = int(self.field_ano.get() or 0)
            preco = float(self.field_preco.get().replace(",", ".") or 0.0)
            estoque = int(self.field_estoque.get() or 0)
            
            if self.selected_id:
                livro.atualizar(self.selected_id, titulo, isbn, ano, preco, estoque, id_ed)
                Toast.show(self.winfo_toplevel(), "Livro atualizado!")
            else:
                new_id = livro.criar(titulo, isbn, ano, preco, estoque, id_ed)
                Toast.show(self.winfo_toplevel(), "Livro cadastrado! Agora você pode adicionar autores.")
                
            self.load_data()
            self.clear_form()
        except Exception as e:
            Toast.show(self.winfo_toplevel(), f"Erro: {e}", is_error=True)
            
    def delete(self):
        if not self.selected_id: return
        dialog = ConfirmDialog(self.winfo_toplevel(), "Remover", "Deseja remover este livro?")
        if dialog.result:
            try:
                livro.deletar(self.selected_id)
                Toast.show(self.winfo_toplevel(), "Removido!")
                self.load_data()
                self.clear_form()
            except Exception as e:
                Toast.show(self.winfo_toplevel(), "Não foi possível remover (verifique associações).", is_error=True)
                
    def add_author(self):
        if not self.selected_id: return
        id_autor = self.combo_autor.get_selected_id()
        if not id_autor: return
        
        try:
            livro_autor.associar(self.selected_id, id_autor)
            Toast.show(self.winfo_toplevel(), "Autor associado!")
            self.load_authors_for_book()
        except Exception as e:
            Toast.show(self.winfo_toplevel(), f"Erro (talvez já associado): {e}", is_error=True)

    def remove_author(self):
        if not self.selected_id: return
        sel = self.authors_list.selection()
        if not sel:
            Toast.show(self.winfo_toplevel(), "Selecione um autor na pequena lista para remover.", is_error=True)
            return
            
        id_autor = self.authors_list.item(sel[0])['values'][0]
        try:
            livro_autor.desassociar(self.selected_id, id_autor)
            Toast.show(self.winfo_toplevel(), "Associação removida!")
            self.load_authors_for_book()
        except Exception as e:
            Toast.show(self.winfo_toplevel(), f"Erro: {e}", is_error=True)
