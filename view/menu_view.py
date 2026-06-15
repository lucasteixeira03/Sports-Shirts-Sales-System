import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import tkinter as tk

class JanelaPrincipal(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Vendas de Camisetas Esportivas - LPOO")
        self.geometry("560x320")

        self.criar_menu()
        self.criar_conteudo()

    def criar_menu(self):
        barra_menu = tk.Menu(self)
        self.config(menu=barra_menu)

        menu_cadastro = tk.Menu(barra_menu, tearoff=0)
        barra_menu.add_cascade(label="Cadastro", menu=menu_cadastro)
        menu_cadastro.add_command(label="Clientes", command=self.abrir_clientes)
        menu_cadastro.add_command(label="Camisetas", command=self.abrir_camisetas)

        menu_venda = tk.Menu(barra_menu, tearoff=0)
        barra_menu.add_cascade(label="Venda", menu=menu_venda)
        menu_venda.add_command(label="Vendas", command=self.abrir_vendas)

        menu_ajuda = tk.Menu(barra_menu, tearoff=0)
        barra_menu.add_cascade(label="Ajuda", menu=menu_ajuda)
        menu_ajuda.add_command(label="Sobre", command=self.abrir_sobre)
        menu_ajuda.add_separator()
        menu_ajuda.add_command(label="Sair", command=self.destroy)

    def criar_conteudo(self):
        lbl_titulo = tk.Label(
            self,
            text="Sistema de Vendas de Camisetas Esportivas",
            font=("Helvetica", 16, "bold")
        )
        lbl_titulo.pack(pady=25)

        lbl_info = tk.Label(self, text="Use a barra de menus para acessar os cadastros e registrar vendas.", font=("Helvetica", 11), justify="center")
        lbl_info.pack(pady=5)

        frame_botoes = tk.Frame(self)
        frame_botoes.pack(pady=25)

        tk.Button(frame_botoes, text="Clientes", width=14, command=self.abrir_clientes).grid(row=0, column=0, padx=8)
        tk.Button(frame_botoes, text="Camisetas", width=14, command=self.abrir_camisetas).grid(row=0, column=1, padx=8)
        tk.Button(frame_botoes, text="Vendas", width=14, command=self.abrir_vendas).grid(row=0, column=2, padx=8)

    def abrir_clientes(self):
        from view.cliente_view import JanelaCliente
        JanelaCliente(master=self)

    def abrir_camisetas(self):
        from view.camiseta_view import JanelaCamiseta
        JanelaCamiseta(master=self)

    def abrir_vendas(self):
        from view.venda_view import JanelaVenda
        JanelaVenda(master=self)

    def abrir_sobre(self):
        from view.sobre_view import JanelaSobre
        JanelaSobre(master=self)
