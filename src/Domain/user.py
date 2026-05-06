"""Domínio do usuário genérico usado nas respostas da API."""


class UserDomain:
    """Representa um usuário simples para retorno na API."""

    def __init__(self, id, name, email, password):
        """Cria um novo UserDomain com os campos informados."""
        self.id = id
        self.name = name
        self.email = email

    def to_dict(self):
        """Retorna o usuário como dicionário pronto para serialização JSON."""
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
        }
