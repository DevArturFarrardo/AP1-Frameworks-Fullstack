from src.Application.Controllers.user_controller import UserController
from src.Application.Controllers.seller_controller import SellerController
from flask import jsonify, make_response


def init_routes(app):
    @app.route("/api", methods=["GET"])
    def health():
        return make_response(
            jsonify({"mensagem": "API - OK; Docker - Up"}),
            200,
        )

    @app.route("/user", methods=["POST"])
    def register_user():
        return UserController.register_user()

    # Cadastro e ativação do Seller (mini mercado)
    @app.route("/api/sellers", methods=["POST"])
    def create_seller():
        return SellerController.create_seller()

    @app.route("/api/sellers/activate", methods=["POST"])
    def activate_seller():
        return SellerController.activate_seller()


