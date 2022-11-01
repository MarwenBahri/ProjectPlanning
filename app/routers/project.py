from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(
    prefix="/projects",
    tags=["Project"]
)


@router.get("/{proj_id}/",  response_model=schemas.ProjectOut)
def get_project(
        proj_id: int,
        db: Session = Depends(get_db),
        current_user: int = Depends(oauth2.get_current_user)):

    user_id = current_user.id
    project = db.query(models.Project
                       ).join(models.Team, models.Team.id == models.Project.team_id
                              ).join(models.UserTeam, models.Team.id == models.UserTeam.team_id
                                     ).filter(models.UserTeam.user_id == user_id,
                                              models.Project.id == proj_id,
                                              ).first()
    if(not project):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Project with id {proj_id} not found")
    return project


@router.post("/",  status_code=status.HTTP_201_CREATED, response_model=schemas.ProjectOut)
def create_project(
        project: schemas.ProjectBase,
        db: Session = Depends(get_db),
        current_user: int = Depends(oauth2.get_current_user)):

    user_id = current_user.id
    new_project = models.Project(**project.dict())
    res = db.query(models.Team
                   ).join(models.UserTeam, models.Team.id == models.UserTeam.team_id
                          ).filter(models.UserTeam.user_id == user_id,
                                   models.Team.id == new_project.team_id
                                   ).first()
    if(not res):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not authorized to perform requested action")
    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    return new_project


@router.delete("/{proj_id}/",  status_code=status.HTTP_204_NO_CONTENT)
def delete_project(
        proj_id: int,
        db: Session = Depends(get_db),
        current_user: int = Depends(oauth2.get_current_user)):

    user_id = current_user.id
    project_query = db.query(models.Project
                             ).join(models.Team, models.Team.id == models.Project.team_id
                                    ).join(models.UserTeam, models.Team.id == models.UserTeam.team_id
                                           ).filter(models.UserTeam.user_id == user_id,
                                                    models.Project.id == proj_id)
    if(not project_query.first()):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not authorized to perform requested action")
    project_query = db.query(models.Project).filter(
        models.Project.id == proj_id)
    project_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{proj_id}/",  response_model=schemas.ProjectOut)
def update_project(
        project: schemas.ProjectBase,
        proj_id: int,
        db: Session = Depends(get_db),
        current_user: int = Depends(oauth2.get_current_user)):

    user_id = current_user.id
    project_query = db.query(models.Project
                             ).join(models.Team, models.Team.id == models.Project.team_id
                                    ).join(models.UserTeam, models.Team.id == models.UserTeam.team_id
                                           ).filter(models.UserTeam.user_id == user_id,
                                                    models.Project.id == proj_id)
    if(not project_query.first()):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Project with {proj_id} does not exits")
    project_query = db.query(models.Project).filter(
        models.Project.id == proj_id)
    project_query.update(project.dict(), synchronize_session=False)
    db.commit()
    return project_query.first()
