"""empty message

Revision ID: f3ee659905ce
Revises: 8cd654a16996
Create Date: 2022-10-28 10:49:50.276882

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f3ee659905ce'
down_revision = '8cd654a16996'
branch_labels = None
depends_on = None


def upgrade():
    op.create_unique_constraint("unique_email", "users", ["email"])
    pass


def downgrade():
    op.drop_constraint("unique_email", "users")
    pass
