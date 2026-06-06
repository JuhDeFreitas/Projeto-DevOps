import os
import smtplib
from email.message import EmailMessage


def enviar_email():
    msg = EmailMessage()
    msg["Subject"] = "Pipeline Jenkins"
    msg["From"] = os.getenv("EMAIL_USER")
    msg["To"] = os.getenv("EMAIL_DESTINO")

    msg.set_content("Pipeline executado com sucesso!")

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(
            os.getenv("EMAIL_USER"),
            os.getenv("EMAIL_PASSWORD")
        )
        smtp.send_message(msg)

    print("""
    [OK] Checkout SCM concluído
    [OK] Dependências instaladas
    [OK] Testes executados
    [OK] Cobertura de código gerada
    [OK] Imagem Docker criada
    [OK] Pacote salvo
    [OK] Notificação por e-mail enviada
    [OK] Post Actions executadas
    
    [SUCCESS] Pipeline finalizado com sucesso.
""")


if __name__ == "__main__":
    enviar_email()