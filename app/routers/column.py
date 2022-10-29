from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import Optional, List

from .. import models, schemas
from ..database import get_db
from sqlalchemy import func

router = APIRouter(
    prefix="/columns",
    tags=['Columns']
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.ColumnOut)
def create_column(column: schemas.ColumnCreate, db: Session = Depends(get_db), user_id: int = 5):
    
    
    project = db.query(models.Project).filter(models.Project.id == column.project_id).first()
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Project with id: {column.project_id} does not exist")
    
    user_team_query = db.query(models.UserTeam).filter(models.UserTeam.user_id==user_id, models.UserTeam.team_id==project.team_id)

    if not user_team_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"user with id: {user_id} is not a member of team with id: {project.team_id} ")

    new_column = models.TicketColumn(**column.dict())
    db.add(new_column)
    db.commit()
    db.refresh(new_column)

    return new_column

@router.get("/", response_model=List[schemas.ColumnOut])
def get_columns(db: Session = Depends(get_db), limit: int = 10, skip: int = 0, search: Optional[str] = ""):

    columns = db.query(models.TicketColumn).limit(limit).offset(skip).all()
    
    return columns


@router.get('/{id}', response_model=schemas.ColumnOut)
def get_column(id: int, db: Session = Depends(get_db)):

    column = db.query(models.TicketColumn).filter(models.TicketColumn.id == id).first()

    if not column:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'column with id: {id} was not found')

    return column

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_column(id: int, db: Session = Depends(get_db)):

    column_query = db.query(models.TicketColumn).filter(models.TicketColumn.id == id)

    if not column_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'column with id: {id} does not exist')

    #TO DO: check if the user is part of the project to which this column belongs

    column_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
    

@router.put('/{id}', response_model=schemas.ColumnOut)
def update_column(id: int, updated_column: schemas.ColumnCreate, db: Session = Depends(get_db)):
    
    column_query = db.query(models.TicketColumn).filter(models.TicketColumn.id == id)
    column = column_query.first()

    if not column:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'column with id: {id} does not exist')

    column_query.update(updated_column.dict(), synchronize_session=False)
    db.commit()

    return column_query.first()