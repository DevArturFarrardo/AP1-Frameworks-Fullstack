"""Domínio da venda usado nas respostas da API."""


class SaleDomain:
    """Representa uma venda para uso fora da camada de banco de dados."""

    def __init__(self, id, seller_id, produto_id, quantidade, preco_unitario, total, created_at):
        """Cria um novo SaleDomain com os campos informados."""
        self.id = id
        self.seller_id = seller_id
        self.produto_id = produto_id
        self.quantidade = quantidade
        self.preco_unitario = preco_unitario
        self.total = total
        self.created_at = created_at

    def to_dict(self):
        """Retorna a venda como dicionário pronto para serialização JSON."""
        return {
            "id": self.id,
            "seller_id": self.seller_id,
            "produto_id": self.produto_id,
            "quantidade": self.quantidade,
            "preco_unitario": self.preco_unitario,
            "total": self.total,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
