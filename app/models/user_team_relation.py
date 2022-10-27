from sqlalchemy import Column, Integer, ForeignKey

from ..database import Base

class UserTeam(Base):
    __tablename__ = "user_team"

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"),primary_key=True, nullable=False)
    team_id = Column(Integer, ForeignKey("teams.id", ondelete="CASCADE"), primary_key=True,nullable=False)