"""Add user settings

Revision ID: 0ed199f5f198
Revises: 75a3481c4d0c
Create Date: 2018-05-05 18:49:25.735600

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0ed199f5f198'
down_revision = '75a3481c4d0c'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('UserSettings',
                    sa.Column('_created', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
                    sa.Column('_modified', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('user_id', sa.Integer(), nullable=False),
                    sa.Column('skip_tutorial', sa.Boolean(), nullable=False),
                    sa.ForeignKeyConstraint(['user_id'], ['Users.id'], name=op.f('fk_UserSettings_user_id_Users')),
                    sa.PrimaryKeyConstraint('id', name=op.f('pk_UserSettings'))
                    )


def downgrade():
    op.drop_table('UserSettings')
