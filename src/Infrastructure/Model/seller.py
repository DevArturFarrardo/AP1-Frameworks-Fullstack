from src.config.data_base import db

STATUS_INATIVO = "Inativo"
STATUS_ATIVO = "Ativo"


class Seller(db.Model):
    __tablename__ = "sellers"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(200), nullable=False)
    cnpj = db.Column(db.String(18), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    celular = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(20), default=STATUS_INATIVO, nullable=False)
    activation_code = db.Column(db.String(4), nullable=True)
    activation_code_expires_at = db.Column(db.DateTime, nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "cnpj": self.cnpj,
            "email": self.email,
            "celular": self.celular,
            "status": self.status,
        }
