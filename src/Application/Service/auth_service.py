"""Serviço de autenticação que cria, renova e valida JWTs do seller."""
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
)

from src.Infrastructure.Model.seller import Seller, STATUS_ATIVO


class AuthService:
    """Centraliza a lógica de autenticação baseada em JWT."""

    @staticmethod
    def generate_tokens(seller_id: int) -> dict:
        """Gera um access token e um refresh token para o seller.

        O `identity` do JWT é o ID do seller convertido em string.
        Retorna um dicionário com as chaves `access_token` e
        `refresh_token`.
        """
        identity = str(seller_id)
        access_token = create_access_token(identity=identity)
        refresh_token = create_refresh_token(identity=identity)
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
        }

    @staticmethod
    def refresh_access_token() -> str:
        """Gera um novo access token a partir do refresh token atual.

        Deve ser chamado dentro de uma rota protegida pelo decorator
        `@jwt_required(refresh=True)`.
        """
        identity = get_jwt_identity()
        return create_access_token(identity=identity)

    @staticmethod
    def get_current_active_seller() -> Seller:
        """Retorna o seller autenticado, garantindo que está ativo.

        Deve ser chamado dentro de uma rota protegida por
        `@jwt_required()`. Lança `ValueError` quando o token não tem
        identidade, o seller não existe ou está com status diferente
        de `Ativo`.
        """
        identity = get_jwt_identity()
        if not identity:
            raise ValueError("Token inválido.")

        seller = Seller.query.get(int(identity))
        if not seller:
            raise ValueError("Seller não encontrado.")

        if seller.status != STATUS_ATIVO:
            raise ValueError("Conta inativa. Não é possível executar esta operação.")

        return seller
