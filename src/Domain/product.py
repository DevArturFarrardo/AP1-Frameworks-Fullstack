"""Domínio do produto usado nas respostas da API."""


class ProductDomain:
    """Representa um produto para uso fora da camada de banco de dados."""

    def __init__(self, id, nome, preco, quantidade, status, img, seller_id):
        """Cria um novo ProductDomain com os campos informados."""
        self.id = id
        self.nome = nome
        self.preco = preco
        self.quantidade = quantidade
        self.status = status
        self.img = img
        self.seller_id = seller_id

    def to_dict(self):
        """Retorna o produto como dicionário pronto para serialização JSON."""
        return {
            "id": self.id,
            "nome": self.nome,
            "preco": self.preco,
            "quantidade": self.quantidade,
            "status": self.status,
            "img": self.img,
            "seller_id": self.seller_id,
        }
