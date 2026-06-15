from dao.camiseta_dao import CamisetaDAO
from dao.cliente_dao import ClienteDAO
from dao.venda_dao import VendaDAO
from model.venda import Venda


class VendaController:
    def __init__(self):
        self.venda_dao = VendaDAO()
        self.cliente_dao = ClienteDAO()
        self.camiseta_dao = CamisetaDAO()

    def listar_clientes(self):
        try:
            return self.cliente_dao.listar_todos()
        except Exception as e:
            print(f"Erro ao listar clientes: {e}")
            return []

    def listar_camisetas(self):
        try:
            return self.camiseta_dao.listar_todos()
        except Exception as e:
            print(f"Erro ao listar camisetas: {e}")
            return []

    def listar_vendas(self):
        try:
            return self.venda_dao.listar_todos()
        except Exception as e:
            print(f"Erro ao listar vendas: {e}")
            return []

    def listar_por_cliente(self, nome_cliente: str):
        try:
            if not nome_cliente or not nome_cliente.strip():
                return self.listar_vendas()
            return self.venda_dao.listar_por_cliente(nome_cliente)
        except Exception as e:
            print(f"Erro ao filtrar vendas: {e}")
            return []

    def buscar_por_id(self, id_venda: int):
        try:
            return self.venda_dao.buscar_por_id(id_venda)
        except Exception as e:
            print(f"Erro ao buscar venda: {e}")
            return None

    def salvar_venda(self, id_cliente: int, id_camiseta: int, quantidade: str, data_venda: str):
        try:
            cliente = self.cliente_dao.buscar_por_id(id_cliente)
            if not cliente:
                return False, "Cliente não encontrado"

            camiseta = self.camiseta_dao.buscar_por_id(id_camiseta)
            if not camiseta:
                return False, "Camiseta não encontrada"

            nova_venda = Venda(
                cliente=cliente,
                camiseta=camiseta,
                quantidade=quantidade,
                data_venda=data_venda,
                validar_estoque=False
            )
            return self.venda_dao.salvar(nova_venda)

        except ValueError as e:
            return False, str(e)
        except Exception as e:
            return False, f"Erro inesperado: {e}"

    def atualizar_venda(self, id_venda: int, id_cliente: int, id_camiseta: int,
                        quantidade: str, data_venda: str):
        if not id_venda:
            return False, "Selecione uma venda para atualizar"

        try:
            venda_existente = self.venda_dao.buscar_por_id(id_venda)
            if not venda_existente:
                return False, "Venda não encontrada"

            cliente = self.cliente_dao.buscar_por_id(id_cliente)
            if not cliente:
                return False, "Cliente não encontrado"

            camiseta = self.camiseta_dao.buscar_por_id(id_camiseta)
            if not camiseta:
                return False, "Camiseta não encontrada"

            venda_atualizada = Venda(
                id=id_venda,
                cliente=cliente,
                camiseta=camiseta,
                quantidade=quantidade,
                data_venda=data_venda,
                validar_estoque=False
            )
            return self.venda_dao.atualizar(venda_atualizada)

        except ValueError as e:
            return False, str(e)
        except Exception as e:
            return False, f"Erro inesperado: {e}"

    def remover_venda(self, id_venda: int):
        if not id_venda:
            return False, "Venda não informada"

        try:
            return self.venda_dao.remover(id_venda)
        except Exception as e:
            return False, f"Erro inesperado: {e}"
