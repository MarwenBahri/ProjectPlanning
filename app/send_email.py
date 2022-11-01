from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from .config import settings
from jinja2 import Environment, select_autoescape, PackageLoader

conf = ConnectionConfig(
    MAIL_USERNAME=settings.mail_username,
    MAIL_PASSWORD=settings.mail_password,
    MAIL_FROM=settings.mail_from,
    MAIL_PORT=settings.mail_port,
    MAIL_SERVER=settings.mail_server,
    MAIL_FROM_NAME=settings.mail_from_name,
    MAIL_TLS=True,
    MAIL_SSL=False,
    USE_CREDENTIALS=True
)

env = Environment(
    loader=PackageLoader('app', 'templates/email'),
    autoescape=select_autoescape(['html', 'xml'])
)

async def send_email_async(subject: str, email_to: str,body:dict, template:str):
    
    template = env.get_template(f'{template}.html')

    html = template.render(
           **body
        )
    message = MessageSchema(
        subject=subject,
        recipients=[email_to],
        html=html,
        subtype='html',
    )


    fm = FastMail(conf)

    await fm.send_message(message)
