"""Registro de todas as rotas HTTP da API."""
from flask import jsonify, make_response

from src.Application.Controllers.user_controller import UserController
from src.Application.Controllers.seller_controller import SellerController
from src.Application.Controllers.product_controller import ProductController
from src.Application.Controllers.sale_controller import SaleController


def init_routes(app):
    """Registra todas as rotas da API na aplicação Flask informada.

    Grupos de rotas:
        - Health check: GET /api
        - Cadastro genérico de usuário: POST /user
        - Cadastro e ativação do seller: POST /api/sellers,
          POST /api/sellers/activate
        - Autenticação do seller (JWT): POST /api/sellers/login,
          POST /api/sellers/refresh
        - Gerenciamento de produtos (protegido por JWT):
          POST/GET /api/products, GET/PUT /api/products/<id>,
          PATCH /api/products/<id>/inactivate
        - Vendas (protegido por JWT): POST/GET /api/sales
    """

    @app.route("/api", methods=["GET"])
    def health():
        """Retorna um status simples para verificar se a API está no ar."""
        return make_response(
            jsonify({"mensagem": "API - OK; Docker - Up"}),
            200,
        )

    @app.route("/user", methods=["POST"])
    def register_user():
        """Cadastra um usuário genérico (não é o fluxo de seller)."""
        return UserController.register_user()

    @app.route("/api/sellers", methods=["POST"])
    def create_seller():
        """Cadastra um novo seller (mini mercado) com status Inativo."""
        return SellerController.create_seller()

    @app.route("/api/sellers/activate", methods=["POST"])
    def activate_seller():
        """Ativa o seller a partir do código de 4 dígitos recebido."""
        return SellerController.activate_seller()

    @app.route("/api/sellers/login", methods=["POST"])
    def login_seller():
        """Autentica o seller e devolve access token e refresh token."""
        return SellerController.login_seller()

    @app.route("/api/sellers/refresh", methods=["POST"])
    def refresh_token():
        """Gera um novo access token a partir do refresh token enviado."""
        return SellerController.refresh_token()

    @app.route("/api/products", methods=["POST"])
    def create_product():
        """Cadastra um novo produto para o seller autenticado."""
        return ProductController.create_product()

    @app.route("/api/products", methods=["GET"])
    def list_products():
        """Lista todos os produtos do seller autenticado."""
        return ProductController.list_products()

    @app.route("/api/products/<int:product_id>", methods=["GET"])
    def get_product(product_id):
        """Retorna os detalhes de um produto do seller autenticado."""
        return ProductController.get_product(product_id)

    @app.route("/api/products/<int:product_id>", methods=["PUT"])
    def update_product(product_id):
        """Edita um produto do seller autenticado (campos parciais)."""
        return ProductController.update_product(product_id)

    @app.route("/api/products/<int:product_id>/inactivate", methods=["PATCH"])
    def inactivate_product(product_id):
        """Inativa um produto do seller autenticado."""
        return ProductController.inactivate_product(product_id)

    @app.route("/api/sales", methods=["POST"])
    def create_sale():
        """Registra uma venda para o seller autenticado."""
        return SaleController.create_sale()

    @app.route("/api/sales", methods=["GET"])
    def list_sales():
        """Lista as vendas realizadas pelo seller autenticado."""
        return SaleController.list_sales()
