import tkinter as tk


class JanelaSobre(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Sobre")
        self.geometry("520x300")
        self.resizable(False, False)

        self.criar_widgets()

    def criar_widgets(self):
        lbl_titulo = tk.Label(self, text="Sistema de Vendas de Camisetas Esportivas", font=("Helvetica", 14, "bold"), wraplength=460, justify="center")
        lbl_titulo.pack(pady=18)

        texto = (
            "Projeto Final da disciplina de Linguagem de Programação "
            "Orientada a Objetos - LPOO.\n\n"
            "Sistema desktop em Python com Tkinter e PostgreSQL para "
            "cadastro de clientes, cadastro de camisetas esportivas e "
            "registro de vendas com controle de estoque.\n\n"
            "Autor: Lucas de Sousa Teixeira\n"
            "Curso: Bacharelado em Ciência da Computação\n"
            "Período: 2026/1"
        )

        lbl_texto = tk.Label(self, text=texto, font=("Helvetica", 10), wraplength=460, justify="center")
        lbl_texto.pack(padx=25, pady=5)

        tk.Button(self, text="Fechar", width=12, command=self.destroy).pack(pady=15)
