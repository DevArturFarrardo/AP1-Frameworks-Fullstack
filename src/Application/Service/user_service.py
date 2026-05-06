"""Serviço com regras simples relacionadas ao usuário e códigos de ativação."""
import random

from src.Domain.user import UserDomain
from src.Infrastructure.Model.user import User
from src.config.data_base import db


class UserService:
    """Operações de cadastro de usuário e geração de códigos."""

    @staticmethod
    def generate_activation_code() -> str:
        """Gera um código de 4 dígitos aleatórios para ativação."""
        return "".join(str(random.randint(0, 9)) for _ in range(4))

    @staticmethod
    def create_user(name, email, password):
        """Cria e persiste um novo usuário e retorna o seu UserDomain."""
        user = User(name=name, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        return UserDomain(user.id, user.name, user.email, user.password)
