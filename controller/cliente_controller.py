from dao.cliente_dao import ClienteDAO
from model.cliente import *

class ClienteController:
    def __init__(self):
        self.cliente_dao = ClienteDAO()

    def salvar_cliente(self, nome: str, cpf: str, telefone: str, email: str):
        try:
            cpf_formatado = formataCpf(cpf)
            cliente_existente = self.cliente_dao.buscar_por_cpf(cpf_formatado)
            if cliente_existente:
                return False, f"Cliente com CPF {cpf_formatado} ja está cadastrado"

            novo_cliente = Cliente(
                nome=nome,
                cpf=cpf_formatado,
                telefone=telefone,
                email=email
            )
            return self.cliente_dao.salvar(novo_cliente)

        except ValueError as e:
            return False, str(e)
        except Exception as e:
            return False, f"Erro inesperado: {e}"

    def listar_clientes(self):
        try:
            return self.cliente_dao.listar_todos()
        except Exception as e:
            print(f"Erro ao listar clientes: {e}")
            return []

    def buscar_por_id(self, id_cliente: int):
        try:
            return self.cliente_dao.buscar_por_id(id_cliente)
        except Exception as e:
            print(f"Erro ao buscar cliente: {e}")
            return None

    def remover_cliente(self, id_cliente: int):
        if not id_cliente:
            return False, "Cliente não informado"

        try:
            return self.cliente_dao.remover(id_cliente)
        except Exception as e:
            return False, f"Erro inesperado: {e}"

    def atualizar_cliente(self, id_cliente: int, nome: str, cpf: str, telefone: str, email: str):
        if not id_cliente:
            return False, "Selecione um cliente para atualizar"

        try:
            cliente_existente = self.cliente_dao.buscar_por_id(id_cliente)
            if not cliente_existente:
                return False, "Cliente não encontrado"

            cpf_formatado = formataCpf(cpf)
            cliente_com_cpf = self.cliente_dao.buscar_por_cpf(cpf_formatado)
            if cliente_com_cpf and cliente_com_cpf.id != id_cliente:
                return False, f"CPF {cpf_formatado} ja pertence a outro cliente"

            cliente_atualizado = Cliente(
                id=id_cliente,
                nome=nome,
                cpf=cpf_formatado,
                telefone=telefone,
                email=email
            )
            return self.cliente_dao.atualizar(cliente_atualizado)

        except ValueError as e:
            return False, str(e)
        except Exception as e:
            return False, f"Erro inesperado: {e}"
