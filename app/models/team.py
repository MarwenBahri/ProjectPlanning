from sqlalchemy import TIMESTAMP, Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.sql.expression import text

from ..database import Base

class Team(Base):
    __tablename__ = "teams"
    
    id =  Column(Integer, primary_key = True, nullable=False)
    name = Column(String , nullable=False)
    description = Column(String, nullable=True)
    is_personal = Column(Boolean, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    

