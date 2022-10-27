from sqlalchemy import Column, Integer, ForeignKey

from ..database import Base

class Column(Base):
    __tablename__ = "user_team"

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    team_id = Column(Integer, ForeignKey("teams.id", ondelete="CASCADE"), nullable=False)