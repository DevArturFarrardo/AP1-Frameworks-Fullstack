"""Serviço com as regras de negócio dos produtos."""
from src.Domain.product import ProductDomain
from src.Infrastructure.Model.product import Product, STATUS_ATIVO, STATUS_INATIVO
from src.config.data_base import db


def _to_domain(product: Product) -> ProductDomain:
    """Converte o Model Product no Domain ProductDomain."""
    return ProductDomain(
        id=product.id,
        nome=product.nome,
        preco=product.preco,
        quantidade=product.quantidade,
        status=product.status,
        img=product.img,
        seller_id=product.seller_id,
    )


class ProductService:
    """Concentra as operações de negócio relativas aos produtos."""

    @staticmethod
    def create_product(seller_id, nome, preco, quantidade, status=None, img=None):
        """
        Cria um novo produto pertencente ao seller informado.
        Regras:
        - preco deve ser >= 0
        - quantidade deve ser >= 0
        - status deve ser "Ativo" ou "Inativo" (padrão: Ativo)
        """
        if preco is None or preco < 0:
            raise ValueError("Preço inválido. Deve ser maior ou igual a zero.")
        if quantidade is None or quantidade < 0:
            raise ValueError("Quantidade inválida. Deve ser maior ou igual a zero.")

        if status is None:
            status = STATUS_ATIVO
        if status not in (STATUS_ATIVO, STATUS_INATIVO):
            raise ValueError("Status inválido. Use 'Ativo' ou 'Inativo'.")

        product = Product(
            nome=nome,
            preco=float(preco),
            quantidade=int(quantidade),
            status=status,
            img=img,
            seller_id=seller_id,
        )
        db.session.add(product)
        db.session.commit()

        return _to_domain(product)

    @staticmethod
    def list_products(seller_id):
        """Lista todos os produtos do seller autenticado."""
        products = Product.query.filter_by(seller_id=seller_id).all()
        return [_to_domain(p) for p in products]

    @staticmethod
    def get_product(seller_id, product_id):
        """
        Retorna um produto específico do seller. Lança ValueError se o produto
        não existir ou pertencer a outro seller.
        """
        product = Product.query.filter_by(id=product_id, seller_id=seller_id).first()
        if not product:
            raise ValueError("Produto não encontrado.")
        return _to_domain(product)

    @staticmethod
    def update_product(seller_id, product_id, data):
        """
        Atualiza os campos enviados em 'data' (dict). Apenas os campos presentes
        são atualizados. Só atualiza produtos do próprio seller.
        """
        product = Product.query.filter_by(id=product_id, seller_id=seller_id).first()
        if not product:
            raise ValueError("Produto não encontrado.")

        if "nome" in data and data["nome"] is not None:
            product.nome = data["nome"]

        if "preco" in data and data["preco"] is not None:
            if data["preco"] < 0:
                raise ValueError("Preço inválido. Deve ser maior ou igual a zero.")
            product.preco = float(data["preco"])

        if "quantidade" in data and data["quantidade"] is not None:
            if data["quantidade"] < 0:
                raise ValueError("Quantidade inválida. Deve ser maior ou igual a zero.")
            product.quantidade = int(data["quantidade"])

        if "status" in data and data["status"] is not None:
            if data["status"] not in (STATUS_ATIVO, STATUS_INATIVO):
                raise ValueError("Status inválido. Use 'Ativo' ou 'Inativo'.")
            product.status = data["status"]

        if "img" in data:
            product.img = data["img"]

        db.session.commit()
        return _to_domain(product)

    @staticmethod
    def inactivate_product(seller_id, product_id):
        """Marca o produto como Inativo. Só atua sobre produtos do próprio seller."""
        product = Product.query.filter_by(id=product_id, seller_id=seller_id).first()
        if not product:
            raise ValueError("Produto não encontrado.")

        product.status = STATUS_INATIVO
        db.session.commit()
        return _to_domain(product)
