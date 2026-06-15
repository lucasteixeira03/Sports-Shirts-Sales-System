import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from dao.db_config import DatabaseConfig
from dao.generic_dao import GenericDAO
from model.cliente import Cliente


class ClienteDAO(GenericDAO):
    def __init__(self):
        self.conexao = DatabaseConfig.get_connection()

    # função usada para mapear linha retornada pelo banco para um objeto Cliente, evita repetição
    def _linha_para_cliente(self, linha):
        return Cliente(
            id=linha[0],
            nome=linha[1],
            cpf=linha[2],
            telefone=linha[3] if linha[3] else "",
            email=linha[4] if linha[4] else ""
        )

    def salvar(self, objeto: Cliente):
        if not self.conexao:
            return False, "Sem conexao com o BD"

        try:
            cursor = self.conexao.cursor()
            query = """
                INSERT INTO tb_cliente (NOME, CPF, TELEFONE, EMAIL)
                VALUES (%s, %s, %s, %s)
                RETURNING ID_CLIENTE
            """
            cursor.execute(query, (objeto.nome, 
                                   objeto.cpf, 
                                   objeto.telefone, 
                                   objeto.email))
            objeto.id = cursor.fetchone()[0]
            self.conexao.commit()
            return True, "Cliente cadastrado com sucesso"

        except Exception as e:
            self.conexao.rollback()
            return False, f"Erro ao inserir cliente: {e}"

        finally:
            if cursor:
                cursor.close()

    def listar_todos(self):
        if not self.conexao:
            return []

        try:
            cursor = self.conexao.cursor()
            query = """
                SELECT ID_CLIENTE, NOME, CPF, TELEFONE, EMAIL
                FROM tb_cliente
                ORDER BY ID_CLIENTE
            """
            cursor.execute(query)
            return [self._linha_para_cliente(linha) for linha in cursor.fetchall()]

        except Exception as e:
            print(f"Erro ao buscar clientes: {e}")
            return []

        finally:
            if cursor:
                cursor.close()

    def remover(self, id_objeto: int):
        if not self.conexao:
            return False, "Sem conexão com o BD"
        
        try:
            cursor = self.conexao.cursor()
            query = "DELETE FROM tb_cliente WHERE ID_CLIENTE = %s"
            cursor.execute(query, (id_objeto,))
            self.conexao.commit()
            return True, "Cliente removido com sucesso"

        except Exception as e:
            self.conexao.rollback()
            return False, f"Erro ao remover cliente: {e}"

        finally:
            if cursor:
                cursor.close()

    def atualizar(self, objeto: Cliente):
        if not self.conexao:
            return False, "Sem conexão com o BD"

        cursor = None
        try:
            cursor = self.conexao.cursor()
            query = """UPDATE tb_cliente
                    SET NOME = %s, CPF = %s, TELEFONE = %s, EMAIL = %s
                    WHERE ID_CLIENTE = %s"""
            cursor.execute(query, (objeto.nome, 
                                   objeto.cpf, 
                                   objeto.telefone, 
                                   objeto.email, 
                                   objeto.id))
            self.conexao.commit()
            return True, "Cliente atualizado com sucesso"

        except Exception as e:
            self.conexao.rollback()
            return False, f"Erro ao atualizar cliente: {e}"

        finally:
            if cursor:
                cursor.close()

    def buscar_por_id(self, id_cliente: int):
        if not self.conexao:
            return None

        try:
            cursor = self.conexao.cursor()
            query = """SELECT ID_CLIENTE, NOME, CPF, TELEFONE, EMAIL
                    FROM tb_cliente
                    WHERE ID_CLIENTE = %s"""
            cursor.execute(query, (id_cliente,))
            linha = cursor.fetchone()
            return self._linha_para_cliente(linha) if linha else None

        except Exception as e:
            print(f"Erro ao buscar cliente: {e}")
            return None

        finally:
            if cursor:
                cursor.close()

    def buscar_por_cpf(self, cpf: str):
        if not self.conexao:
            return None

        try:
            cursor = self.conexao.cursor()
            query = """SELECT ID_CLIENTE, NOME, CPF, TELEFONE, EMAIL
                    FROM tb_cliente
                    WHERE CPF = %s"""
            cursor.execute(query, (cpf,))
            linha = cursor.fetchone()
            return self._linha_para_cliente(linha) if linha else None

        except Exception as e:
            print(f"Erro ao buscar cliente por CPF: {e}")
            return None

        finally:
            if cursor:
                cursor.close()
