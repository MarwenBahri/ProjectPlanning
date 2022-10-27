from sqlalchemy import TIMESTAMP, Column, ForeignKey, Integer, String
from sqlalchemy.sql.expression import text

from ..database import Base

class Project(Base):
    __tablename__ = "projects"
    
    id =  Column(Integer, primary_key = True, nullable=False)
    name = Column(String , nullable=False)
    description = Column(String, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    team_id = Column(Integer, ForeignKey("teams.id", ondelete="CASCADE"), nullable=False)
    

