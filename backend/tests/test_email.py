from unittest.mock import patch, MagicMock
from send_email import enviar_email


@patch("send_email.smtplib.SMTP_SSL")
def test_envio_email(mock_smtp):
    smtp = MagicMock()
    mock_smtp.return_value.__enter__.return_value = smtp

    enviar_email()

    smtp.send_message.assert_called_once()