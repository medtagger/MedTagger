"""Add owners to labels and scans

Revision ID: ab732474a829
Revises: 4e93b463a357
Create Date: 2018-03-05 22:59:20.353295

"""
from alembic import op
import sqlalchemy as sa


revision = 'ab732474a829'
down_revision = '4e93b463a357'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('Labels', sa.Column('owner_id', sa.Integer(), nullable=True))
    op.create_foreign_key(op.f('fk_Labels_owner_id_Users'), 'Labels', 'Users', ['owner_id'], ['id'])
    op.create_unique_constraint(op.f('uq_Roles_name'), 'Roles', ['name'])
    op.drop_constraint('Roles_name_key', 'Roles', type_='unique')
    op.create_unique_constraint(op.f('uq_ScanCategories_key'), 'ScanCategories', ['key'])
    op.drop_constraint('ScanCategories_key_key', 'ScanCategories', type_='unique')
    op.add_column('Scans', sa.Column('owner_id', sa.Integer(), nullable=True))
    op.create_foreign_key(op.f('fk_Scans_owner_id_Users'), 'Scans', 'Users', ['owner_id'], ['id'])
    op.create_unique_constraint(op.f('uq_Users_email'), 'Users', ['email'])
    op.drop_constraint('Users_email_key', 'Users', type_='unique')


def downgrade():
    op.create_unique_constraint('Users_email_key', 'Users', ['email'])
    op.drop_constraint(op.f('uq_Users_email'), 'Users', type_='unique')
    op.drop_constraint(op.f('fk_Scans_owner_id_Users'), 'Scans', type_='foreignkey')
    op.drop_column('Scans', 'owner_id')
    op.create_unique_constraint('ScanCategories_key_key', 'ScanCategories', ['key'])
    op.drop_constraint(op.f('uq_ScanCategories_key'), 'ScanCategories', type_='unique')
    op.create_unique_constraint('Roles_name_key', 'Roles', ['name'])
    op.drop_constraint(op.f('uq_Roles_name'), 'Roles', type_='unique')
    op.drop_constraint(op.f('fk_Labels_owner_id_Users'), 'Labels', type_='foreignkey')
    op.drop_column('Labels', 'owner_id')

