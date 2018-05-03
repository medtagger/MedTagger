"""add_label_tools

Revision ID: 7995a5e4f811
Revises: 61737c4342bc
Create Date: 2018-05-03 22:33:59.012448

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import table, column
from sqlalchemy.dialects import postgresql
from sqlalchemy.dialects.postgresql import ENUM

revision = '7995a5e4f811'
down_revision = '61737c4342bc'
branch_labels = None
depends_on = None

label_tool = ENUM('RECTANGLE', name='label_tool', create_type=False)


def upgrade():
    label_tool.create(op.get_bind(), checkfirst=True)

    op.create_table('RectangularLabelElements',
                    sa.Column('id', sa.String(), nullable=False),
                    sa.Column('position_x', sa.Float(), nullable=False),
                    sa.Column('position_y', sa.Float(), nullable=False),
                    sa.Column('shape_width', sa.Float(), nullable=False),
                    sa.Column('shape_height', sa.Float(), nullable=False),
                    sa.Column('has_binary_mask', sa.Boolean(), nullable=True),
                    sa.ForeignKeyConstraint(['id'], ['LabelElements.id'],
                                            name=op.f('fk_RectangularLabelElements_id_LabelElements')),
                    sa.PrimaryKeyConstraint('id', name=op.f('pk_RectangularLabelElements'))
                    )

    op.add_column('LabelElements', sa.Column('tool', label_tool, server_default='RECTANGLE'))

    old_label_elements = table('LabelElements', column('id'), column('position_x'), column('position_y'),
                               column('shape_width'), column('shape_height'), column('has_binary_mask'))
    new_rectangular_elements = table('RectangularLabelElements', column('id'), column('position_x'),
                                     column('position_y'), column('shape_width'), column('shape_height'),
                                     column('has_binary_mask'))

    op.execute(
        new_rectangular_elements.insert().from_select(['id', 'position_x', 'position_y', 'shape_width', 'shape_height',
                                                       'has_binary_mask'], old_label_elements.select()))

    op.drop_column('LabelElements', 'position_y')
    op.drop_column('LabelElements', 'shape_width')
    op.drop_column('LabelElements', 'shape_height')
    op.drop_column('LabelElements', 'position_x')
    op.drop_column('LabelElements', 'has_binary_mask')


def downgrade():
    op.add_column('LabelElements', sa.Column('has_binary_mask', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.add_column('LabelElements',
                  sa.Column('position_x', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False,
                            nullable=True))
    op.add_column('LabelElements',
                  sa.Column('shape_height', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False,
                            nullable=True))
    op.add_column('LabelElements',
                  sa.Column('shape_width', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False,
                            nullable=True))
    op.add_column('LabelElements',
                  sa.Column('position_y', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False,
                            nullable=True))
    op.drop_column('LabelElements', 'tool')
    op.drop_table('RectangularLabelElements')
    label_tool.drop(op.get_bind(), checkfirst=True)
