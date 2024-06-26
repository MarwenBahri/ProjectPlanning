"""empty message

Revision ID: 2675fa78ef5d
Revises: cb79afe173fe
Create Date: 2022-11-01 19:14:48.564698

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2675fa78ef5d'
down_revision = 'cb79afe173fe'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('confirmed', sa.Boolean(), server_default='false', nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'confirmed')
    # ### end Alembic commands ###
