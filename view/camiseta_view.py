import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import tkinter as tk
from tkinter import messagebox, ttk
from controller.camiseta_controller import CamisetaController


class JanelaCamiseta(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Camisetas")
        self.geometry("950x540")

        self.controller = CamisetaController()
        self.camiseta_selecionada_id = None

        self.criar_widgets()
        self.carregar_dados()

    def criar_widgets(self):
        lbl_titulo = tk.Label(self, text="Camisetas Cadastradas", font=("Helvetica", 16, "bold"))
        lbl_titulo.pack(pady=10)

        frame_form = tk.Frame(self)
        frame_form.pack(fill="x", padx=20, pady=5)

        tk.Label(frame_form, text="Seleção:").grid(row=0, column=0, sticky="w", pady=3)
        self.txt_selecao = tk.Entry(frame_form, width=30)
        self.txt_selecao.grid(row=0, column=1, sticky="we", padx=5, pady=3)

        tk.Label(frame_form, text="Modelo:").grid(row=0, column=2, sticky="w", pady=3)
        self.txt_modelo = tk.Entry(frame_form, width=30)
        self.txt_modelo.grid(row=0, column=3, sticky="we", padx=5, pady=3)

        tk.Label(frame_form, text="Tamanho:").grid(row=1, column=0, sticky="w", pady=3)
        self.txt_tamanho = tk.Entry(frame_form, width=12)
        self.txt_tamanho.grid(row=1, column=1, sticky="we", padx=5, pady=3)

        tk.Label(frame_form, text="Preço:").grid(row=1, column=2, sticky="w", pady=3)
        self.txt_preco = tk.Entry(frame_form, width=15)
        self.txt_preco.grid(row=1, column=3, sticky="we", padx=5, pady=3)

        tk.Label(frame_form, text="Estoque:").grid(row=2, column=0, sticky="w", pady=3)
        self.txt_estoque = tk.Entry(frame_form, width=12)
        self.txt_estoque.grid(row=2, column=1, sticky="we", padx=5, pady=3)

        tk.Label(frame_form, text="Tipo:").grid(row=2, column=2, sticky="w", pady=3)
        self.cb_tipo = ttk.Combobox(frame_form, values=self.controller.listar_tipos(), state="readonly")
        self.cb_tipo.grid(row=2, column=3, sticky="we", padx=5, pady=3)
        self.cb_tipo.current(0)

        frame_form.columnconfigure(1, weight=1)
        frame_form.columnconfigure(3, weight=1)

        frame_botoes_form = tk.Frame(self)
        frame_botoes_form.pack(fill="x", padx=20, pady=5)

        tk.Button(frame_botoes_form, text="Salvar", width=12, command=self.salvar_camiseta).pack(side="left", padx=5)
        tk.Button(frame_botoes_form, text="Atualizar", width=12, command=self.atualizar_camiseta).pack(side="left", padx=5)
        tk.Button(frame_botoes_form, text="Limpar", width=12, command=self.limpar_campos).pack(side="left", padx=5)

        frame_busca = tk.Frame(self)
        frame_busca.pack(fill="x", padx=20, pady=5)

        tk.Label(frame_busca, text="Buscar por seleção:").pack(side="left")
        self.txt_busca = tk.Entry(frame_busca)
        self.txt_busca.pack(side="left", expand=True, fill="x", padx=5)
        tk.Button(frame_busca, text="Buscar", width=10, command=self.aplicar_busca).pack(side="left", padx=5)
        tk.Button(frame_busca, text="Todos", width=10, command=self.carregar_dados).pack(side="left", padx=5)

        frame_tree = tk.Frame(self)
        frame_tree.pack(expand=True, fill="both", padx=20, pady=10)

        scrollbar = ttk.Scrollbar(frame_tree)
        scrollbar.pack(side="right", fill="y")

        colunas = ("ID", "Selecao", "Modelo", "Tamanho", "Preco", "Estoque", "Tipo")
        self.tree = ttk.Treeview(frame_tree, columns=colunas, show="headings", yscrollcommand=scrollbar.set)

        for col in colunas:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width=115)

        self.tree.column("ID", width=60)
        self.tree.column("Selecao", width=170)
        self.tree.column("Modelo", width=170)
        self.tree.pack(expand=True, fill="both")
        self.tree.bind("<<TreeviewSelect>>", self.selecionar_camiseta)
        scrollbar.config(command=self.tree.yview)

        frame_botoes = tk.Frame(self)
        frame_botoes.pack(fill="x", padx=20, pady=5)

        tk.Button(frame_botoes, text="Remover", width=12, command=self.remover_camiseta).pack(side="left", padx=5)
        tk.Button(frame_botoes, text="Fechar", width=12, command=self.destroy).pack(side="right", padx=5)

    def carregar_dados(self):
        self.txt_busca.delete(0, tk.END)
        camisetas = self.controller.listar_camisetas()
        self.preencher_tabela(camisetas)

    def preencher_tabela(self, camisetas):
        for row in self.tree.get_children():
            self.tree.delete(row)

        for camiseta in camisetas:
            preco_formatado = f"R$ {camiseta.preco:.2f}".replace(".", ",")
            self.tree.insert("", "end", values=(
                camiseta.id,
                camiseta.selecao,
                camiseta.modelo,
                camiseta.tamanho,
                preco_formatado,
                camiseta.estoque,
                camiseta.tipo.value
            ))

    def aplicar_busca(self):
        camisetas = self.controller.listar_por_selecao(self.txt_busca.get().strip())
        self.preencher_tabela(camisetas)

    def selecionar_camiseta(self, _event=None):
        selecionado = self.tree.selection()
        if not selecionado:
            return

        item = self.tree.item(selecionado[0])
        valores = item["values"]
        self.camiseta_selecionada_id = int(valores[0])

        self.txt_selecao.delete(0, tk.END)
        self.txt_selecao.insert(0, valores[1])

        self.txt_modelo.delete(0, tk.END)
        self.txt_modelo.insert(0, valores[2])

        self.txt_tamanho.delete(0, tk.END)
        self.txt_tamanho.insert(0, valores[3])

        self.txt_preco.delete(0, tk.END)
        self.txt_preco.insert(0, str(valores[4]).replace("R$ ", ""))

        self.txt_estoque.delete(0, tk.END)
        self.txt_estoque.insert(0, valores[5])

        self.cb_tipo.set(valores[6])

    def obter_dados_formulario(self):
        return (
            self.txt_selecao.get().strip(),
            self.txt_modelo.get().strip(),
            self.txt_tamanho.get().strip(),
            self.txt_preco.get().strip(),
            self.txt_estoque.get().strip(),
            self.cb_tipo.get().strip()
        )

    def salvar_camiseta(self):
        selecao, modelo, tamanho, preco, estoque, tipo = self.obter_dados_formulario()
        sucesso, msg = self.controller.salvar_camiseta(selecao, modelo, tamanho, preco, estoque, tipo)

        if sucesso:
            messagebox.showinfo("Sucesso", msg, parent=self)
            self.limpar_campos()
            self.carregar_dados()
        else:
            messagebox.showerror("Erro", msg, parent=self)

    def atualizar_camiseta(self):
        selecao, modelo, tamanho, preco, estoque, tipo = self.obter_dados_formulario()
        sucesso, msg = self.controller.atualizar_camiseta(
            self.camiseta_selecionada_id,
            selecao,
            modelo,
            tamanho,
            preco,
            estoque,
            tipo
        )

        if sucesso:
            messagebox.showinfo("Sucesso", msg, parent=self)
            self.limpar_campos()
            self.carregar_dados()
        else:
            messagebox.showerror("Erro", msg, parent=self)

    def remover_camiseta(self):
        if not self.camiseta_selecionada_id:
            messagebox.showwarning("Aviso", "Selecione uma camiseta para remover.", parent=self)
            return

        resposta = messagebox.askyesno(
            "Confirmar Exclusão",
            "Tem certeza que deseja remover a camiseta selecionada?",
            parent=self
        )
        if not resposta:
            return

        sucesso, msg = self.controller.remover_camiseta(self.camiseta_selecionada_id)
        if sucesso:
            messagebox.showinfo("Sucesso", msg, parent=self)
            self.limpar_campos()
            self.carregar_dados()
        else:
            messagebox.showerror("Erro", msg, parent=self)

    def limpar_campos(self):
        self.camiseta_selecionada_id = None
        self.tree.selection_remove(self.tree.selection())
        self.txt_selecao.delete(0, tk.END)
        self.txt_modelo.delete(0, tk.END)
        self.txt_tamanho.delete(0, tk.END)
        self.txt_preco.delete(0, tk.END)
        self.txt_estoque.delete(0, tk.END)
        self.cb_tipo.current(0)
