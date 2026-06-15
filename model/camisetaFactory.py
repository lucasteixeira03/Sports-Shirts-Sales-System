from enum import Enum

class TipoCamiseta(Enum):
    JOGADOR = "JOGADOR"
    RETRO = "RETRO"
    TREINO = "TREINO"
    TORCEDOR = "TORCEDOR"


class Camiseta:
    def __init__(self, selecao: str, modelo: str, tamanho: str, preco: float, estoque: int, tipo, id: int = None):
        self.id = id
        self.__selecao = ""
        self.__modelo = ""
        self.__tamanho = ""
        self.__preco = 0.0
        self.__estoque = 0
        self.__tipo = None

        self.selecao = selecao
        self.modelo = modelo
        self.tamanho = tamanho
        self.preco = preco
        self.estoque = estoque
        self.tipo = tipo

    @property
    def selecao(self):
        return self.__selecao

    @selecao.setter
    def selecao(self, selecao: str):
        if not selecao or not selecao.strip():
            raise ValueError("Selecão é obrigatória.")
        self.__selecao = selecao.strip()

    @property
    def modelo(self):
        return self.__modelo

    @modelo.setter
    def modelo(self, modelo: str):
        if not modelo or not modelo.strip():
            raise ValueError("Modelo é obrigatório.")
        self.__modelo = modelo.strip()

    @property
    def tamanho(self):
        return self.__tamanho

    @tamanho.setter
    def tamanho(self, tamanho: str):
        if not tamanho or not tamanho.strip():
            raise ValueError("Tamanho é obrigatório.")
        self.__tamanho = tamanho.strip().upper()

    @property
    def preco(self):
        return self.__preco

    @preco.setter
    def preco(self, preco):
        if preco is None:
            raise ValueError("O preço é obrigatório.")

        try:
            preco_float = float(str(preco).replace(",", "."))
        except ValueError:
            raise ValueError("O preço deve ser um valor numérico.")

        if preco_float <= 0:
            raise ValueError("O preço da camiseta deve ser maior que zero.")

        self.__preco = preco_float

    @property
    def estoque(self):
        return self.__estoque

    @estoque.setter
    def estoque(self, estoque: int):
        if estoque is None:
            raise ValueError("É obrigatório definir uma quantidade de estoque.")

        try:
            estoque_int = int(estoque)
        except ValueError:
            raise ValueError("Estoque deve ser um número inteiro.")

        if estoque_int < 0:
            raise ValueError("Estoque deve ser maior ou igual a zero.")

        self.__estoque = estoque_int

    @property
    def tipo(self):
        return self.__tipo

    @tipo.setter
    def tipo(self, tipo):
        if isinstance(tipo, TipoCamiseta):
            self.__tipo = tipo
            return

        try:
            self.__tipo = TipoCamiseta[str(tipo).strip().upper()]
        except KeyError:
            tipos_validos = ", ".join(tipo_camiseta.value for tipo_camiseta in TipoCamiseta)
            raise ValueError(f"Tipo de camiseta inválido. Use: {tipos_validos}.")

    def reduzir_estoque(self, quantidade: int):
        quantidade = int(quantidade)
        if quantidade <= 0:
            raise ValueError("Quantidade deve ser maior que zero.")
        if quantidade > self.estoque:
            raise ValueError("Quantidade maior que o estoque disponivel.")
        self.estoque = self.estoque - quantidade

    def exibir_dados(self):
        return (
            f"Selecao: {self.selecao}\n"
            f"Modelo: {self.modelo}\n"
            f"Tamanho: {self.tamanho}\n"
            f"Preco: R$ {self.preco:.2f}\n"
            f"Estoque: {self.estoque}\n"
            f"Tipo: {self.tipo.value}"
        )


class CamisetaFactory:
    @staticmethod
    def criar_camiseta(tipo: str, selecao: str, modelo: str, tamanho: str, preco: float, estoque: int, id: int = None):
        tipo_normalizado = str(tipo).strip().upper()
        if tipo_normalizado not in TipoCamiseta.__members__:
            tipos_validos = ", ".join(tipo_camiseta.value for tipo_camiseta in TipoCamiseta)
            raise ValueError(f"Tipo de camiseta inválido. Use: {tipos_validos}.")

        return Camiseta(
            id=id,
            selecao=selecao,
            modelo=modelo,
            tamanho=tamanho,
            preco=preco,
            estoque=estoque,
            tipo=tipo_normalizado
        )
