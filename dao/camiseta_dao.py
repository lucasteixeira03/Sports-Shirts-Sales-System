import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from dao.db_config import DatabaseConfig
from dao.generic_dao import GenericDAO
from model.camisetaFactory import Camiseta, CamisetaFactory


class CamisetaDAO(GenericDAO):
    def __init__(self):
        self.conexao = DatabaseConfig.get_connection()

    def _linha_para_camiseta(self, linha):
        return CamisetaFactory.criar_camiseta(
            id=linha[0],
            selecao=linha[1],
            modelo=linha[2],
            tamanho=linha[3],
            preco=float(linha[4]),
            estoque=linha[5],
            tipo=linha[6]
        )

    def salvar(self, objeto: Camiseta):
        if not self.conexao:
            return False, "Sem conexão com o BD"

        try:
            cursor = self.conexao.cursor()
            query = """INSERT INTO tb_camiseta (SELECAO, MODELO, TAMANHO, PRECO, ESTOQUE, TIPO)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    RETURNING ID_CAMISETA"""
            cursor.execute(query, (objeto.selecao,
                                   objeto.modelo,
                                   objeto.tamanho,
                                   objeto.preco,
                                   objeto.estoque,
                                   objeto.tipo.value))
            objeto.id = cursor.fetchone()[0]
            self.conexao.commit()
            return True, "Camiseta cadastrada com sucesso"

        except Exception as e:
            self.conexao.rollback()
            return False, f"Erro ao inserir camiseta: {e}"

        finally:
            if cursor:
                cursor.close()

    def listar_todos(self):
        if not self.conexao:
            return []

        try:
            cursor = self.conexao.cursor()
            query = """SELECT ID_CAMISETA, SELECAO, MODELO, TAMANHO, PRECO, ESTOQUE, TIPO
                    FROM tb_camiseta
                    ORDER BY ID_CAMISETA"""
            cursor.execute(query)
            return [self._linha_para_camiseta(linha) for linha in cursor.fetchall()]

        except Exception as e:
            print(f"Erro ao buscar camisetas: {e}")
            return []

        finally:
            if cursor:
                cursor.close()

    def remover(self, id_objeto: int):
        if not self.conexao:
            return False, "Sem conexão com o BD"

        try:
            cursor = self.conexao.cursor()
            query = "DELETE FROM tb_camiseta WHERE ID_CAMISETA = %s"
            cursor.execute(query, (id_objeto,))
            self.conexao.commit()
            return True, "Camiseta removida com sucesso"

        except Exception as e:
            self.conexao.rollback()
            return False, f"Erro ao remover camiseta: {e}"

        finally:
            if cursor:
                cursor.close()

    def atualizar(self, objeto: Camiseta):
        if not self.conexao:
            return False, "Sem conexão com o BD"

        try:
            cursor = self.conexao.cursor()
            query = """UPDATE tb_camiseta
                    SET SELECAO = %s, MODELO = %s, TAMANHO = %s,
                        PRECO = %s, ESTOQUE = %s, TIPO = %s
                    WHERE ID_CAMISETA = %s"""
            cursor.execute(query, (objeto.selecao,
                                   objeto.modelo,
                                   objeto.tamanho,
                                   objeto.preco,
                                   objeto.estoque,
                                   objeto.tipo.value,
                                   objeto.id))
            self.conexao.commit()
            return True, "Camiseta atualizada com sucesso"

        except Exception as e:
            self.conexao.rollback()
            return False, f"Erro ao atualizar camiseta: {e}"

        finally:
            if cursor:
                cursor.close()

    def buscar_por_id(self, id_camiseta: int):
        if not self.conexao:
            return None

        try:
            cursor = self.conexao.cursor()
            query = """SELECT ID_CAMISETA, SELECAO, MODELO, TAMANHO, PRECO, ESTOQUE, TIPO
                    FROM tb_camiseta
                    WHERE ID_CAMISETA = %s"""
            cursor.execute(query, (id_camiseta,))
            linha = cursor.fetchone()
            return self._linha_para_camiseta(linha) if linha else None

        except Exception as e:
            print(f"Erro ao buscar camiseta: {e}")
            return None

        finally:
            if cursor:
                cursor.close()

    def listar_por_selecao(self, selecao: str):
        if not self.conexao:
            return []

        try:
            cursor = self.conexao.cursor()
            query = """SELECT ID_CAMISETA, SELECAO, MODELO, TAMANHO, PRECO, ESTOQUE, TIPO
                    FROM tb_camiseta
                    WHERE SELECAO ILIKE %s
                    ORDER BY SELECAO, MODELO"""
            cursor.execute(query, (f"%{selecao.strip()}%",))
            return [self._linha_para_camiseta(linha) for linha in cursor.fetchall()]

        except Exception as e:
            print(f"Erro ao filtrar camisetas por selecao: {e}")
            return []

        finally:
            if cursor:
                cursor.close()
