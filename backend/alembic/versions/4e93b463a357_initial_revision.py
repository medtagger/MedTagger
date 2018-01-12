"""Initial revision

Revision ID: 4e93b463a357
Revises: 
Create Date: 2018-01-12 19:58:16.619287

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import ENUM


# revision identifiers, used by Alembic.
revision = '4e93b463a357'
down_revision = None
branch_labels = None
depends_on = None

label_status_enum = ENUM('VALID', 'INVALID', 'NOT_VERIFIED', name='label_status_enum', create_type=False)
slices_orientation_enum = ENUM('X', 'Y', 'Z', name='sliceorientation', create_type=False)


def upgrade():
    # At first, create all enums
    label_status_enum.create(op.get_bind(), checkfirst=True)
    slices_orientation_enum.create(op.get_bind(), checkfirst=True)

    # Now, we are ready to create all tables
    op.create_table('Roles',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('name', sa.String(length=50), nullable=True),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('name'),
                    )
    op.create_table('ScanCategories',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('key', sa.String(length=50), nullable=False),
                    sa.Column('name', sa.String(length=100), nullable=False),
                    sa.Column('image_path', sa.String(length=100), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('key'),
                    )
    op.create_table('Users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('email', sa.String(length=50), nullable=False),
                    sa.Column('password', sa.String(length=255), nullable=False),
                    sa.Column('first_name', sa.String(length=50), nullable=False),
                    sa.Column('last_name', sa.String(length=50), nullable=False),
                    sa.Column('active', sa.Boolean(), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email'),
                    )
    op.create_table('Scans',
                    sa.Column('id', sa.String(), nullable=False),
                    sa.Column('converted', sa.Boolean(), nullable=True),
                    sa.Column('number_of_slices', sa.Integer(), nullable=False),
                    sa.Column('category_id', sa.Integer(), nullable=True),
                    sa.ForeignKeyConstraint(['category_id'], ['ScanCategories.id'], ),
                    sa.PrimaryKeyConstraint('id'),
                    )
    op.create_table('Users_Roles',
                    sa.Column('user_id', sa.Integer(), nullable=True),
                    sa.Column('role_id', sa.Integer(), nullable=True),
                    sa.ForeignKeyConstraint(['role_id'], ['Roles.id'], ),
                    sa.ForeignKeyConstraint(['user_id'], ['Users.id'], ),
                    )
    op.create_table('Labels',
                    sa.Column('id', sa.String(), nullable=False),
                    sa.Column('scan_id', sa.String(), nullable=True),
                    sa.Column('status', label_status_enum, server_default='NOT_VERIFIED', nullable=False),
                    sa.ForeignKeyConstraint(['scan_id'], ['Scans.id'], ),
                    sa.PrimaryKeyConstraint('id'),
                    )
    op.create_table('Slices',
                    sa.Column('id', sa.String(), nullable=False),
                    sa.Column('orientation', slices_orientation_enum, nullable=False),
                    sa.Column('location', sa.Float(), nullable=True),
                    sa.Column('position_x', sa.Float(), nullable=True),
                    sa.Column('position_y', sa.Float(), nullable=True),
                    sa.Column('position_z', sa.Float(), nullable=True),
                    sa.Column('stored', sa.Boolean(), nullable=True),
                    sa.Column('converted', sa.Boolean(), nullable=True),
                    sa.Column('scan_id', sa.String(), nullable=True),
                    sa.ForeignKeyConstraint(['scan_id'], ['Scans.id'], ),
                    sa.PrimaryKeyConstraint('id'),
                    )
    op.create_table('LabelSelections',
                    sa.Column('id', sa.String(), nullable=False),
                    sa.Column('position_x', sa.Float(), nullable=False),
                    sa.Column('position_y', sa.Float(), nullable=False),
                    sa.Column('slice_index', sa.Integer(), nullable=False),
                    sa.Column('shape_width', sa.Float(), nullable=False),
                    sa.Column('shape_height', sa.Float(), nullable=False),
                    sa.Column('has_binary_mask', sa.Boolean(), nullable=False),
                    sa.Column('label_id', sa.String(), nullable=True),
                    sa.ForeignKeyConstraint(['label_id'], ['Labels.id'], ),
                    sa.PrimaryKeyConstraint('id'),
                    )


def downgrade():
    op.drop_table('LabelSelections')
    op.drop_table('Slices')
    op.drop_table('Labels')
    op.drop_table('Users_Roles')
    op.drop_table('Scans')
    op.drop_table('Users')
    op.drop_table('ScanCategories')
    op.drop_table('Roles')

    label_status_enum.drop(op.get_bind(), checkfirst=True)
    slices_orientation_enum.drop(op.get_bind(), checkfirst=True)
