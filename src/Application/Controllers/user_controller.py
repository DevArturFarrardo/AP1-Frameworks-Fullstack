"""Controller HTTP do endpoint de cadastro genérico de usuário."""
from flask import request, jsonify, make_response
from src.Application.Service.user_service import UserService


class UserController:
    """Agrupa os handlers HTTP relativos ao usuário genérico."""

    @staticmethod
    def register_user():
        """Cria um usuário a partir dos campos `name`, `email` e `password`."""
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')

        if not name or not email or not password:
            return make_response(jsonify({"erro": "Campos obrigatórios ausentes"}), 400)

        user = UserService.create_user(name, email, password)
        return make_response(jsonify({
            "mensagem": "Usuário salvo com sucesso.",
            "usuario": user.to_dict()
        }), 200)
