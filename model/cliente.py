def formataCpf(cpf: str):
    cpf = cpf.strip() if cpf else ""
    numeros = "".join(caractere for caractere in cpf if caractere.isdigit())

    if len(numeros) > 11:
        raise ValueError("CPF não pode ultrapassar 11 dígitos.")

    if len(numeros) != 11:
        raise ValueError("CPF deve conter 11 dígitos.")

    return f"{numeros[0:3]}.{numeros[3:6]}.{numeros[6:9]}-{numeros[9:11]}"

class Cliente:
    def __init__(self, nome: str = "", cpf: str = "", telefone: str = "", email: str = "", id: int = None):
        self.id = id
        self.nome = nome
        self.cpf = cpf
        self.telefone = telefone
        self.email = email

    @property
    def nome(self):
        return self.__nome

    @nome.setter
    def nome(self, nome: str):
        if not nome or not nome.strip():
            raise ValueError("Nome é obrigatório.")
        self.__nome = nome.strip()

    @property
    def cpf(self):
        return self.__cpf

    @cpf.setter
    def cpf(self, cpf: str):
        if not cpf or not cpf.strip():
            raise ValueError("CPF é obrigatório.")
        self.__cpf = formataCpf(cpf)

    @property
    def telefone(self):
        return self.__telefone

    @telefone.setter
    def telefone(self, telefone: str):
        self.__telefone = telefone.strip() if telefone else ""

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, email: str):
        email = email.strip() if email else ""
        if email and "@" not in email:
            raise ValueError("Email deve conter @.")
        self.__email = email

    def exibir_dados(self):
        return (
            f"Nome: {self.nome}\n"
            f"CPF: {self.cpf}\n"
            f"Telefone: {self.telefone}\n"
            f"Email: {self.email}"
        )
