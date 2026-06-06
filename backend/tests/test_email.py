from unittest.mock import patch, MagicMock
import pytest
from send_email import enviar_email


# =========================
# TESTE 1 - ENVIO NORMAL
# =========================
@patch("send_email.os.getenv")
@patch("send_email.smtplib.SMTP_SSL")
def test_envio_email_ok(mock_smtp, mock_getenv):
    mock_getenv.side_effect = lambda key: {
        "EMAIL_USER": "teste@gmail.com",
        "EMAIL_PASSWORD": "123",
        "EMAIL_DESTINO": "destino@gmail.com"
    }.get(key)

    smtp = MagicMock()
    mock_smtp.return_value.__enter__.return_value = smtp

    enviar_email()

    smtp.login.assert_called_once_with("teste@gmail.com", "123")
    smtp.send_message.assert_called_once()


# =========================
# TESTE 2 - FALHA NO LOGIN SMTP
# =========================
@patch("send_email.os.getenv")
@patch("send_email.smtplib.SMTP_SSL")
def test_envio_email_falha_login(mock_smtp, mock_getenv):
    mock_getenv.side_effect = lambda key: {
        "EMAIL_USER": "teste@gmail.com",
        "EMAIL_PASSWORD": "errado",
        "EMAIL_DESTINO": "destino@gmail.com"
    }.get(key)

    smtp = MagicMock()
    smtp.login.side_effect = Exception("Erro no login")

    mock_smtp.return_value.__enter__.return_value = smtp

    with pytest.raises(Exception):
        enviar_email()


# =========================
# TESTE 3 - SMTP QUEBRADO
# =========================
@patch("send_email.os.getenv")
@patch("send_email.smtplib.SMTP_SSL")
def test_envio_email_falha_smtp(mock_smtp, mock_getenv):
    mock_getenv.side_effect = lambda key: {
        "EMAIL_USER": "teste@gmail.com",
        "EMAIL_PASSWORD": "123",
        "EMAIL_DESTINO": "destino@gmail.com"
    }.get(key)

    smtp = MagicMock()
    smtp.send_message.side_effect = Exception("Erro SMTP")

    mock_smtp.return_value.__enter__.return_value = smtp

    with pytest.raises(Exception):
        enviar_email()