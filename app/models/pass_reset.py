from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP

from ..database import Base


class PasswordReset(Base):
    __tablename__ = "pass_reset"

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"),primary_key=True,  nullable=False)
    code = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
