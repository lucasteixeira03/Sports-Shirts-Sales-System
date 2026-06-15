from datetime import date, datetime

from model.camisetaFactory import Camiseta
from model.cliente import Cliente


class Venda:
    def __init__(self, cliente: Cliente, camiseta: Camiseta, quantidade: int, id: int = None,  valor_total: float = None, data_venda=None, validar_estoque: bool = True):
        self.id = id
        self.__cliente = None
        self.__camiseta = None
        self.__quantidade = 0
        self.__valor_total = 0.0
        self.__data_venda = None
        self.__validar_estoque = validar_estoque

        self.cliente = cliente
        self.camiseta = camiseta
        self.quantidade = quantidade
        self.valor_total = valor_total if valor_total is not None else self.calcular_valor_total()
        self.data_venda = data_venda if data_venda else date.today()

    @property
    def cliente(self):
        return self.__cliente

    @cliente.setter
    def cliente(self, cliente: Cliente):
        if not isinstance(cliente, Cliente):
            raise ValueError("Venda deve possuir um cliente válido.")
        self.__cliente = cliente

    @property
    def camiseta(self):
        return self.__camiseta

    @camiseta.setter
    def camiseta(self, camiseta: Camiseta):
        if not isinstance(camiseta, Camiseta):
            raise ValueError("Venda deve possuir uma camiseta válido.")
        self.__camiseta = camiseta

    @property
    def quantidade(self):
        return self.__quantidade

    @quantidade.setter
    def quantidade(self, quantidade: int):
        try:
            quantidade_int = int(quantidade)
        except (TypeError, ValueError):
            raise ValueError("Quantidade deve ser um número inteiro.")

        if quantidade_int <= 0:
            raise ValueError("Quantidade deve ser maior que zero.")

        if self.__validar_estoque and self.camiseta and quantidade_int > self.camiseta.estoque:
            raise ValueError("Quantidade maior que o estoque disponivel.")

        self.__quantidade = quantidade_int

    @property
    def valor_total(self):
        return self.__valor_total

    @valor_total.setter
    def valor_total(self, valor_total):
        try:
            valor_float = float(str(valor_total).replace(",", "."))
        except ValueError:
            raise ValueError("Valor total deve ser numérico.")

        if valor_float < 0:
            raise ValueError("Valor total não pode ser negativo.")

        self.__valor_total = valor_float

    @property
    def data_venda(self):
        return self.__data_venda

    @data_venda.setter
    def data_venda(self, data_venda):
        if isinstance(data_venda, date) and not isinstance(data_venda, datetime):
            self.__data_venda = data_venda
            return

        if isinstance(data_venda, datetime):
            self.__data_venda = data_venda.date()
            return

        if isinstance(data_venda, str):
            try:
                self.__data_venda = date.fromisoformat(data_venda)
            except ValueError:
                self.__data_venda = datetime.fromisoformat(data_venda).date()
            return

        raise ValueError("Data da venda inválida.")

    def calcular_valor_total(self):
        return self.quantidade * self.camiseta.preco

    def baixar_estoque(self):
        self.camiseta.reduzir_estoque(self.quantidade)

    def exibir_dados(self):
        return (
            f"Cliente: {self.cliente.nome}\n"
            f"Camiseta: {self.camiseta.selecao} - {self.camiseta.modelo}\n"
            f"Quantidade: {self.quantidade}\n"
            f"Valor total: R$ {self.valor_total:.2f}\n"
            f"Data da venda: {self.data_venda.strftime('%d/%m/%Y')}"
        )
