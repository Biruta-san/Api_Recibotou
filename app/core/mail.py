import aiosmtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.core.config import settings
from app.core.logger_config import logger
from datetime import datetime
from app.utils.utility import format_datetime

async def send_password_recovery_email(to_email: str, token: str, expire: datetime):
  try:
    smtp_server = settings.SMTP_SERVER
    smtp_port = settings.SMTP_PORT
    smtp_user = settings.SMTP_USERNAME
    smtp_password = settings.SMTP_PASSWORD
    sender_email = settings.SMTP_FROM or smtp_user

    subject = "Recuperação de Senha"
    body = f"""\
    <html lang="pt-BR">
    <head>
      <meta charset="UTF-8" />
      <title>Código de Verificação</title>
      <style>
        body {{
          font-family: Arial, sans-serif;
          background-color: #f4f4f7;
          padding: 20px;
          color: #333;
        }}
        .container {{
          max-width: 500px;
          margin: 0 auto;
          background-color: #ffffff;
          border-radius: 8px;
          padding: 30px;
          box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
        }}
        .code {{
          font-size: 32px;
          font-weight: bold;
          letter-spacing: 6px;
          background-color: #f0f0f0;
          padding: 15px;
          border-radius: 6px;
          text-align: center;
          margin: 20px 0;
          color: #009929;
        }}
        .footer {{
          font-size: 12px;
          color: #888;
          text-align: center;
          margin-top: 20px;
        }}
      </style>
    </head>
    <body>
      <div class="container">
        <h2>Recuperação de senha Recibotou</h2>
        <p>Olá,</p>
        <p>Use o código abaixo para acessar sua conta com segurança:</p>

        <div class="code">{token}</div>

        <p>Este código expira em <strong>{format_datetime(expire)}</strong>. Se você não solicitou este código, ignore este e-mail.</p>

        <div class="footer">
          © 2025 Recibotou. Todos os direitos reservados.
        </div>
      </div>
    </body>
    </html>"""


    msg = MIMEMultipart("alternative")
    msg["From"] = sender_email
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "html"))

    if not smtp_server or not smtp_port or not smtp_user:
      raise Exception("Configurações SMTP não estão definidas.")

    await aiosmtplib.send(
      msg,
      hostname=smtp_server,
      port=smtp_port,
      username=smtp_user,
      password=smtp_password,
      use_tls=True,
    )

    logger.info(f"E-mail de recuperação enviado para {to_email}")
  except Exception as e:
    logger.exception(f"Erro ao enviar e-mail para {to_email}: {e}")

async def send_two_factor_code(to_email: str, token: str, expire: datetime):
  try:
    smtp_server = settings.SMTP_SERVER
    smtp_port = settings.SMTP_PORT
    smtp_user = settings.SMTP_USERNAME
    smtp_password = settings.SMTP_PASSWORD
    sender_email = settings.SMTP_FROM or smtp_user

    subject = "Autenticação de Dois Fatores"
    body = f"""\
    <html lang="pt-BR">
    <head>
      <meta charset="UTF-8" />
      <title>Código de Autenticação</title>
      <style>
        body {{
          font-family: Arial, sans-serif;
          background-color: #f4f4f7;
          padding: 20px;
          color: #333;
        }}
        .container {{
          max-width: 500px;
          margin: 0 auto;
          background-color: #ffffff;
          border-radius: 8px;
          padding: 30px;
          box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
        }}
        .code {{
          font-size: 32px;
          font-weight: bold;
          letter-spacing: 6px;
          background-color: #f0f0f0;
          padding: 15px;
          border-radius: 6px;
          text-align: center;
          margin: 20px 0;
          color: #009929;
        }}
        .footer {{
          font-size: 12px;
          color: #888;
          text-align: center;
          margin-top: 20px;
        }}
      </style>
    </head>
    <body>
      <div class="container">
        <h2>Autenticação de Dois Fatores Recibotou</h2>
        <p>Olá,</p>
        <p>Use o código abaixo para acessar sua conta com segurança:</p>

        <div class="code">{token}</div>

        <p>Este código expira em <strong>{format_datetime(expire)}</strong>. Se você não solicitou este código, ignore este e-mail.</p>

        <div class="footer">
          © 2025 Recibotou. Todos os direitos reservados.
        </div>
      </div>
    </body>
    </html>"""


    msg = MIMEMultipart("alternative")
    msg["From"] = sender_email
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "html"))

    if not smtp_server or not smtp_port or not smtp_user:
      raise Exception("Configurações SMTP não estão definidas.")

    await aiosmtplib.send(
      msg,
      hostname=smtp_server,
      port=smtp_port,
      username=smtp_user,
      password=smtp_password,
      use_tls=True,
    )

    logger.info(f"E-mail de autenticação enviado para {to_email}")
  except Exception as e:
    logger.exception(f"Erro ao enviar e-mail para {to_email}: {e}")
