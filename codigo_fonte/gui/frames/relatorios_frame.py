import customtkinter as ctk
from tkinter import ttk
from gui.widgets.components import DataTable, Toast, EntityComboBox
from services import relatorios
from models import funcionario

class RelatoriosFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        
        # Header
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", pady=(0, 10))
        ctk.CTkLabel(header, text="Relatórios", font=("", 28, "bold")).pack(side="left")
        
        # Tabs
        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(fill="both", expand=True)
        
        self.tab1 = self.tabview.add("Livros Mais Vendidos")
        self.tab2 = self.tabview.add("Faturamento por Cliente")
        self.tab3 = self.tabview.add("Vendas por Período")
        
        self.setup_tab1()
        self.setup_tab2()
        self.setup_tab3()
        
    def setup_tab1(self):
        btn = ctk.CTkButton(self.tab1, text="Gerar Relatório", command=self.load_tab1, fg_color="transparent", border_width=1, border_color="#38bdf8", text_color="#38bdf8", hover_color="#16213e")
        btn.pack(pady=10)
        
        self.table1 = DataTable(self.tab1, columns=("Livro", "Total Vendido (unidades)"))
        self.table1.pack(fill="both", expand=True, padx=10, pady=10)
        
        scroll = ttk.Scrollbar(self.table1, orient="vertical", command=self.table1.yview)
        self.table1.configure(yscrollcommand=scroll.set)
        scroll.pack(side="right", fill="y")
        
    def setup_tab2(self):
        btn = ctk.CTkButton(self.tab2, text="Gerar Relatório", command=self.load_tab2, fg_color="transparent", border_width=1, border_color="#38bdf8", text_color="#38bdf8", hover_color="#16213e")
        btn.pack(pady=10)
        
        self.table2 = DataTable(self.tab2, columns=("Cliente", "Faturamento Total (R$)"))
        self.table2.pack(fill="both", expand=True, padx=10, pady=10)
        
        scroll = ttk.Scrollbar(self.table2, orient="vertical", command=self.table2.yview)
        self.table2.configure(yscrollcommand=scroll.set)
        scroll.pack(side="right", fill="y")
        
    def setup_tab3(self):
        controls = ctk.CTkFrame(self.tab3, fg_color="transparent")
        controls.pack(fill="x", pady=10, padx=10)
        
        ctk.CTkLabel(controls, text="Vendedor:").pack(side="left", padx=5)
        self.combo_func = EntityComboBox(controls, width=150)
        self.combo_func.pack(side="left", padx=5)
        
        ctk.CTkLabel(controls, text="Início (DD/MM/YYYY):").pack(side="left", padx=(15, 5))
        self.entry_inicio = ctk.CTkEntry(controls, width=100)
        self.entry_inicio.pack(side="left", padx=5)
        
        ctk.CTkLabel(controls, text="Fim (DD/MM/YYYY):").pack(side="left", padx=(15, 5))
        self.entry_fim = ctk.CTkEntry(controls, width=100)
        self.entry_fim.pack(side="left", padx=5)
        
        self.entry_inicio.bind("<KeyRelease>", self.format_date_inicio)
        self.entry_fim.bind("<KeyRelease>", self.format_date_fim)
        
        btn = ctk.CTkButton(controls, text="Gerar", command=self.load_tab3, fg_color="transparent", border_width=1, border_color="#38bdf8", text_color="#38bdf8", hover_color="#16213e")
        btn.pack(side="left", padx=20)
        
        self.table3 = DataTable(self.tab3, columns=("Venda ID", "Data", "Cliente", "Total (R$)"))
        self.table3.column("Venda ID", width=60, stretch=False)
        self.table3.column("Data", width=100, stretch=False)
        self.table3.pack(fill="both", expand=True, padx=10, pady=10)
        
        scroll = ttk.Scrollbar(self.table3, orient="vertical", command=self.table3.yview)
        self.table3.configure(yscrollcommand=scroll.set)
        scroll.pack(side="right", fill="y")
        
        # Load combobox data
        try:
            funcs = funcionario.listar()
            self.combo_func.set_values(funcs, lambda f: f"{f[1]}")
        except Exception as e:
            print("Erro ao carregar func:", e)
            
    def format_date_inicio(self, event):
        self._format_date_entry(self.entry_inicio, event)
        
    def format_date_fim(self, event):
        self._format_date_entry(self.entry_fim, event)
        
    def _format_date_entry(self, entry, event):
        if event.keysym == 'BackSpace':
            return
            
        text = entry.get()
        digits = "".join(c for c in text if c.isdigit())
        formatted = ""
        if len(digits) > 0:
            formatted += digits[:2]
        if len(digits) > 2:
            formatted += "/" + digits[2:4]
        if len(digits) > 4:
            formatted += "/" + digits[4:8]
            
        if text != formatted:
            entry.delete(0, "end")
            entry.insert(0, formatted)

    def load_tab1(self):
        for row in self.table1.get_children(): self.table1.delete(row)
        try:
            dados = relatorios.livros_mais_vendidos()
            for d in dados:
                self.table1.insert("", "end", values=d)
            Toast.show(self.winfo_toplevel(), "Relatório gerado com sucesso!")
        except Exception as e:
            Toast.show(self.winfo_toplevel(), f"Erro: {e}", is_error=True)
            
    def load_tab2(self):
        for row in self.table2.get_children(): self.table2.delete(row)
        try:
            dados = relatorios.faturamento_por_cliente()
            for d in dados:
                self.table2.insert("", "end", values=(d[0], f"R$ {d[1]:.2f}"))
            Toast.show(self.winfo_toplevel(), "Relatório gerado com sucesso!")
        except Exception as e:
            Toast.show(self.winfo_toplevel(), f"Erro: {e}", is_error=True)
            
    def load_tab3(self):
        import datetime
        for row in self.table3.get_children(): self.table3.delete(row)
        id_func = self.combo_func.get_selected_id()
        inicio = self.entry_inicio.get().strip()
        fim = self.entry_fim.get().strip()
        
        if not id_func or not inicio or not fim:
            Toast.show(self.winfo_toplevel(), "Preencha todos os campos para filtrar!", is_error=True)
            return
            
        try:
            inicio_db = datetime.datetime.strptime(inicio, "%d/%m/%Y").strftime("%Y-%m-%d")
            fim_db = datetime.datetime.strptime(fim, "%d/%m/%Y").strftime("%Y-%m-%d")
            dados = relatorios.vendas_por_periodo_e_funcionario(inicio_db, fim_db, id_func)
            for d in dados:
                data_br = datetime.datetime.strptime(str(d[1]), "%Y-%m-%d").strftime("%d/%m/%Y")
                self.table3.insert("", "end", values=(d[0], data_br, d[2], f"R$ {d[3]:.2f}"))
            Toast.show(self.winfo_toplevel(), f"Encontradas {len(dados)} vendas no período.")
        except Exception as e:
            Toast.show(self.winfo_toplevel(), f"Verifique o formato das datas (DD/MM/YYYY)", is_error=True)
