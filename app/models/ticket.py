from sqlalchemy import TIMESTAMP, Column, ForeignKey, Integer, String, Enum
from sqlalchemy.sql.expression import text

from ..schemas import TicketPriority
from ..database import Base

class Ticket(Base):
    __tablename__ = "tickets"
    
    id =  Column(Integer, primary_key = True, nullable=False)
    name = Column(String , nullable=False)
    description = Column(String, nullable=True)
    priority = Column(Enum(TicketPriority),nullable = False)
    deadline = Column(TIMESTAMP(timezone=True), nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    column_id = Column(Integer, ForeignKey("columns.id", ondelete="CASCADE"), nullable=False)
    

