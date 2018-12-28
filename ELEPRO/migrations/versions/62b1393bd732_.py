"""empty message

Revision ID: 62b1393bd732
Revises: c7c8551fd23a
Create Date: 2018-12-26 12:03:04.520044

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '62b1393bd732'
down_revision = 'c7c8551fd23a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'description')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('description', sa.VARCHAR(length=400), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
