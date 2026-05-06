"""Model SQLAlchemy da venda."""
from datetime import datetime

from src.config.data_base import db


class Sale(db.Model):
    """Tabela `sales` que registra cada venda realizada por um seller."""

    __tablename__ = "sales"
    id = db.Column(db.Integer, primary_key=True)
    seller_id = db.Column(db.Integer, db.ForeignKey("sellers.id"), nullable=False)
    produto_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    preco_unitario = db.Column(db.Float, nullable=False)
    total = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

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
