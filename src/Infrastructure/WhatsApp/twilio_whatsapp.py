"""Cliente para envio de mensagens via WhatsApp usando a API da Twilio."""
import os
import json
import logging

import requests

logger = logging.getLogger(__name__)

TWILIO_MESSAGES_URL = "https://api.twilio.com/2010-04-01/Accounts/{account_sid}/Messages.json"


class TwilioWhatsApp:
    """Cliente para envio de mensagens WhatsApp via Twilio.

    Suporta tanto o envio via template aprovado (Content API) quanto
    via texto simples (campo `Body`), útil para uso em sandbox.
    Credenciais e números são lidos de variáveis de ambiente:

    Variáveis utilizadas:
        - TWILIO_ACCOUNT_SID: SID da conta Twilio.
        - TWILIO_AUTH_TOKEN: token de autenticação.
        - TWILIO_WHATSAPP_FROM: número remetente no formato
          `whatsapp:+...` (padrão: número de sandbox da Twilio).
        - TWILIO_CONTENT_SID: SID do template aprovado.
        - TWILIO_SEND_CODE_WITH_BODY: se "1"/"true"/"yes", envia o
          código como texto simples no `Body` em vez de usar template.
    """

    def __init__(
        self,
        account_sid=None,
        auth_token=None,
        from_whatsapp=None,
        content_sid=None,
    ):
        """Inicializa o cliente com credenciais explícitas ou via env."""
        self.account_sid = account_sid or os.environ.get("TWILIO_ACCOUNT_SID")
        self.auth_token = auth_token or os.environ.get("TWILIO_AUTH_TOKEN")
        self.from_whatsapp = from_whatsapp or os.environ.get("TWILIO_WHATSAPP_FROM", "whatsapp:+14155238886")
        self.content_sid = content_sid or os.environ.get("TWILIO_CONTENT_SID", "HXb5b62575e6e4ff6129ad7c8efe1f983e")

    def _ensure_whatsapp_prefix(self, number: str) -> str:
        """Garante que o número telefônico tenha o prefixo `whatsapp:`."""
        number = number.strip()
        if not number.startswith("whatsapp:"):
            number = f"whatsapp:{number}"
        return number

    def _is_configured(self) -> bool:
        """Indica se as credenciais mínimas estão presentes."""
        return bool(self.account_sid and self.auth_token)

    def send_activation_code(self, to_phone: str, code: str) -> bool:
        """Envia o código de ativação de 4 dígitos via WhatsApp.

        Quando `TWILIO_SEND_CODE_WITH_BODY` estiver ativado, envia o
        código como texto simples no campo `Body`. Caso contrário,
        utiliza o template (ContentSid) com `ContentVariables` no
        formato `{"1": code}`.

        Observações sobre o sandbox da Twilio:
            - O número destinatário precisa enviar `join <codigo>`
              ao número `+1 415 523 8886` antes de receber mensagens.
            - Caso o `ContentSid` não esteja aprovado para a conta,
              prefira o modo `Body` definindo a variável de ambiente
              `TWILIO_SEND_CODE_WITH_BODY=true`.

        :param to_phone: número do celular (ex.: `+5511959913833` ou
            `whatsapp:+5511959913833`).
        :param code: código de 4 dígitos.
        :return: True quando o envio foi aceito pela Twilio; False em
            caso de erro ou quando o cliente não está configurado.
        """
        if not self._is_configured():
            msg = "Twilio não configurado (TWILIO_ACCOUNT_SID/AUTH_TOKEN). Código não enviado."
            logger.warning(msg)
            print(f"[WhatsApp] {msg}")
            return False

        to_phone = self._ensure_whatsapp_prefix(to_phone)
        if not self.from_whatsapp.startswith("whatsapp:"):
            self.from_whatsapp = f"whatsapp:{self.from_whatsapp}"

        url = TWILIO_MESSAGES_URL.format(account_sid=self.account_sid)
        auth = (self.account_sid, self.auth_token)

        use_plain_body = os.environ.get("TWILIO_SEND_CODE_WITH_BODY", "").lower() in (
            "1",
            "true",
            "yes",
        )
        if use_plain_body:
            payload = {
                "To": to_phone,
                "From": self.from_whatsapp,
                "Body": f"Seu código de ativação: {code}",
            }
        else:
            content_variables = json.dumps({"1": code})
            payload = {
                "To": to_phone,
                "From": self.from_whatsapp,
                "ContentSid": self.content_sid,
                "ContentVariables": content_variables,
            }

        try:
            logger.info(
                "Twilio: enviando código para %s (From=%s, modo=%s)",
                to_phone,
                self.from_whatsapp,
                "Body" if use_plain_body else f"ContentSid={self.content_sid}",
            )
            response = requests.post(
                url,
                data=payload,
                auth=auth,
                timeout=10,
            )
            if response.ok:
                try:
                    data = response.json()
                    sid = data.get("sid")
                    status = data.get("status")
                except Exception:
                    sid, status = None, None
                logger.info(
                    "WhatsApp (Twilio): pedido aceito. sid=%s status=%s to=%s",
                    sid,
                    status,
                    to_phone,
                )
                print(
                    f"[WhatsApp] Twilio aceitou o envio. SID={sid} status={status}. "
                    "Se não chegou: confira Monitor > Logs > Messaging no console Twilio "
                    "e, no sandbox, se o número já enviou join <palavra> ao +14155238886."
                )
                return True
            try:
                err_json = response.json()
                err_msg = err_json.get("message") or err_json.get("error_message") or response.text
            except Exception:
                err_msg = response.text
            logger.error(
                "Twilio erro %s: %s | Resposta: %s",
                response.status_code,
                err_msg,
                response.text[:500],
            )
            print(f"[WhatsApp] Erro Twilio {response.status_code}: {err_msg}")
            return False
        except requests.RequestException as e:
            logger.exception("Falha ao enviar WhatsApp via Twilio: %s", e)
            return False

    def send_template(self, to_phone: str, content_sid: str, content_variables: dict) -> bool:
        """Envia uma mensagem usando um template Twilio com variáveis.

        :param to_phone: número no formato `whatsapp:+55...`.
        :param content_sid: SID do template aprovado na Twilio.
        :param content_variables: dicionário com as variáveis do
            template, por exemplo `{"1": "valor1", "2": "valor2"}`.
        :return: True quando o envio foi aceito; False em caso de erro.
        """
        if not self._is_configured():
            logger.warning("Twilio não configurado. Mensagem não enviada.")
            return False

        to_phone = self._ensure_whatsapp_prefix(to_phone)
        if not self.from_whatsapp.startswith("whatsapp:"):
            self.from_whatsapp = f"whatsapp:{self.from_whatsapp}"

        url = TWILIO_MESSAGES_URL.format(account_sid=self.account_sid)
        payload = {
            "To": to_phone,
            "From": self.from_whatsapp,
            "ContentSid": content_sid,
            "ContentVariables": json.dumps(content_variables),
        }
        auth = (self.account_sid, self.auth_token)

        try:
            response = requests.post(url, data=payload, auth=auth, timeout=10)
            if response.ok:
                return True
            logger.error("Twilio erro %s: %s", response.status_code, response.text)
            return False
        except requests.RequestException as e:
            logger.exception("Falha ao enviar WhatsApp: %s", e)
            return False
