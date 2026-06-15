import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from datetime import date
import tkinter as tk
from tkinter import messagebox, ttk

from controller.venda_controller import VendaController


class JanelaVenda(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Vendas")
        self.geometry("1000x560")

        self.controller = VendaController()
        self.venda_selecionada_id = None
        self.clientes = []
        self.camisetas = []

        self.criar_widgets()
        self.carregar_opcoes()
        self.carregar_dados()

    def criar_widgets(self):
        lbl_titulo = tk.Label(self, text="Vendas Cadastradas", font=("Helvetica", 16, "bold"))
        lbl_titulo.pack(pady=10)

        frame_form = tk.Frame(self)
        frame_form.pack(fill="x", padx=20, pady=5)

        tk.Label(frame_form, text="Cliente:").grid(row=0, column=0, sticky="w", pady=3)
        self.cb_cliente = ttk.Combobox(frame_form, state="readonly")
        self.cb_cliente.grid(row=0, column=1, sticky="we", padx=5, pady=3)

        tk.Label(frame_form, text="Camiseta:").grid(row=0, column=2, sticky="w", pady=3)
        self.cb_camiseta = ttk.Combobox(frame_form, state="readonly")
        self.cb_camiseta.grid(row=0, column=3, sticky="we", padx=5, pady=3)

        tk.Label(frame_form, text="Quantidade:").grid(row=1, column=0, sticky="w", pady=3)
        self.txt_quantidade = tk.Entry(frame_form, width=12)
        self.txt_quantidade.grid(row=1, column=1, sticky="we", padx=5, pady=3)

        tk.Label(frame_form, text="Data (AAAA-MM-DD):").grid(row=1, column=2, sticky="w", pady=3)
        self.txt_data = tk.Entry(frame_form, width=15)
        self.txt_data.grid(row=1, column=3, sticky="we", padx=5, pady=3)
        self.txt_data.insert(0, date.today().isoformat())

        frame_form.columnconfigure(1, weight=1)
        frame_form.columnconfigure(3, weight=1)

        frame_botoes_form = tk.Frame(self)
        frame_botoes_form.pack(fill="x", padx=20, pady=5)

        tk.Button(frame_botoes_form, text="Salvar", width=12, command=self.salvar_venda).pack(side="left", padx=5)
        tk.Button(frame_botoes_form, text="Atualizar", width=12, command=self.atualizar_venda).pack(side="left", padx=5)
        tk.Button(frame_botoes_form, text="Limpar", width=12, command=self.limpar_campos).pack(side="left", padx=5)
        tk.Button(frame_botoes_form, text="Recarregar", width=12, command=self.recarregar_tela).pack(side="left", padx=5)

        frame_busca = tk.Frame(self)
        frame_busca.pack(fill="x", padx=20, pady=5)

        tk.Label(frame_busca, text="Buscar por cliente:").pack(side="left")
        self.txt_busca = tk.Entry(frame_busca)
        self.txt_busca.pack(side="left", expand=True, fill="x", padx=5)
        tk.Button(frame_busca, text="Buscar", width=10, command=self.aplicar_busca).pack(side="left", padx=5)
        tk.Button(frame_busca, text="Todos", width=10, command=self.carregar_dados).pack(side="left", padx=5)

        frame_tree = tk.Frame(self)
        frame_tree.pack(expand=True, fill="both", padx=20, pady=10)

        scrollbar = ttk.Scrollbar(frame_tree)
        scrollbar.pack(side="right", fill="y")

        colunas = ("ID", "Cliente", "Camiseta", "Quantidade", "Valor Total", "Data")
        self.tree = ttk.Treeview(frame_tree, columns=colunas, show="headings", yscrollcommand=scrollbar.set)

        for col in colunas:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width=130)

        self.tree.column("ID", width=60)
        self.tree.column("Cliente", width=220)
        self.tree.column("Camiseta", width=260)
        self.tree.pack(expand=True, fill="both")
        self.tree.bind("<<TreeviewSelect>>", self.selecionar_venda)
        scrollbar.config(command=self.tree.yview)

        frame_botoes = tk.Frame(self)
        frame_botoes.pack(fill="x", padx=20, pady=5)

        tk.Button(frame_botoes, text="Remover", width=12, command=self.remover_venda).pack(side="left", padx=5)
        tk.Button(frame_botoes, text="Fechar", width=12, command=self.destroy).pack(side="right", padx=5)

    def carregar_opcoes(self):
        self.clientes = self.controller.listar_clientes()
        self.camisetas = self.controller.listar_camisetas()

        self.cb_cliente["values"] = [
            f"{cliente.id} - {cliente.nome} ({cliente.cpf})"
            for cliente in self.clientes
        ]
        self.cb_camiseta["values"] = [
            f"{camiseta.id} - {camiseta.selecao} {camiseta.modelo} {camiseta.tamanho} "
            f"(Estoque: {camiseta.estoque})"
            for camiseta in self.camisetas
        ]

        if self.clientes:
            self.cb_cliente.current(0)
        if self.camisetas:
            self.cb_camiseta.current(0)

    def carregar_dados(self):
        self.txt_busca.delete(0, tk.END)
        vendas = self.controller.listar_vendas()
        self.preencher_tabela(vendas)

    def preencher_tabela(self, vendas):
        for row in self.tree.get_children():
            self.tree.delete(row)

        for venda in vendas:
            camiseta_texto = f"{venda.camiseta.selecao} - {venda.camiseta.modelo}"
            valor_formatado = f"R$ {venda.valor_total:.2f}".replace(".", ",")
            self.tree.insert("", "end", values=(
                venda.id,
                venda.cliente.nome,
                camiseta_texto,
                venda.quantidade,
                valor_formatado,
                venda.data_venda.strftime("%d/%m/%Y")
            ))

    def aplicar_busca(self):
        vendas = self.controller.listar_por_cliente(self.txt_busca.get().strip())
        self.preencher_tabela(vendas)

    def selecionar_venda(self, _event=None):
        selecionado = self.tree.selection()
        if not selecionado:
            return

        item = self.tree.item(selecionado[0])
        id_venda = int(item["values"][0])
        venda = self.controller.buscar_por_id(id_venda)
        if not venda:
            messagebox.showerror("Erro", "Venda nao encontrada.", parent=self)
            return

        self.venda_selecionada_id = id_venda
        self.selecionar_combo_por_id(self.cb_cliente, venda.cliente.id)
        self.selecionar_combo_por_id(self.cb_camiseta, venda.camiseta.id)

        self.txt_quantidade.delete(0, tk.END)
        self.txt_quantidade.insert(0, venda.quantidade)

        self.txt_data.delete(0, tk.END)
        self.txt_data.insert(0, venda.data_venda.isoformat())

    def selecionar_combo_por_id(self, combo, id_objeto: int):
        for indice, valor in enumerate(combo["values"]):
            if str(valor).startswith(f"{id_objeto} - "):
                combo.current(indice)
                return

    def obter_id_combo(self, combo, nome_campo: str):
        valor = combo.get().strip()
        if not valor:
            raise ValueError(f"Selecione um {nome_campo}.")
        return int(valor.split(" - ")[0])

    def obter_dados_formulario(self):
        return (
            self.obter_id_combo(self.cb_cliente, "cliente"),
            self.obter_id_combo(self.cb_camiseta, "camiseta"),
            self.txt_quantidade.get().strip(),
            self.txt_data.get().strip()
        )

    def salvar_venda(self):
        try:
            id_cliente, id_camiseta, quantidade, data_venda = self.obter_dados_formulario()
            sucesso, msg = self.controller.salvar_venda(id_cliente, id_camiseta, quantidade, data_venda)
        except ValueError as e:
            sucesso, msg = False, str(e)

        if sucesso:
            messagebox.showinfo("Sucesso", msg, parent=self)
            self.recarregar_tela()
        else:
            messagebox.showerror("Erro", msg, parent=self)

    def atualizar_venda(self):
        try:
            id_cliente, id_camiseta, quantidade, data_venda = self.obter_dados_formulario()
            sucesso, msg = self.controller.atualizar_venda(self.venda_selecionada_id, id_cliente, id_camiseta, quantidade, data_venda)
        except ValueError as e:
            sucesso, msg = False, str(e)

        if sucesso:
            messagebox.showinfo("Sucesso", msg, parent=self)
            self.recarregar_tela()
        else:
            messagebox.showerror("Erro", msg, parent=self)

    def remover_venda(self):
        if not self.venda_selecionada_id:
            messagebox.showwarning("Aviso", "Selecione uma venda para remover.", parent=self)
            return

        resposta = messagebox.askyesno(
            "Confirmar Exclusao",
            "Tem certeza que deseja remover a venda selecionada?",
            parent=self
        )
        if not resposta:
            return

        sucesso, msg = self.controller.remover_venda(self.venda_selecionada_id)
        if sucesso:
            messagebox.showinfo("Sucesso", msg, parent=self)
            self.recarregar_tela()
        else:
            messagebox.showerror("Erro", msg, parent=self)

    def recarregar_tela(self):
        self.carregar_opcoes()
        self.limpar_campos()
        self.carregar_dados()

    def limpar_campos(self):
        self.venda_selecionada_id = None
        self.tree.selection_remove(self.tree.selection())
        self.txt_quantidade.delete(0, tk.END)
        self.txt_data.delete(0, tk.END)
        self.txt_data.insert(0, date.today().isoformat())

        if self.clientes:
            self.cb_cliente.current(0)
        if self.camisetas:
            self.cb_camiseta.current(0)
