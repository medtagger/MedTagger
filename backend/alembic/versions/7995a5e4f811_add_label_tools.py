""" Added Label Tools

Introduced Label Tools enum and specific

Revision ID: 7995a5e4f811
Revises: 61737c4342bc
Create Date: 2018-05-03 22:33:59.012448

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import table, column
from sqlalchemy.dialects.postgresql import ENUM

revision = '7995a5e4f811'
down_revision = '61737c4342bc'
branch_labels = None
depends_on = None

label_tool_enum = ENUM('RECTANGLE', name='label_tool', create_type=False)


def upgrade():
    label_tool_enum.create(op.get_bind(), checkfirst=True)

    op.create_table('RectangularLabelElements',
                    sa.Column('id', sa.String(), nullable=False),
                    sa.Column('position_x', sa.Float(), nullable=False),
                    sa.Column('position_y', sa.Float(), nullable=False),
                    sa.Column('shape_width', sa.Float(), nullable=False),
                    sa.Column('shape_height', sa.Float(), nullable=False),
                    sa.ForeignKeyConstraint(['id'], ['LabelElements.id'],
                                            name=op.f('fk_RectangularLabelElements_id_LabelElements')),
                    sa.PrimaryKeyConstraint('id', name=op.f('pk_RectangularLabelElements'))
                    )

    op.add_column('LabelElements', sa.Column('tool', label_tool_enum, server_default='RECTANGLE', nullable=False))

    old_label_elements = table('LabelElements', column('id'), column('position_x'), column('position_y'),
                               column('shape_width'), column('shape_height'))
    new_rectangular_elements = table('RectangularLabelElements', column('id'), column('position_x'),
                                     column('position_y'), column('shape_width'), column('shape_height'))

    op.execute(
        new_rectangular_elements.insert().from_select(['id', 'position_x', 'position_y', 'shape_width', 'shape_height'],
                                                      old_label_elements.select()))

    op.drop_column('LabelElements', 'position_y')
    op.drop_column('LabelElements', 'shape_width')
    op.drop_column('LabelElements', 'shape_height')
    op.drop_column('LabelElements', 'position_x')


def downgrade():
    op.add_column('LabelElements', sa.Column('position_x', sa.Float(), nullable=True))
    op.add_column('LabelElements', sa.Column('shape_height', sa.Float(), nullable=True))
    op.add_column('LabelElements', sa.Column('shape_width', sa.Float(), nullable=True))
    op.add_column('LabelElements', sa.Column('position_y', sa.Float(), nullable=True))

    op.drop_column('LabelElements', 'tool')

    old_label_elements = table('LabelElements', column('id'), column('position_x'), column('position_y'),
                               column('shape_width'), column('shape_height'))
    new_rectangular_elements = table('RectangularLabelElements', column('id'), column('position_x'),
                                     column('position_y'), column('shape_width'), column('shape_height'))

    op.execute(old_label_elements.update().where(new_rectangular_elements.c.id == old_label_elements.c.id).values(
        {
            old_label_elements.c.position_x: new_rectangular_elements.c.position_x,
            old_label_elements.c.position_y: new_rectangular_elements.c.position_y,
            old_label_elements.c.shape_width: new_rectangular_elements.c.shape_width,
            old_label_elements.c.shape_height: new_rectangular_elements.c.shape_height,
        }
    ))

    op.drop_table('RectangularLabelElements')
    label_tool_enum.drop(op.get_bind(), checkfirst=True)
