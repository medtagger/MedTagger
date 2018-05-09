"""Change columns names of Rectangular Label Elements

Revision ID: 39c660178412
Revises: 7995a5e4f811
Create Date: 2018-05-06 19:12:02.135573

"""
from alembic import op

revision = '39c660178412'
down_revision = '7995a5e4f811'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('RectangularLabelElements', 'position_x', new_column_name='x')
    op.alter_column('RectangularLabelElements', 'position_y', new_column_name='y')
    op.alter_column('RectangularLabelElements', 'shape_height', new_column_name='height')
    op.alter_column('RectangularLabelElements', 'shape_width', new_column_name='width')


def downgrade():
    op.alter_column('RectangularLabelElements', 'x', new_column_name='position_x')
    op.alter_column('RectangularLabelElements', 'y', new_column_name='position_y')
    op.alter_column('RectangularLabelElements', 'height', new_column_name='shape_height')
    op.alter_column('RectangularLabelElements', 'width', new_column_name='shape_width')
