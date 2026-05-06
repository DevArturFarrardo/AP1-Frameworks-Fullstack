"""Model SQLAlchemy do usuário genérico."""
from src.config.data_base import db


class User(db.Model):
    """Tabela `users` com cadastro simples (nome, e-mail e senha)."""

    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def to_dict(self):
        """Retorna o usuário como dicionário (inclui a senha bruta)."""
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "password": self.password
        }
