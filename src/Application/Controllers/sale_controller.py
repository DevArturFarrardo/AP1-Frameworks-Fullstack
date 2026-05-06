"""Controller HTTP responsável pelos endpoints de vendas."""
from flask import request, jsonify, make_response
from flask_jwt_extended import jwt_required

from src.Application.Service.auth_service import AuthService
from src.Application.Service.sale_service import SaleService


class SaleController:
    """Agrupa os handlers HTTP relativos às vendas."""

    @staticmethod
    @jwt_required()
    def create_sale():
        """POST /api/sales - Realiza uma venda para o seller autenticado."""
        try:
            seller = AuthService.get_current_active_seller()
        except ValueError as e:
            return make_response(jsonify({"erro": str(e)}), 401)

        data = request.get_json() or {}
        produto_id = data.get("produtoId") or data.get("produto_id")
        quantidade = data.get("quantidade")

        if produto_id is None or quantidade is None:
            return make_response(
                jsonify({"erro": "Campos obrigatórios: produtoId e quantidade"}),
                400,
            )

        try:
            sale_domain = SaleService.create_sale(
                seller_id=seller.id,
                produto_id=int(produto_id),
                quantidade=int(quantidade),
            )
            return make_response(
                jsonify({
                    "mensagem": "Venda registrada com sucesso.",
                    "venda": sale_domain.to_dict(),
                }),
                201,
            )
        except ValueError as e:
            return make_response(jsonify({"erro": str(e)}), 400)

    @staticmethod
    @jwt_required()
    def list_sales():
        """GET /api/sales - Lista todas as vendas do seller autenticado."""
        try:
            seller = AuthService.get_current_active_seller()
        except ValueError as e:
            return make_response(jsonify({"erro": str(e)}), 401)

        vendas = SaleService.list_sales(seller_id=seller.id)
        return make_response(
            jsonify({"vendas": [v.to_dict() for v in vendas]}),
            200,
        )
