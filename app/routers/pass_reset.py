from datetime import datetime

from fastapi import APIRouter,HTTPException, status, Depends, BackgroundTasks
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from pydantic import EmailStr, BaseModel
from sqlalchemy.orm import Session
from string import ascii_letters, digits
from random import choice 

from jinja2 import Environment, select_autoescape, PackageLoader

from ..database import get_db
from .. import models, utils, schemas
from ..config import settings

class EmailSchema(BaseModel):
    email: EmailStr


conf = ConnectionConfig(
    MAIL_USERNAME = settings.mail_username,
    MAIL_PASSWORD = settings.mail_password,
    MAIL_FROM = settings.mail_from,
    MAIL_PORT = settings.mail_port,
    MAIL_SERVER = settings.mail_server,
    MAIL_FROM_NAME= settings.mail_from_name,
    MAIL_STARTTLS = True,
    MAIL_SSL_TLS = False,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True
)

router = APIRouter(
    prefix="/password",
    tags=['Password']
)

RESET_PASS_EXPIRATION_TIME = 5*60 # in seconds

env = Environment(
    loader=PackageLoader('app', 'templates/email'),
    autoescape=select_autoescape(['html', 'xml'])
)

@router.post("/", status_code=status.HTTP_200_OK)
def send_email_background(email: EmailSchema, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    
    user = db.query(models.User).filter(models.User.email==email.email).first()
    if not user:
        return {"answer": "If the email belongs to a user, a confirmation code would have been sent"}

    pass_reset = db.query(models.PasswordReset).filter(models.PasswordReset.user_id==user.id).first()
    if pass_reset:
        return {"answer": "If the email belongs to a user, a confirmation code would have been sent"}

    code = ''.join(choice(ascii_letters+digits) for i in range(8))
    
    template = env.get_template('pass_reset.html')

    html = template.render(
           **{"name": user.name,"code":code}
        )

    message = MessageSchema(
        subject="Project Planning Password Reset",
        recipients=[email.email],
        body=html,
        subtype=MessageType.html)

    fm = FastMail(conf)
    background_tasks.add_task(fm.send_message, message)

    #fm.send_message(message)
    new_pass_reset_entry = {"user_id": user.id, "code": code}
    new_pass_reset = models.PasswordReset(**new_pass_reset_entry)
    db.add(new_pass_reset)
    db.commit()

    return {"answer": "If the email belongs to a user, a confirmation code would have been sent"}


@router.post("/confirm", status_code=status.HTTP_200_OK)
def cofirm_reset_code(new_pass: schemas.PassReset, db: Session = Depends(get_db)):
    
    pass_reset_query = db.query(models.PasswordReset).filter(models.PasswordReset.code==new_pass.code)
    pass_reset = pass_reset_query.first()

    if not pass_reset:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Wrong confirmation code')
    

    passed_time = datetime.now() - pass_reset.created_at.replace(tzinfo=None)
    expired = passed_time.total_seconds() > RESET_PASS_EXPIRATION_TIME

    user_id = pass_reset.user_id
    
    if expired:
        pass_reset_query.delete(synchronize_session=False)
        db.commit()
        raise HTTPException(status_code=status.HTTP_408_REQUEST_TIMEOUT, detail='Confirmation code expired')

    user_query = db.query(models.User).filter(models.User.id == user_id)
    if not user_query.first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Conflict')

    user_query.update({"password":utils.hash(new_pass.password)}, synchronize_session=False)
    pass_reset_query.delete(synchronize_session=False)
    db.commit()

    return {"response":"password reset successfully"}
