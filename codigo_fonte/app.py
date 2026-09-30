import customtkinter as ctk
import database

# Importa todos os frames
from gui.frames.autores_frame import AutoresFrame
from gui.frames.editoras_frame import EditorasFrame
from gui.frames.livros_frame import LivrosFrame
from gui.frames.funcionarios_frame import FuncionariosFrame
from gui.frames.clientes_frame import ClientesFrame
from gui.frames.vendas_frame import VendasFrame
from gui.frames.relatorios_frame import RelatoriosFrame

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Sistema Livraria")
        self.geometry("1100x650")
        
        # Configuração inicial do tema
        ctk.set_appearance_mode("dark")
        
        # --- Sidebar ---
        self.sidebar = ctk.CTkFrame(self, width=220, corner_radius=0, fg_color="#1a1a2e")
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False) # Mantém a largura fixa
        
        # Logo/Título
        ctk.CTkLabel(self.sidebar, text="Livraria", 
                     font=ctk.CTkFont(size=28, weight="bold"), text_color="#f1f5f9").pack(pady=(30, 40))
        
        # Botões de Navegação
        self.nav_buttons = {}
        buttons_config = [
            ("Livros",       LivrosFrame),
            ("Vendas",       VendasFrame),
            ("Autores",      AutoresFrame),
            ("Editoras",     EditorasFrame),
            ("Clientes",     ClientesFrame),
            ("Funcionários", FuncionariosFrame),
            ("Relatórios",   RelatoriosFrame),
        ]
        
        for text, frame_class in buttons_config:
            btn = ctk.CTkButton(self.sidebar, text=text, anchor="w",
                                fg_color="transparent", text_color="#94a3b8",
                                hover_color="#16213e", font=ctk.CTkFont(size=14),
                                command=lambda fc=frame_class: self.show_frame(fc))
            btn.pack(pady=5, padx=20, fill="x")
            self.nav_buttons[frame_class] = btn
            
        # --- Área de Conteúdo ---
        self.configure(fg_color="#0f0f23")
        self.content = ctk.CTkFrame(self, corner_radius=10, fg_color="transparent")
        self.content.pack(side="right", fill="both", expand=True, padx=20, pady=20)
        
        # Estado inicial
        self.current_frame = None
        self.show_frame(LivrosFrame) # Inicia na tela de livros

    def show_frame(self, frame_class):
        # Destrói o frame atual se existir
        if self.current_frame:
            self.current_frame.destroy()
            
        # Cria e exibe o novo frame
        self.current_frame = frame_class(self.content)
        self.current_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Atualiza o destaque do botão selecionado
        for fc, btn in self.nav_buttons.items():
            if fc == frame_class:
                btn.configure(fg_color="#16213e", text_color="#f1f5f9")
            else:
                btn.configure(fg_color="transparent", text_color="#94a3b8")

if __name__ == "__main__":
    # Garante que o banco está inicializado
    database.init_db()
    
    # Inicia a aplicação
    app = App()
    app.mainloop()
