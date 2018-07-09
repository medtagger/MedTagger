"""Add comment column to label model

Revision ID: 85bad1834e93
Revises: 01dc85c25335
Create Date: 2018-07-09 09:02:37.404910

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '85bad1834e93'
down_revision = '01dc85c25335'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Labels', sa.Column('comment', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Labels', 'comment')
    # ### end Alembic commands ###
