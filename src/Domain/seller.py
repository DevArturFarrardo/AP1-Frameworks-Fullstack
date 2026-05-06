"""Domínio do seller (mini mercado) usado nas respostas da API."""


class SellerDomain:
    """Representa um seller para uso fora da camada de banco de dados."""

    def __init__(self, id, nome, cnpj, email, celular, status):
        """Cria um novo SellerDomain com os campos informados."""
        self.id = id
        self.nome = nome
        self.cnpj = cnpj
        self.email = email
        self.celular = celular
        self.status = status

    def to_dict(self):
        """Retorna o seller como dicionário pronto para serialização JSON."""
        return {
            "id": self.id,
            "nome": self.nome,
            "cnpj": self.cnpj,
            "email": self.email,
            "celular": self.celular,
            "status": self.status,
        }
