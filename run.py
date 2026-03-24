import os
from datetime import timedelta
from pathlib import Path

from dotenv import load_dotenv

# Garante que .env seja carregado da pasta do projeto (onde fica run.py)
_env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=_env_path)

from flask import Flask
from flask_jwt_extended import JWTManager
from src.config.data_base import init_db
from src.routes import init_routes

jwt = JWTManager()

def create_app():
    """
    Função que cria e configura a aplicação Flask.
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
