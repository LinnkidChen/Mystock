"""empty message

Revision ID: a1ad75d38837
Revises: 181488197283
Create Date: 2022-12-11 16:58:34.286517

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a1ad75d38837'
down_revision = '181488197283'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('feeSummary', sa.Column('count', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('feeSummary', 'count')
    # ### end Alembic commands ###
