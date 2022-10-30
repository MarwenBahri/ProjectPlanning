from typing import List
from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(
    prefix="/teams",
    tags=["Team"]
)


@router.get("/",  response_model=List[schemas.TeamOut])
def get_teams(
        db: Session = Depends(get_db),
        current_user: int = Depends(oauth2.get_current_user)):

    user_id = current_user.id
    teams = db.query(models.Team
                     ).join(models.UserTeam, models.Team.id == models.UserTeam.team_id
                            ).filter(models.UserTeam.user_id == user_id,
                                     ).all()
    return teams


@router.get("/{team_id}/",  response_model=schemas.TeamOut)
def get_team(
        team_id: int,
        db: Session = Depends(get_db),
        current_user: int = Depends(oauth2.get_current_user)):

    user_id = current_user.id
    team = db.query(models.Team
                    ).join(models.UserTeam, models.Team.id == models.UserTeam.team_id
                           ).filter(models.UserTeam.user_id == user_id,
                                    models.UserTeam.team_id == team_id,
                                    ).first()
    if(not team):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Team with id {team_id} not found")
    return team


@router.post("/",  status_code=status.HTTP_201_CREATED, response_model=schemas.TeamOut)
def create_team(
        team: schemas.TeamBase,
        db: Session = Depends(get_db),
        current_user: int = Depends(oauth2.get_current_user)):

    user_id = current_user.id
    new_team = models.Team(**team.dict(), owner_id=user_id)
    db.add(new_team)
    db.commit()
    db.refresh(new_team)
    user_team = models.UserTeam(user_id=user_id, team_id=new_team.id)
    db.add(user_team)
    db.commit()
    return new_team


@router.delete("/{team_id}/",  status_code=status.HTTP_204_NO_CONTENT)
def delete_team(
        team_id: int,
        db: Session = Depends(get_db),
        current_user: int = Depends(oauth2.get_current_user)):

    user_id = current_user.id
    team_query = db.query(models.Team
                          ).join(models.UserTeam, models.Team.id == models.UserTeam.team_id
                                 ).filter(models.UserTeam.user_id == user_id,
                                          models.UserTeam.team_id == team_id,
                                          models.Team.owner_id == user_id)
    if(not team_query.first()):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not authorized to perform requested action")
    team_query = db.query(models.Team).filter(
        models.Team.id == team_id)
    team_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{team_id}/",  response_model=schemas.TeamOut)
def update_team(
        team: schemas.TeamBase,
        team_id: int,
        db: Session = Depends(get_db),
        current_user: int = Depends(oauth2.get_current_user)):

    user_id = current_user.id
    team_query = db.query(models.Team
                          ).join(models.UserTeam, models.Team.id == models.UserTeam.team_id
                                 ).filter(models.UserTeam.user_id == user_id,
                                          models.UserTeam.team_id == team_id,
                                          models.Team.owner_id == user_id)
    if(not team_query.first()):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Team with {team_id} does not exits")
    team_query = db.query(models.Team).filter(
        models.Team.id == team_id)
    team_query.update(team.dict(), synchronize_session=False)
    db.commit()
    return team_query.first()
