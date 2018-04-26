"""Added LabelTags

Revision ID: 0c1023f8d037
Revises: ab732474a829
Create Date: 2018-04-26 19:04:26.641687

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from sqlalchemy.dialects.postgresql import ENUM

revision = '0c1023f8d037'
down_revision = 'ab732474a829'
branch_labels = None
depends_on = None

label_status_enum = ENUM('VALID', 'INVALID', 'NOT_VERIFIED', name='label_status_enum', create_type=False)


def upgrade():
    label_status_enum.create(op.get_bind(), checkfirst=True)
    op.create_table('LabelTags',
                    sa.Column('id', sa.String(), nullable=False),
                    sa.Column('key', sa.String(length=50), nullable=False),
                    sa.Column('name', sa.String(length=100), nullable=False),
                    sa.Column('scan_category_id', sa.Integer(), nullable=True),
                    sa.ForeignKeyConstraint(['scan_category_id'], ['ScanCategories.id'],
                                            name=op.f('fk_LabelTags_scan_category_id_ScanCategories')),
                    sa.PrimaryKeyConstraint('id', name=op.f('pk_LabelTags')),
                    sa.UniqueConstraint('key', name=op.f('uq_LabelTags_key'))
                    )
    op.create_table('LabelElements',
                    sa.Column('id', sa.String(), nullable=False),
                    sa.Column('position_x', sa.Float(), nullable=False),
                    sa.Column('position_y', sa.Float(), nullable=False),
                    sa.Column('slice_index', sa.Integer(), nullable=False),
                    sa.Column('shape_width', sa.Float(), nullable=False),
                    sa.Column('shape_height', sa.Float(), nullable=False),
                    sa.Column('has_binary_mask', sa.Boolean(), nullable=False),
                    sa.Column('label_id', sa.String(), nullable=True),
                    sa.Column('tag_id', sa.String(), nullable=True),
                    sa.Column('status', label_status_enum,
                              server_default='NOT_VERIFIED', nullable=False),
                    sa.ForeignKeyConstraint(['label_id'], ['Labels.id'], name=op.f('fk_LabelElements_label_id_Labels')),
                    sa.ForeignKeyConstraint(['tag_id'], ['LabelTags.id'],
                                            name=op.f('fk_LabelElements_tag_id_LabelTags')),
                    sa.PrimaryKeyConstraint('id', name=op.f('pk_LabelElements'))
                    )
    op.drop_table('LabelSelections')
    op.drop_column('Labels', 'status')


def downgrade():
    op.add_column('Labels',
                  sa.Column('status', postgresql.ENUM('VALID', 'INVALID', 'NOT_VERIFIED', name='label_status_enum'),
                            server_default=sa.text("'NOT_VERIFIED'::label_status_enum"), autoincrement=False,
                            nullable=False))
    op.create_table('LabelSelections',
                    sa.Column('id', sa.VARCHAR(), autoincrement=False, nullable=False),
                    sa.Column('position_x', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False,
                              nullable=False),
                    sa.Column('position_y', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False,
                              nullable=False),
                    sa.Column('slice_index', sa.INTEGER(), autoincrement=False, nullable=False),
                    sa.Column('shape_width', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False,
                              nullable=False),
                    sa.Column('shape_height', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False,
                              nullable=False),
                    sa.Column('has_binary_mask', sa.BOOLEAN(), autoincrement=False, nullable=False),
                    sa.Column('label_id', sa.VARCHAR(), autoincrement=False, nullable=True),
                    sa.ForeignKeyConstraint(['label_id'], ['Labels.id'], name='fk_LabelSelections_label_id_Labels'),
                    sa.PrimaryKeyConstraint('id', name='pk_LabelSelections')
                    )
    op.drop_table('LabelElements')
    op.drop_table('LabelTags')
