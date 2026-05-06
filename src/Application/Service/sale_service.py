"""Serviço com as regras de negócio das vendas."""
from src.Domain.sale import SaleDomain
from src.Infrastructure.Model.product import Product, STATUS_ATIVO as PRODUCT_ATIVO
from src.Infrastructure.Model.sale import Sale
from src.config.data_base import db


def _to_domain(sale: Sale) -> SaleDomain:
    """Converte o Model Sale no Domain SaleDomain."""
    return SaleDomain(
        id=sale.id,
        seller_id=sale.seller_id,
        produto_id=sale.produto_id,
        quantidade=sale.quantidade,
        preco_unitario=sale.preco_unitario,
        total=sale.total,
        created_at=sale.created_at,
    )


class SaleService:
    """Concentra as operações de negócio relativas às vendas."""

    @staticmethod
    def create_sale(seller_id, produto_id, quantidade):
        """
        Realiza uma venda. Regras:
        - O produto deve existir e pertencer ao seller.
        - O produto não pode estar inativo.
        - A quantidade vendida deve ser > 0 e não maior que o estoque.
        - O preço da venda é o preço atual do produto (preserva histórico).
        """
        if quantidade is None or quantidade <= 0:
            raise ValueError("Quantidade inválida. Deve ser maior que zero.")

        product = Product.query.filter_by(id=produto_id, seller_id=seller_id).first()
        if not product:
            raise ValueError("Produto não encontrado.")

        if product.status != PRODUCT_ATIVO:
            raise ValueError("Produto inativo não pode ser vendido.")

        if quantidade > product.quantidade:
            raise ValueError(
                f"Estoque insuficiente. Disponível: {product.quantidade}."
            )

        preco_unitario = float(product.preco)
        total = round(preco_unitario * int(quantidade), 2)

        sale = Sale(
            seller_id=seller_id,
            produto_id=product.id,
            quantidade=int(quantidade),
            preco_unitario=preco_unitario,
            total=total,
        )

        product.quantidade = product.quantidade - int(quantidade)

        db.session.add(sale)
        db.session.commit()

        return _to_domain(sale)

    @staticmethod
    def list_sales(seller_id):
        """Lista todas as vendas realizadas pelo seller autenticado."""
        sales = Sale.query.filter_by(seller_id=seller_id).order_by(Sale.created_at.desc()).all()
        return [_to_domain(s) for s in sales]
