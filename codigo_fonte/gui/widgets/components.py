import customtkinter as ctk
from tkinter import ttk

class FormField(ctk.CTkFrame):
    """Componente de formulário padronizado com Label e Entry."""
    def __init__(self, master, label_text, width=200, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.label = ctk.CTkLabel(self, text=label_text, anchor="w", text_color="#cbd5e1", font=("", 14))
        self.label.pack(fill="x", pady=(0, 2))
        
        # Cores mais neutras e visíveis para os campos (Cinza Ardósia)
        self.entry = ctk.CTkEntry(self, width=width, fg_color="#1e293b", border_color="#334155", 
                                  border_width=1, text_color="white", font=("", 14))
        self.entry.pack(fill="x", pady=(0, 15))
        
    def get(self):
        return self.entry.get().strip()
        
    def set(self, value):
        self.entry.delete(0, 'end')
        self.entry.insert(0, str(value) if value is not None else "")
        
    def clear(self):
        self.entry.delete(0, 'end')

class DataTable(ttk.Treeview):
    """Tabela estilizada para combinar com o tema do app."""
    def __init__(self, master, columns, **kwargs):
        display_cols = [c for c in columns if c not in ("ID", "Venda ID")]
        super().__init__(master, columns=columns, show='headings', displaycolumns=display_cols, **kwargs)
        
        # Estilo
        style = ttk.Style()
        style.theme_use("default")
        
        # Ajuste de cores para melhor visibilidade e contraste
        bg_color = "#1e293b"        # Fundo da tabela (mais claro que o fundo do app)
        fg_color = "white"          # Texto das linhas
        selected_bg = "#38bdf8"     # Fundo quando selecionado
        selected_fg = "black"       # Texto quando selecionado
        heading_bg = "#0f172a"      # Fundo do cabeçalho
        
        style.configure("Treeview",
                        background=bg_color,
                        foreground=fg_color,
                        rowheight=32,
                        fieldbackground=bg_color,
                        borderwidth=1,
                        font=("", 12))  # FONTE MAIOR EXPLÍCITA PARA VISIBILIDADE
                        
        style.map('Treeview', 
                  background=[('selected', selected_bg)],
                  foreground=[('selected', selected_fg)])
        
        style.configure("Treeview.Heading",
                        background=heading_bg,
                        foreground="white",
                        relief="flat",
                        font=("", 13, "bold"))
        style.map("Treeview.Heading",
                  background=[('active', '#1e293b')])
        
        for col in columns:
            self.heading(col, text=col, anchor="center")
            self.column(col, width=120, anchor="center")

class Toast:
    """Notificação flutuante temporária (Sucesso ou Erro)."""
    @staticmethod
    def show(master, message, is_error=False, duration_ms=3000):
        color = "#ef4444" if is_error else "#34d399"
        text_color = "#ffffff" if is_error else "#0f0f23"
        
        toast = ctk.CTkLabel(master, text=message, fg_color=color, 
                             text_color=text_color, corner_radius=12, 
                             padx=20, pady=10, font=("", 14, "bold"))
        
        toast.place(relx=0.5, rely=0.9, anchor="center")
        master.after(duration_ms, toast.destroy)

class ConfirmDialog(ctk.CTkToplevel):
    """Diálogo modal para confirmação (Sim/Não)."""
    def __init__(self, master, title, message):
        super().__init__(master)
        self.title(title)
        self.geometry("400x180")
        self.result = False
        self.configure(fg_color="#1a1a2e")
        
        self.transient(master)
        self.grab_set()
        
        ctk.CTkLabel(self, text=message, font=("", 15), wraplength=350, text_color="#f1f5f9").pack(pady=35)
        
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(fill="x", padx=40)
        
        self.btn_yes = ctk.CTkButton(btn_frame, text="Confirmar", command=self.confirm, width=120, 
                                     fg_color="transparent", border_width=1, border_color="#ef4444", 
                                     text_color="#ef4444", hover_color="#3f1414")
        self.btn_yes.pack(side="left")
        
        self.btn_no = ctk.CTkButton(btn_frame, text="Cancelar", command=self.cancel, width=120,
                                    fg_color="transparent", text_color="#94a3b8", hover_color="#16213e")
        self.btn_no.pack(side="right")
        
        self.wait_window()
        
    def confirm(self):
        self.result = True
        self.destroy()
        
    def cancel(self):
        self.result = False
        self.destroy()

class EntityComboBox(ctk.CTkComboBox):
    """Combobox que exibe texto, mas guarda mapeamento para o ID do banco de dados."""
    def __init__(self, master, **kwargs):
        # Cores e fontes ajustadas para visibilidade
        super().__init__(master, fg_color="#1e293b", border_color="#334155", border_width=1, text_color="white", 
                         dropdown_fg_color="#1e293b", dropdown_text_color="white", font=("", 14),
                         dropdown_hover_color="#38bdf8", **kwargs)
        self.entity_map = {} 
        
    def set_values(self, entities, display_func=None):
        if not entities:
            self.entity_map = {}
            self.configure(values=["Vazio"])
            self.set("Vazio")
            return
            
        self.entity_map = {}
        values = []
        for ent in entities:
            ent_id = ent[0]
            display_text = display_func(ent) if display_func else str(ent[1])
            self.entity_map[display_text] = ent_id
            values.append(display_text)
            
        self.configure(values=values)
        if values:
            self.set(values[0])
        
    def get_selected_id(self):
        text = self.get()
        return self.entity_map.get(text, None)
        
    def set_by_id(self, entity_id):
        for text, eid in self.entity_map.items():
            if eid == entity_id:
                self.set(text)
                return
        if self.cget("values"):
            self.set(self.cget("values")[0])
