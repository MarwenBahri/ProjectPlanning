from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(
    prefix="/tickets",
    tags=["ticket"]
)


@router.get("/{ticket_id}",  response_model=schemas.TicketOut)
def get_ticket(
        ticket_id: int,
        db: Session = Depends(get_db),
        current_user: int = Depends(oauth2.get_current_user)):

    user_id = current_user.id
    ticket = db.query(models.Ticket
                      ).join(models.TicketColumn, models.Ticket.column_id == models.TicketColumn.id
                             ).join(models.Project, models.Project.id == models.TicketColumn.project_id
                                    ).join(models.Team, models.Team.id == models.Project.team_id
                                           ).join(models.UserTeam, models.Team.id == models.UserTeam.team_id
                                                  ).filter(models.UserTeam.user_id == user_id,
                                                           models.Ticket.id == ticket_id).first()
    if(not ticket):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Ticket with id {ticket_id} not found")
    return ticket


@router.post("/",  status_code=status.HTTP_201_CREATED, response_model=schemas.TicketOut)
def create_ticket(
        ticket: schemas.TicketBase,
        db: Session = Depends(get_db),
        current_user: int = Depends(oauth2.get_current_user)):

    user_id = current_user.id
    new_ticket = models.Ticket(**ticket.dict())
    col = db.query(models.TicketColumn
                   ).join(models.Project, models.Project.id == models.TicketColumn.project_id
                          ).join(models.Team, models.Team.id == models.Project.team_id
                                 ).join(models.UserTeam, models.Team.id == models.UserTeam.team_id
                                        ).filter(models.UserTeam.user_id == user_id,
                                                 models.TicketColumn.id == new_ticket.column_id,
                                                 ).first()
    if(not col):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not authorized to perform requested action")
    db.add(new_ticket)
    db.commit()
    db.refresh(new_ticket)
    return new_ticket


@router.delete("/{ticket_id}",  status_code=status.HTTP_204_NO_CONTENT)
def delete_ticket(
        ticket_id: int,
        db: Session = Depends(get_db),
        current_user: int = Depends(oauth2.get_current_user)):

    user_id = current_user.id
    ticket_query = db.query(models.Ticket
                            ).join(models.TicketColumn, models.Ticket.column_id == models.TicketColumn.id
                                   ).join(models.Project, models.Project.id == models.TicketColumn.project_id
                                          ).join(models.Team, models.Team.id == models.Project.team_id
                                                 ).join(models.UserTeam, models.Team.id == models.UserTeam.team_id
                                                        ).filter(models.UserTeam.user_id == user_id,
                                                                 models.Ticket.id == ticket_id)
    ticket = ticket_query.first()
    if(not ticket):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not authorized to perform requested action")
    ticket_query = db.query(models.Ticket).filter(
        models.Ticket.id == ticket_id)
    ticket_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{ticket_id}",  response_model=schemas.TicketOut)
def update_ticket(
        ticket: schemas.TicketBase,
        ticket_id: int,
        db: Session = Depends(get_db),
        current_user: int = Depends(oauth2.get_current_user)):

    user_id = current_user.id
    ticket_query = db.query(models.Ticket
                            ).join(models.TicketColumn, models.Ticket.column_id == models.TicketColumn.id
                                   ).join(models.Project, models.Project.id == models.TicketColumn.project_id
                                          ).join(models.Team, models.Team.id == models.Project.team_id
                                                 ).join(models.UserTeam, models.Team.id == models.UserTeam.team_id
                                                        ).filter(models.UserTeam.user_id == user_id,
                                                                 models.Ticket.id == ticket_id)
    if(not ticket_query.first()):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Ticket with {ticket_id} does not exits")
    ticket_query = db.query(models.Ticket).filter(
        models.Ticket.id == ticket_id)
    ticket_query.update(ticket.dict(), synchronize_session=False)
    db.commit()
    return ticket_query.first()
