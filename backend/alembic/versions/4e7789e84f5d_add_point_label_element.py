"""Add Point Label Element

Revision ID: 4e7789e84f5d
Revises: 9a6cd75ba23f
Create Date: 2018-06-10 07:59:05.951360

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import ENUM


# revision identifiers, used by Alembic.
revision = '4e7789e84f5d'
down_revision = '9a6cd75ba23f'
branch_labels = None
depends_on = None


old_label_tool_enum = ENUM('RECTANGLE', 'BRUSH',  name='label_tool', create_type=False)
tmp_label_tool_enum = ENUM('RECTANGLE', 'BRUSH', 'POINT', name='label_tool_', create_type=False)
new_label_tool_enum = ENUM('RECTANGLE', 'BRUSH', 'POINT', name='label_tool', create_type=False)


def upgrade():
    # Add Point as available Tool
    tmp_label_tool_enum.create(op.get_bind(), checkfirst=False)
    op.execute('ALTER TABLE "LabelElements" ALTER COLUMN tool TYPE label_tool_ USING tool::text::label_tool_')
    old_label_tool_enum.drop(op.get_bind(), checkfirst=False)
    new_label_tool_enum.create(op.get_bind(), checkfirst=False)
    op.execute('ALTER TABLE "LabelElements" ALTER COLUMN tool TYPE label_tool USING tool::text::label_tool')
    tmp_label_tool_enum.drop(op.get_bind(), checkfirst=False)

    # Create table in PostgreSQL
    op.create_table('PointLabelElements',
                    sa.Column('id', sa.String(), nullable=False),
                    sa.Column('x', sa.Float(), nullable=False),
                    sa.Column('y', sa.Float(), nullable=False),
                    sa.ForeignKeyConstraint(['id'], ['LabelElements.id'],
                                            name=op.f('fk_PointLabelElement_id_LabelElements')),
                    sa.PrimaryKeyConstraint('id', name=op.f('pk_PointLabelElement'))
                    )


def downgrade():
    op.drop_table('PointLabelElements')

    # Remove all elements that were labeled with Point
    label_elements_table = sa.sql.table('LabelElements', sa.Column('tool', new_label_tool_enum, nullable=False))
    op.execute(label_elements_table.delete().where(label_elements_table.c.tool == 'POINT'))

    # Remove Point as available Tool
    tmp_label_tool_enum.create(op.get_bind(), checkfirst=False)
    op.execute('ALTER TABLE "LabelElements" ALTER COLUMN tool TYPE label_tool_ USING tool::text::label_tool_')
    new_label_tool_enum.drop(op.get_bind(), checkfirst=False)
    old_label_tool_enum.create(op.get_bind(), checkfirst=False)
    op.execute('ALTER TABLE "LabelElements" ALTER COLUMN tool TYPE label_tool USING tool::text::label_tool')
    tmp_label_tool_enum.drop(op.get_bind(), checkfirst=False)
