from datetime import datetime, timedelta

from werkzeug.security import generate_password_hash, check_password_hash

from src.Application.Service.auth_service import AuthService
from src.Application.Service.user_service import UserService
from src.Domain.seller import SellerDomain
from src.Infrastructure.Model.seller import Seller, STATUS_ATIVO, STATUS_INATIVO
from src.Infrastructure.WhatsApp import TwilioWhatsApp
from src.config.data_base import db

CODE_VALID_MINUTES = 15


class SellerService:
    @staticmethod
    def create_seller(nome, cnpj, email, celular, senha):
        """
        Cadastra um novo seller com status Inativo, gera código de 4 dígitos
        e envia via WhatsApp (Twilio). Se Twilio não estiver configurado, o código
        ainda é retornado na resposta para testes.
        """
        if Seller.query.filter_by(email=email).first():
            raise ValueError("Já existe um seller cadastrado com este e-mail.")
        if Seller.query.filter_by(cnpj=cnpj).first():
            raise ValueError("Já existe um seller cadastrado com este CNPJ.")

        activation_code = UserService.generate_activation_code()
        expires_at = datetime.utcnow() + timedelta(minutes=CODE_VALID_MINUTES)

        seller = Seller(
            nome=nome,
            cnpj=cnpj,
            email=email,
            celular=celular,
            password=generate_password_hash(senha),
            status=STATUS_INATIVO,
            activation_code=activation_code,
            activation_code_expires_at=expires_at,
        )
        db.session.add(seller)
        db.session.commit()

        whatsapp = TwilioWhatsApp()
        whatsapp.send_activation_code(to_phone=celular, code=activation_code)

        return SellerDomain(
            seller.id,
            seller.nome,
            seller.cnpj,
            seller.email,
            seller.celular,
            seller.status,
        ), activation_code

    @staticmethod
    def activate_seller(celular, codigo):
        """
        Ativa o seller quando o código de 4 dígitos confere.
        Somente sellers ativados poderão fazer login.
        """
        seller = Seller.query.filter_by(celular=celular).first()
        if not seller:
            raise ValueError("Nenhum seller encontrado com este celular.")

        if seller.status == STATUS_ATIVO:
            raise ValueError("Conta já está ativa.")

        if not seller.activation_code:
            raise ValueError("Código de ativação não encontrado. Solicite um novo cadastro.")

        if seller.activation_code_expires_at and datetime.utcnow() > seller.activation_code_expires_at:
            raise ValueError("Código de ativação expirado.")

        if seller.activation_code != codigo:
            raise ValueError("Código de ativação inválido.")

        seller.status = STATUS_ATIVO
        seller.activation_code = None
        seller.activation_code_expires_at = None
        db.session.commit()

        return SellerDomain(
            seller.id,
            seller.nome,
            seller.cnpj,
            seller.email,
            seller.celular,
            seller.status,
        )

    @staticmethod
    def login(email, senha):
        """
        Autentica o seller por e-mail e senha.
        Sellers com status Inativo são bloqueados.
        Retorna o SellerDomain, access_token e refresh_token.
        """
        seller = Seller.query.filter_by(email=email).first()
        if not seller or not check_password_hash(seller.password, senha):
            raise ValueError("E-mail ou senha inválidos.")

        if seller.status != STATUS_ATIVO:
            raise ValueError("Conta inativa. Ative sua conta antes de fazer login.")

        tokens = AuthService.generate_tokens(seller_id=seller.id)

        seller_domain = SellerDomain(
            seller.id,
            seller.nome,
            seller.cnpj,
            seller.email,
            seller.celular,
            seller.status,
        )

        return seller_domain, tokens
