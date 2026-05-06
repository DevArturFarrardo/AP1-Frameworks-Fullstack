"""Controller HTTP responsável pelos endpoints de produtos."""
from flask import request, jsonify, make_response
from flask_jwt_extended import jwt_required

from src.Application.Service.auth_service import AuthService
from src.Application.Service.product_service import ProductService


class ProductController:
    """Agrupa os handlers HTTP relativos aos produtos."""

    @staticmethod
    @jwt_required()
    def create_product():
        """POST /api/products - Cadastra um novo produto para o seller autenticado."""
        try:
            seller = AuthService.get_current_active_seller()
        except ValueError as e:
            return make_response(jsonify({"erro": str(e)}), 401)

        data = request.get_json() or {}
        nome = data.get("nome")
        preco = data.get("preco")
        quantidade = data.get("quantidade")
        status = data.get("status")
        img = data.get("img")

        required = {"nome": nome, "preco": preco, "quantidade": quantidade}
        missing = [k for k, v in required.items() if v is None]
        if missing:
            return make_response(
                jsonify({"erro": "Campos obrigatórios ausentes", "campos": missing}),
                400,
            )

        try:
            product_domain = ProductService.create_product(
                seller_id=seller.id,
                nome=nome,
                preco=preco,
                quantidade=quantidade,
                status=status,
                img=img,
            )
            return make_response(
                jsonify({
                    "mensagem": "Produto cadastrado com sucesso.",
                    "produto": product_domain.to_dict(),
                }),
                201,
            )
        except ValueError as e:
            return make_response(jsonify({"erro": str(e)}), 400)

    @staticmethod
    @jwt_required()
    def list_products():
        """GET /api/products - Lista todos os produtos do seller autenticado."""
        try:
            seller = AuthService.get_current_active_seller()
        except ValueError as e:
            return make_response(jsonify({"erro": str(e)}), 401)

        produtos = ProductService.list_products(seller_id=seller.id)
        return make_response(
            jsonify({"produtos": [p.to_dict() for p in produtos]}),
            200,
        )

    @staticmethod
    @jwt_required()
    def get_product(product_id):
        """GET /api/products/<id> - Detalhes de um produto do seller autenticado."""
        try:
            seller = AuthService.get_current_active_seller()
        except ValueError as e:
            return make_response(jsonify({"erro": str(e)}), 401)

        try:
            product_domain = ProductService.get_product(seller_id=seller.id, product_id=product_id)
            return make_response(jsonify({"produto": product_domain.to_dict()}), 200)
        except ValueError as e:
            return make_response(jsonify({"erro": str(e)}), 404)

    @staticmethod
    @jwt_required()
    def update_product(product_id):
        """PUT /api/products/<id> - Edita os dados de um produto do seller."""
        try:
            seller = AuthService.get_current_active_seller()
        except ValueError as e:
            return make_response(jsonify({"erro": str(e)}), 401)

        data = request.get_json() or {}
        try:
            product_domain = ProductService.update_product(
                seller_id=seller.id,
                product_id=product_id,
                data=data,
            )
            return make_response(
                jsonify({
                    "mensagem": "Produto atualizado com sucesso.",
                    "produto": product_domain.to_dict(),
                }),
                200,
            )
        except ValueError as e:
            return make_response(jsonify({"erro": str(e)}), 400)

    @staticmethod
    @jwt_required()
    def inactivate_product(product_id):
        """PATCH /api/products/<id>/inactivate - Inativa um produto do seller."""
        try:
            seller = AuthService.get_current_active_seller()
        except ValueError as e:
            return make_response(jsonify({"erro": str(e)}), 401)

        try:
            product_domain = ProductService.inactivate_product(
                seller_id=seller.id,
                product_id=product_id,
            )
            return make_response(
                jsonify({
                    "mensagem": "Produto inativado com sucesso.",
                    "produto": product_domain.to_dict(),
                }),
                200,
            )
        except ValueError as e:
            return make_response(jsonify({"erro": str(e)}), 404)
