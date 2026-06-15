from dao.camiseta_dao import CamisetaDAO
from model.camisetaFactory import CamisetaFactory, TipoCamiseta


class CamisetaController:
    def __init__(self):
        self.camiseta_dao = CamisetaDAO()

    def salvar_camiseta(self, selecao: str, modelo: str, tamanho: str, preco: str, estoque: str, tipo: str):
        try:
            nova_camiseta = CamisetaFactory.criar_camiseta(
                tipo=tipo,
                selecao=selecao,
                modelo=modelo,
                tamanho=tamanho,
                preco=preco,
                estoque=estoque
            )
            return self.camiseta_dao.salvar(nova_camiseta)

        except ValueError as e:
            return False, str(e)
        except Exception as e:
            return False, f"Erro inesperado: {e}"

    def listar_camisetas(self):
        try:
            return self.camiseta_dao.listar_todos()
        except Exception as e:
            print(f"Erro ao listar camisetas: {e}")
            return []

    def listar_por_selecao(self, selecao: str):
        try:
            if not selecao or not selecao.strip():
                return self.listar_camisetas()
            return self.camiseta_dao.listar_por_selecao(selecao)
        except Exception as e:
            print(f"Erro ao filtrar camisetas: {e}")
            return []

    def buscar_por_id(self, id_camiseta: int):
        try:
            return self.camiseta_dao.buscar_por_id(id_camiseta)
        except Exception as e:
            print(f"Erro ao buscar camiseta: {e}")
            return None

    def remover_camiseta(self, id_camiseta: int):
        if not id_camiseta:
            return False, "Camiseta não informada"

        try:
            return self.camiseta_dao.remover(id_camiseta)
        except Exception as e:
            return False, f"Erro inesperado: {e}"

    def atualizar_camiseta(self, id_camiseta: int, selecao: str, modelo: str, tamanho: str, preco: str, estoque: str, tipo: str):
        if not id_camiseta:
            return False, "Selecione uma camiseta para atualizar"

        try:
            camiseta_existente = self.camiseta_dao.buscar_por_id(id_camiseta)
            if not camiseta_existente:
                return False, "Camiseta não encontrada"

            camiseta_atualizada = CamisetaFactory.criar_camiseta(
                id=id_camiseta,
                tipo=tipo,
                selecao=selecao,
                modelo=modelo,
                tamanho=tamanho,
                preco=preco,
                estoque=estoque
            )
            return self.camiseta_dao.atualizar(camiseta_atualizada)

        except ValueError as e:
            return False, str(e)
        except Exception as e:
            return False, f"Erro inesperado: {e}"

    def listar_tipos(self):
        return [tipo.value for tipo in TipoCamiseta]
