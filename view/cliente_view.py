import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import tkinter as tk
from tkinter import messagebox, ttk
from controller.cliente_controller import ClienteController


class JanelaCliente(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Clientes")
        self.geometry("900x520")

        self.controller = ClienteController()
        self.cliente_selecionado_id = None
        self.clientes = []

        self.criar_widgets()
        self.carregar_dados()

    def criar_widgets(self):
        lbl_titulo = tk.Label(self, text="Clientes Cadastrados", font=("Helvetica", 16, "bold"))
        lbl_titulo.pack(pady=10)

        frame_form = tk.Frame(self)
        frame_form.pack(fill="x", padx=20, pady=5)

        tk.Label(frame_form, text="Nome:").grid(row=0, column=0, sticky="w", pady=3)
        self.txt_nome = tk.Entry(frame_form, width=35)
        self.txt_nome.grid(row=0, column=1, sticky="we", padx=5, pady=3)

        tk.Label(frame_form, text="CPF:").grid(row=0, column=2, sticky="w", pady=3)
        self.txt_cpf = tk.Entry(frame_form, width=20)
        self.txt_cpf.grid(row=0, column=3, sticky="we", padx=5, pady=3)
        self.txt_cpf.bind("<KeyRelease>", self.formatar_cpf_evento)

        tk.Label(frame_form, text="Telefone:").grid(row=1, column=0, sticky="w", pady=3)
        self.txt_telefone = tk.Entry(frame_form, width=25)
        self.txt_telefone.grid(row=1, column=1, sticky="we", padx=5, pady=3)

        tk.Label(frame_form, text="Email:").grid(row=1, column=2, sticky="w", pady=3)
        self.txt_email = tk.Entry(frame_form, width=35)
        self.txt_email.grid(row=1, column=3, sticky="we", padx=5, pady=3)

        frame_form.columnconfigure(1, weight=1)
        frame_form.columnconfigure(3, weight=1)

        frame_botoes_form = tk.Frame(self)
        frame_botoes_form.pack(fill="x", padx=20, pady=5)

        tk.Button(frame_botoes_form, text="Salvar", width=12, command=self.salvar_cliente).pack(side="left", padx=5)
        tk.Button(frame_botoes_form, text="Atualizar", width=12, command=self.atualizar_cliente).pack(side="left", padx=5)
        tk.Button(frame_botoes_form, text="Limpar", width=12, command=self.limpar_campos).pack(side="left", padx=5)

        frame_busca = tk.Frame(self)
        frame_busca.pack(fill="x", padx=20, pady=5)

        tk.Label(frame_busca, text="Buscar por nome ou CPF:").pack(side="left")
        self.txt_busca = tk.Entry(frame_busca)
        self.txt_busca.pack(side="left", expand=True, fill="x", padx=5)
        tk.Button(frame_busca, text="Buscar", width=10, command=self.aplicar_busca).pack(side="left", padx=5)
        tk.Button(frame_busca, text="Todos", width=10, command=self.carregar_dados).pack(side="left", padx=5)

        frame_tree = tk.Frame(self)
        frame_tree.pack(expand=True, fill="both", padx=20, pady=10)

        scrollbar = ttk.Scrollbar(frame_tree)
        scrollbar.pack(side="right", fill="y")

        colunas = ("ID", "Nome", "CPF", "Telefone", "Email")
        self.tree = ttk.Treeview(frame_tree, columns=colunas, show="headings", yscrollcommand=scrollbar.set)

        for col in colunas:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width=120)

        self.tree.column("ID", width=60)
        self.tree.column("Nome", width=220)
        self.tree.column("Email", width=220)
        self.tree.pack(expand=True, fill="both")
        self.tree.bind("<<TreeviewSelect>>", self.selecionar_cliente)
        scrollbar.config(command=self.tree.yview)

        frame_botoes = tk.Frame(self)
        frame_botoes.pack(fill="x", padx=20, pady=5)

        tk.Button(frame_botoes, text="Remover", width=12, command=self.remover_cliente).pack(side="left", padx=5)
        tk.Button(frame_botoes, text="Fechar", width=12, command=self.destroy).pack(side="right", padx=5)

    def carregar_dados(self):
        self.txt_busca.delete(0, tk.END)
        self.clientes = self.controller.listar_clientes()
        self.preencher_tabela(self.clientes)

    def preencher_tabela(self, clientes):
        for row in self.tree.get_children():
            self.tree.delete(row)

        for cliente in clientes:
            self.tree.insert("", "end", values=(
                cliente.id,
                cliente.nome,
                cliente.cpf,
                cliente.telefone,
                cliente.email
            ))

    def aplicar_busca(self):
        termo = self.txt_busca.get().strip().lower()
        if not termo:
            self.preencher_tabela(self.clientes)
            return

        clientes_filtrados = [
            cliente for cliente in self.clientes
            if termo in cliente.nome.lower() or termo in cliente.cpf.lower()
        ]
        self.preencher_tabela(clientes_filtrados)

    def selecionar_cliente(self, _event=None):
        selecionado = self.tree.selection()
        if not selecionado:
            return

        item = self.tree.item(selecionado[0])
        valores = item["values"]
        self.cliente_selecionado_id = int(valores[0])

        self.txt_nome.delete(0, tk.END)
        self.txt_nome.insert(0, valores[1])

        self.txt_cpf.delete(0, tk.END)
        self.txt_cpf.insert(0, valores[2])

        self.txt_telefone.delete(0, tk.END)
        self.txt_telefone.insert(0, valores[3])

        self.txt_email.delete(0, tk.END)
        self.txt_email.insert(0, valores[4])

    def obter_dados_formulario(self):
        return (
            self.txt_nome.get().strip(),
            self.txt_cpf.get().strip(),
            self.txt_telefone.get().strip(),
            self.txt_email.get().strip()
        )

    def formatar_cpf_evento(self, _event=None):
        numeros = "".join(caractere for caractere in self.txt_cpf.get() if caractere.isdigit())
        numeros = numeros[:11]

        if len(numeros) <= 3:
            cpf_formatado = numeros
        elif len(numeros) <= 6:
            cpf_formatado = f"{numeros[0:3]}.{numeros[3:6]}"
        elif len(numeros) <= 9:
            cpf_formatado = f"{numeros[0:3]}.{numeros[3:6]}.{numeros[6:9]}"
        else:
            cpf_formatado = f"{numeros[0:3]}.{numeros[3:6]}.{numeros[6:9]}-{numeros[9:11]}"

        self.txt_cpf.delete(0, tk.END)
        self.txt_cpf.insert(0, cpf_formatado)

    def salvar_cliente(self):
        nome, cpf, telefone, email = self.obter_dados_formulario()
        sucesso, msg = self.controller.salvar_cliente(nome, cpf, telefone, email)

        if sucesso:
            messagebox.showinfo("Sucesso", msg, parent=self)
            self.limpar_campos()
            self.carregar_dados()
        else:
            messagebox.showerror("Erro", msg, parent=self)

    def atualizar_cliente(self):
        nome, cpf, telefone, email = self.obter_dados_formulario()
        sucesso, msg = self.controller.atualizar_cliente(
            self.cliente_selecionado_id,
            nome,
            cpf,
            telefone,
            email
        )

        if sucesso:
            messagebox.showinfo("Sucesso", msg, parent=self)
            self.limpar_campos()
            self.carregar_dados()
        else:
            messagebox.showerror("Erro", msg, parent=self)

    def remover_cliente(self):
        if not self.cliente_selecionado_id:
            messagebox.showwarning("Aviso", "Selecione um cliente para remover.", parent=self)
            return

        resposta = messagebox.askyesno(
            "Confirmar Exclusão",
            "Tem certeza que deseja remover o cliente selecionado?",
            parent=self
        )
        if not resposta:
            return

        sucesso, msg = self.controller.remover_cliente(self.cliente_selecionado_id)
        if sucesso:
            messagebox.showinfo("Sucesso", msg, parent=self)
            self.limpar_campos()
            self.carregar_dados()
        else:
            messagebox.showerror("Erro", msg, parent=self)

    def limpar_campos(self):
        self.cliente_selecionado_id = None
        self.tree.selection_remove(self.tree.selection())
        self.txt_nome.delete(0, tk.END)
        self.txt_cpf.delete(0, tk.END)
        self.txt_telefone.delete(0, tk.END)
        self.txt_email.delete(0, tk.END)
