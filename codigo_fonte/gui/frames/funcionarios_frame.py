import customtkinter as ctk
from tkinter import ttk
from gui.widgets.components import FormField, DataTable, Toast, ConfirmDialog
from models import funcionario

class FuncionariosFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        self.selected_id = None
        
        # Header
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", pady=(0, 10))
        ctk.CTkLabel(header, text="Funcionários", font=("", 28, "bold")).pack(side="left")
        
        self.search_entry = ctk.CTkEntry(header, placeholder_text="Buscar nome...", width=200)
        self.search_entry.pack(side="right")
        self.search_entry.bind("<KeyRelease>", self.filter_data)
        
        # Content
        content = ctk.CTkFrame(self, fg_color="transparent")
        content.pack(fill="both", expand=True)
        
        # Form (Left)
        form_frame = ctk.CTkFrame(content, width=300)
        form_frame.pack(side="left", fill="y", padx=(0, 10))
        
        self.field_nome = FormField(form_frame, "Nome:")
        self.field_nome.pack(fill="x", padx=10, pady=5)
        self.field_cargo = FormField(form_frame, "Cargo:")
        self.field_cargo.pack(fill="x", padx=10, pady=5)
        self.field_salario = FormField(form_frame, "Salário:")
        self.field_salario.pack(fill="x", padx=10, pady=5)
        
        btn_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        btn_frame.pack(fill="x", padx=10, pady=20)
        
        self.btn_save = ctk.CTkButton(btn_frame, text="Salvar", command=self.save, fg_color="#38bdf8", text_color="#0f0f23", hover_color="#0ea5e9")
        self.btn_save.pack(fill="x", pady=5)
        
        self.btn_delete = ctk.CTkButton(btn_frame, text="Remover", command=self.delete, fg_color="transparent", text_color="#ef4444", hover_color="#1e293b", state="disabled")
        self.btn_delete.pack(fill="x", pady=5)
        
        ctk.CTkButton(btn_frame, text="Limpar", command=self.clear_form, fg_color="transparent", border_width=1, border_color="#1e293b", text_color="#f1f5f9", hover_color="#16213e").pack(fill="x", pady=5)
        
        # Table (Right)
        table_frame = ctk.CTkFrame(content)
        table_frame.pack(side="right", fill="both", expand=True)
        
        self.table = DataTable(table_frame, columns=("ID", "Nome", "Cargo", "Salário"))
        self.table.column("ID", width=50, stretch=False)
        self.table.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.table.yview)
        self.table.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y", pady=5)
        
        self.table.bind("<<TreeviewSelect>>", self.on_select)
        
        self.all_data = []
        self.load_data()
        
    def load_data(self):
        for row in self.table.get_children():
            self.table.delete(row)
        self.all_data = funcionario.listar()
        for row_data in self.all_data:
            self.table.insert("", "end", values=row_data)
            
    def filter_data(self, event=None):
        query = self.search_entry.get().lower()
        for row in self.table.get_children():
            self.table.delete(row)
        for row_data in self.all_data:
            if query in str(row_data[1]).lower():
                self.table.insert("", "end", values=row_data)
                
    def on_select(self, event):
        selection = self.table.selection()
        if selection:
            item = self.table.item(selection[0])
            values = item['values']
            self.selected_id = values[0]
            self.field_nome.set(values[1])
            self.field_cargo.set(values[2])
            self.field_salario.set(values[3])
            self.btn_save.configure(text="Atualizar")
            self.btn_delete.configure(state="normal")
            
    def clear_form(self):
        self.selected_id = None
        self.field_nome.clear()
        self.field_cargo.clear()
        self.field_salario.clear()
        self.btn_save.configure(text="Salvar")
        self.btn_delete.configure(state="disabled")
        if self.table.selection():
            self.table.selection_remove(self.table.selection())
        
    def save(self):
        nome = self.field_nome.get()
        cargo = self.field_cargo.get()
        salario = self.field_salario.get()
        if not nome:
            Toast.show(self.winfo_toplevel(), "Nome é obrigatório!", is_error=True)
            return
        try:
            salario_float = float(salario) if salario else 0.0
        except ValueError:
            Toast.show(self.winfo_toplevel(), 'Salário deve ser um número!', is_error=True)
            return
        try:
            if self.selected_id:
                funcionario.atualizar(self.selected_id, nome, cargo, salario_float)
                Toast.show(self.winfo_toplevel(), "Atualizado com sucesso!")
            else:
                funcionario.criar(nome, cargo, salario_float)
                Toast.show(self.winfo_toplevel(), "Cadastrado com sucesso!")
            self.load_data()
            self.clear_form()
        except Exception as e:
            Toast.show(self.winfo_toplevel(), f"Erro: {e}", is_error=True)
            
    def delete(self):
        if not self.selected_id: return
        dialog = ConfirmDialog(self.winfo_toplevel(), "Remover", "Tem certeza que deseja remover este item?")
        if dialog.result:
            try:
                funcionario.deletar(self.selected_id)
                Toast.show(self.winfo_toplevel(), "Removido com sucesso!")
                self.load_data()
                self.clear_form()
            except Exception as e:
                Toast.show(self.winfo_toplevel(), "Não foi possível deletar. O item pode estar associado a outras partes do sistema.", is_error=True)
