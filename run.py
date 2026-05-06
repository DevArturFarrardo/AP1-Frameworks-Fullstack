"""Ponto de entrada da aplicação Flask.

Carrega as variáveis de ambiente do arquivo `.env` localizado na mesma
pasta deste módulo e cria a aplicação chamando `create_app()`.
"""
import os
from datetime import timedelta
from pathlib import Path

from dotenv import load_dotenv

_env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=_env_path)

from flask import Flask
from flask_jwt_extended import JWTManager
from src.config.data_base import init_db
from src.routes import init_routes

jwt = JWTManager()


def create_app():
    """Cria e configura a aplicação Flask.

    - Define a chave secreta do JWT a partir da variável de ambiente
      `JWT_SECRET_KEY` (com fallback para desenvolvimento).
    - Define o tempo de expiração do access token (1 hora) e do refresh
      token (30 dias).
    - Inicializa o banco de dados e registra as rotas da API.
    """
    app = Flask(__name__)

    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "super-secret-change-me")
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)

    jwt.init_app(app)

    init_db(app)

    init_routes(app)

    return app


app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
