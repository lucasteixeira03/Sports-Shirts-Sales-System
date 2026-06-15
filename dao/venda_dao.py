import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from dao.db_config import DatabaseConfig
from dao.generic_dao import GenericDAO
from model.camisetaFactory import CamisetaFactory
from model.cliente import Cliente
from model.venda import Venda

class VendaDAO(GenericDAO):
    def __init__(self):
        self.conexao = DatabaseConfig.get_connection()

    def _linha_para_venda(self, linha):
        cliente = Cliente(
            id=linha[1],
            nome=linha[2],
            cpf=linha[3],
            telefone=linha[4] if linha[4] else "",
            email=linha[5] if linha[5] else ""
        )
        camiseta = CamisetaFactory.criar_camiseta(
            id=linha[6],
            selecao=linha[7],
            modelo=linha[8],
            tamanho=linha[9],
            preco=float(linha[10]),
            estoque=linha[11],
            tipo=linha[12]
        )
        return Venda(
            id=linha[0],
            cliente=cliente,
            camiseta=camiseta,
            quantidade=linha[13],
            valor_total=float(linha[14]),
            data_venda=linha[15],
            validar_estoque=False
        )

    def _query_listagem(self):
        return """SELECT v.ID_VENDA,
                    c.ID_CLIENTE, c.NOME, c.CPF, c.TELEFONE, c.EMAIL,
                    ca.ID_CAMISETA, ca.SELECAO, ca.MODELO, ca.TAMANHO,
                    ca.PRECO, ca.ESTOQUE, ca.TIPO,
                    v.QUANTIDADE, v.VLTOTAL, v.DAVENDA
                FROM tb_venda v
                INNER JOIN tb_cliente c ON v.CLIENTE_ID = c.ID_CLIENTE
                INNER JOIN tb_camiseta ca ON v.CAMISETA_ID = ca.ID_CAMISETA"""

    def salvar(self, objeto: Venda):
        if not self.conexao:
            return False, "Sem conexao com o BD"

        try:
            cursor = self.conexao.cursor()
            query = "SELECT ESTOQUE, PRECO FROM tb_camiseta WHERE ID_CAMISETA = %s FOR UPDATE"
            cursor.execute(query, (objeto.camiseta.id,))
            linha_camiseta = cursor.fetchone()
            if not linha_camiseta:
                self.conexao.rollback()
                return False, "Camiseta nao encontrada"

            estoque_atual = int(linha_camiseta[0])
            preco_atual = float(linha_camiseta[1])
            if objeto.quantidade > estoque_atual:
                self.conexao.rollback()
                return False, "Quantidade maior que o estoque disponivel"

            objeto.valor_total = objeto.quantidade * preco_atual

            query = """INSERT INTO tb_venda
                    (CLIENTE_ID, CAMISETA_ID, QUANTIDADE, VLTOTAL, DAVENDA)
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING ID_VENDA"""
            cursor.execute(query, (objeto.cliente.id,
                                   objeto.camiseta.id,
                                   objeto.quantidade,
                                   objeto.valor_total,
                                   objeto.data_venda))
            objeto.id = cursor.fetchone()[0]

            cursor.execute("UPDATE tb_camiseta SET ESTOQUE = ESTOQUE - %s WHERE ID_CAMISETA = %s",(objeto.quantidade, objeto.camiseta.id))
            self.conexao.commit()
            return True, "Venda cadastrada com sucesso"

        except Exception as e:
            self.conexao.rollback()
            return False, f"Erro ao inserir venda: {e}"

        finally:
            if cursor:
                cursor.close()

    def listar_todos(self):
        if not self.conexao:
            return []

        try:
            cursor = self.conexao.cursor()
            query = self._query_listagem() + " ORDER BY v.ID_VENDA"
            cursor.execute(query)
            return [self._linha_para_venda(linha) for linha in cursor.fetchall()]

        except Exception as e:
            print(f"Erro ao buscar vendas: {e}")
            return []

        finally:
            if cursor:
                cursor.close()

    def remover(self, id_objeto: int):
        if not self.conexao:
            return False, "Sem conexao com o BD"

        try:
            cursor = self.conexao.cursor()
            query = "SELECT CAMISETA_ID, QUANTIDADE FROM tb_venda WHERE ID_VENDA = %s"
            cursor.execute(query, (id_objeto,))
            linha_venda = cursor.fetchone()
            if not linha_venda:
                self.conexao.rollback()
                return False, "Venda não encontrada"

            id_camiseta = linha_venda[0]
            quantidade = linha_venda[1]

            cursor.execute("DELETE FROM tb_venda WHERE ID_VENDA = %s", (id_objeto,))
            cursor.execute("UPDATE tb_camiseta SET ESTOQUE = ESTOQUE + %s WHERE ID_CAMISETA = %s", (quantidade, id_camiseta))

            self.conexao.commit()
            return True, "Venda removida com sucesso"

        except Exception as e:
            self.conexao.rollback()
            return False, f"Erro ao remover venda: {e}"

        finally:
            if cursor:
                cursor.close()

    def atualizar(self, objeto: Venda):
        if not self.conexao:
            return False, "Sem conexão com o BD"

        try:
            cursor = self.conexao.cursor()
            query = "SELECT CAMISETA_ID, QUANTIDADE FROM tb_venda WHERE ID_VENDA = %s FOR UPDATE"
            cursor.execute(query, (objeto.id,))
            venda_atual = cursor.fetchone()
            if not venda_atual:
                self.conexao.rollback()
                return False, "Venda não encontrada"

            camiseta_antiga_id = venda_atual[0]
            quantidade_antiga = int(venda_atual[1])

            cursor.execute("SELECT ESTOQUE, PRECO FROM tb_camiseta WHERE ID_CAMISETA = %s FOR UPDATE", (objeto.camiseta.id,))
            camiseta_nova = cursor.fetchone()
            if not camiseta_nova:
                self.conexao.rollback()
                return False, "Camiseta não encontrada"

            estoque_novo = int(camiseta_nova[0])
            preco_atual = float(camiseta_nova[1])

            if camiseta_antiga_id == objeto.camiseta.id:
                diferenca = objeto.quantidade - quantidade_antiga
                if diferenca > estoque_novo:
                    self.conexao.rollback()
                    return False, "Quantidade maior que o estoque disponivel"
                cursor.execute("UPDATE tb_camiseta SET ESTOQUE = ESTOQUE - %s WHERE ID_CAMISETA = %s", (diferenca, objeto.camiseta.id))
            else:
                cursor.execute("UPDATE tb_camiseta SET ESTOQUE = ESTOQUE + %s WHERE ID_CAMISETA = %s", (quantidade_antiga, camiseta_antiga_id))
                if objeto.quantidade > estoque_novo:
                    self.conexao.rollback()
                    return False, "Quantidade maior que o estoque disponivel"
                cursor.execute("UPDATE tb_camiseta SET ESTOQUE = ESTOQUE - %s WHERE ID_CAMISETA = %s", (objeto.quantidade, objeto.camiseta.id))

            objeto.valor_total = objeto.quantidade * preco_atual

            query = """UPDATE tb_venda
                    SET CLIENTE_ID = %s, CAMISETA_ID = %s, QUANTIDADE = %s,
                        VLTOTAL = %s, DAVENDA = %s
                    WHERE ID_VENDA = %s"""
            cursor.execute(query, (objeto.cliente.id,
                                   objeto.camiseta.id,
                                   objeto.quantidade,
                                   objeto.valor_total,
                                   objeto.data_venda,
                                   objeto.id))
            self.conexao.commit()
            return True, "Venda atualizada com sucesso"

        except Exception as e:
            self.conexao.rollback()
            return False, f"Erro ao atualizar venda: {e}"

        finally:
            if cursor:
                cursor.close()

    def buscar_por_id(self, id_venda: int):
        if not self.conexao:
            return None

        try:
            cursor = self.conexao.cursor()
            query = self._query_listagem() + " WHERE v.ID_VENDA = %s"
            cursor.execute(query, (id_venda,))
            linha = cursor.fetchone()
            return self._linha_para_venda(linha) if linha else None

        except Exception as e:
            print(f"Erro ao buscar venda: {e}")
            return None

        finally:
            if cursor:
                cursor.close()

    def listar_por_cliente(self, nome_cliente: str):
        if not self.conexao:
            return []

        cursor = None
        try:
            cursor = self.conexao.cursor()
            query = self._query_listagem() + """ WHERE c.NOME ILIKE %s ORDER BY v.ID_VENDA"""
            cursor.execute(query, (f"%{nome_cliente.strip()}%",))
            return [self._linha_para_venda(linha) for linha in cursor.fetchall()]

        except Exception as e:
            print(f"Erro ao filtrar vendas por cliente: {e}")
            return []

        finally:
            if cursor:
                cursor.close()
