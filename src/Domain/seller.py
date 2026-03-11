class SellerDomain:
    def __init__(self, id, nome, cnpj, email, celular, status):
        self.id = id
        self.nome = nome
        self.cnpj = cnpj
        self.email = email
        self.celular = celular
        self.status = status

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "cnpj": self.cnpj,
            "email": self.email,
            "celular": self.celular,
            "status": self.status,
        }
