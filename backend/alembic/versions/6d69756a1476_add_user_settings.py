"""Add user settings

Revision ID: 6d69756a1476
Revises: 729cd1e8cde1
Create Date: 2018-05-10 16:12:06.872006

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6d69756a1476'
down_revision = '729cd1e8cde1'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('UserSettings',
                    sa.Column('_created', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
                    sa.Column('_modified', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('skip_tutorial', sa.Boolean(), nullable=False),
                    sa.ForeignKeyConstraint(['id'], ['Users.id'], name=op.f('fk_UserSettings_id_Users')),
                    sa.PrimaryKeyConstraint('id', name=op.f('pk_UserSettings'))
                    )


def downgrade():
    op.drop_table('UserSettings')
