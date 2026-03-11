import random

from src.Domain.user import UserDomain
from src.Infrastructure.Model.user import User
from src.config.data_base import db


class UserService:
    @staticmethod
    def generate_activation_code() -> str:
        """Gera um código de 4 números aleatórios para ativação (ex.: SMS/WhatsApp)."""
        return "".join(str(random.randint(0, 9)) for _ in range(4))

    @staticmethod
    def create_user(name, email, password):
        user = User(name=name, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        return UserDomain(user.id, user.name, user.email, user.password)
