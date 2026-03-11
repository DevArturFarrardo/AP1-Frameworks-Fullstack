from flask import request, jsonify, make_response

from src.Application.Service.seller_service import SellerService


class SellerController:
    @staticmethod
    def create_seller():
        """POST /api/sellers - Cadastro de mini mercado (seller)."""
        data = request.get_json() or {}
        nome = data.get("nome")
        cnpj = data.get("cnpj")
        email = data.get("email")
        celular = data.get("celular")
        senha = data.get("senha")

        required = {"nome": nome, "cnpj": cnpj, "email": email, "celular": celular, "senha": senha}
        missing = [k for k, v in required.items() if not v]
        if missing:
            return make_response(
                jsonify({"erro": "Campos obrigatórios ausentes", "campos": missing}),
                400,
            )

        try:
            seller_domain, activation_code = SellerService.create_seller(
                nome=nome,
                cnpj=cnpj,
                email=email,
                celular=celular,
                senha=senha,
            )
            response = {
                "mensagem": "Seller cadastrado com sucesso. Use o código de ativação para ativar a conta (integração WhatsApp em breve).",
                "seller": seller_domain.to_dict(),
                "codigo_ativacao": activation_code,
            }
            return make_response(jsonify(response), 201)
        except ValueError as e:
            return make_response(jsonify({"erro": str(e)}), 400)

    @staticmethod
    def activate_seller():
        """POST /api/sellers/activate - Ativação do seller com código recebido (ex.: via WhatsApp)."""
        data = request.get_json() or {}
        celular = data.get("celular")
        codigo = data.get("codigo")

        if not celular or not codigo:
            return make_response(
                jsonify({"erro": "Campos obrigatórios: celular e codigo"}),
                400,
            )

        # Aceita código como string de 4 dígitos
        codigo = str(codigo).strip()
        if len(codigo) != 4 or not codigo.isdigit():
            return make_response(
                jsonify({"erro": "Código deve ter exatamente 4 dígitos"}),
                400,
            )

        try:
            seller_domain = SellerService.activate_seller(celular=celular, codigo=codigo)
            return make_response(
                jsonify({
                    "mensagem": "Conta ativada com sucesso. Agora você pode fazer login.",
                    "seller": seller_domain.to_dict(),
                }),
                200,
            )
        except ValueError as e:
            return make_response(jsonify({"erro": str(e)}), 400)
