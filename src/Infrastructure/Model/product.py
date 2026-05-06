"""Model SQLAlchemy do produto e constantes de status."""
from src.config.data_base import db

STATUS_ATIVO = "Ativo"
STATUS_INATIVO = "Inativo"


class Product(db.Model):
    """Tabela `products` vinculada ao seller dono do produto."""

    __tablename__ = "products"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(200), nullable=False)
    preco = db.Column(db.Float, nullable=False)
    quantidade = db.Column(db.Integer, nullable=False, default=0)
    status = db.Column(db.String(20), default=STATUS_ATIVO, nullable=False)
    img = db.Column(db.String(500), nullable=True)
    seller_id = db.Column(db.Integer, db.ForeignKey("sellers.id"), nullable=False)

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
