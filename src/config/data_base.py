"""Configuração e inicialização do banco de dados via Flask-SQLAlchemy."""
import os

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def init_db(app):
    """Inicializa o banco de dados na aplicação Flask informada.

    Por padrão usa SQLite, com o arquivo `market_management.db` criado
    na raiz do projeto. Não exige Docker e é ideal para desenvolvimento.

    Para usar MySQL com Docker:
        1. Comente as três linhas abaixo do bloco SQLite.
        2. Descomente a linha do MySQL.
        3. Execute `docker-compose up`.

    Linha de configuração para MySQL:
        app.config['SQLALCHEMY_DATABASE_URI'] = (
            'mysql+mysqlconnector://root:root@mysql57:3306/market_management'
        )

    Após configurar a URI, todos os models são importados para garantir
    que as tabelas correspondentes sejam criadas automaticamente por
    `db.create_all()`.
    """
    basedir = os.path.abspath(os.path.dirname(__file__))
    db_path = os.path.join(basedir, '..', '..', 'market_management.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    from src.Infrastructure.Model.user import User
    from src.Infrastructure.Model.seller import Seller
    from src.Infrastructure.Model.product import Product
    from src.Infrastructure.Model.sale import Sale

    with app.app_context():
        db.create_all()
