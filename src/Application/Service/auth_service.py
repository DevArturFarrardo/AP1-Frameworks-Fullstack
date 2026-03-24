from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
)


class AuthService:
    @staticmethod
    def generate_tokens(seller_id: int) -> dict:
        """
        Gera um access token e um refresh token para o seller autenticado.
        O identity do JWT é o ID do seller.
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
        """
        Gera um novo access token a partir do refresh token atual.
        Deve ser chamado dentro de uma rota protegida por @jwt_required(refresh=True).
        """
        identity = get_jwt_identity()
        return create_access_token(identity=identity)
