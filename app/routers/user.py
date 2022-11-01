from aiosmtplib import send
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas, utils, oauth2
from ..config import settings
from ..database import get_db
from ..send_email import send_email_async

router = APIRouter(
    prefix="/users",
    tags=['Users']
)

# /users/
# /users


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    # hash the password - user.password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    
    user_query = db.query(models.User).filter(
        models.User.email == user.email)

    if user_query.first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="email already used")

    new_user = models.User(**user.dict())
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    confirmation  = models.EmailConfirmation(user_id=new_user.id , code=utils.generate_random_code())
    db.add(confirmation)
    db.commit()
    await send_email_async(
        subject= "Confirm your Project planning account",
        email_to = new_user.email, 
        body={
            "username" : user.name,
            "confirmation_link": f'{settings.host}confirm/{confirmation.code}'
        }, 
        template="confirmation")
    return new_user


@router.get('/', response_model=List[schemas.UserOut])
def get_users(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    users = db.query(models.User).all()
    return users


@router.get('/{id}', response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id: {id} does not exist")

    return user


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    if id != current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
        detail='Not authorized to perform requested action')

    user_query = db.query(models.User).filter(models.User.id == id)
    user = user_query.first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id: {id} does not exist")

    user_query.delete()
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT) 


@router.put("/{id}", response_model=schemas.UserOut)
def update_user(id: int, updated_user: schemas.UserCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    if id != current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
        detail='Not authorized to perform requested action')
    
    user_query = db.query(models.User).filter(models.User.id == id)

    user = user_query.first()
    updated_user.password = utils.hash(updated_user.password)
    
    if user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"user with id: {id} does not exist")


    user_query.update(updated_user.dict(), synchronize_session=False)

    db.commit()

    return user_query.first()