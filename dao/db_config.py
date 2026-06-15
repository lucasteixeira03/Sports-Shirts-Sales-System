import psycopg2
from psycopg2 import Error


class DatabaseConfig:
    @staticmethod
    def get_connection():
        try:
            conexao = psycopg2.connect(
                user="postgres",
                password="Sacul123@",   ## Lembrar de trocar para localhost quando projeto finalizar
                host="localhost",
                port="5432",
                database="lpoo_projeto_lucas_teixeira"
            )
            return conexao
        except Error as e:
            print(f"Erro ao conectar o banco de dados: {e}")
            return None

    @staticmethod
    def testar_conexao():
        conexao = DatabaseConfig.get_connection()
        if not conexao:
            return False, "Não foi possivel conectar ao banco de dados."

        conexao.close()
        return True, "Conexão com o banco de dados realizada com sucesso."
