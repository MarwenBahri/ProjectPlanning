from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from .. import models
from ..database import get_db

router = APIRouter(
    prefix="/confirm",
    tags=["confirmation"]
)


@router.get('/{code}')
def confirm(code: str, db: Session = Depends(get_db)):
    confirmation_query = db.query(models.EmailConfirmation).filter(
        models.EmailConfirmation.code == code)
    confirmation = confirmation_query.first()
    if not confirmation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Link not found")
    user_id = confirmation.user_id
    user_query = db.query(models.User).filter(models.User.id == user_id)
    user_query.update({"confirmed": True}, synchronize_session=False)
    confirmation_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
