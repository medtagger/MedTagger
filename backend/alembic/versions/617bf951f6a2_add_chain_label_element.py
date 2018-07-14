"""Add Chain Label Element

Revision ID: 617bf951f6a2
Revises: e1d0a4fcf63c
Create Date: 2018-07-08 09:59:44.803619

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
from sqlalchemy.dialects.postgresql import ENUM


revision = '617bf951f6a2'
down_revision = '01dc85c25335'
branch_labels = None
depends_on = None


old_label_tool_enum = ENUM('RECTANGLE', 'BRUSH', 'POINT', name='label_tool', create_type=False)
tmp_label_tool_enum = ENUM('RECTANGLE', 'BRUSH', 'POINT', 'CHAIN', name='label_tool_', create_type=False)
new_label_tool_enum = ENUM('RECTANGLE', 'BRUSH', 'POINT', 'CHAIN', name='label_tool', create_type=False)


def upgrade():
    # Add Chain as available Tool
    tmp_label_tool_enum.create(op.get_bind(), checkfirst=False)
    op.execute('ALTER TABLE "LabelElements" ALTER COLUMN tool TYPE label_tool_ USING tool::text::label_tool_')
    old_label_tool_enum.drop(op.get_bind(), checkfirst=False)
    new_label_tool_enum.create(op.get_bind(), checkfirst=False)
    op.execute('ALTER TABLE "LabelElements" ALTER COLUMN tool TYPE label_tool USING tool::text::label_tool')
    tmp_label_tool_enum.drop(op.get_bind(), checkfirst=False)

    op.create_table('ChainLabelElementPoints',
                    sa.Column('_created', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
                    sa.Column('_modified', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
                    sa.Column('id', sa.String(), nullable=False),
                    sa.Column('x', sa.Float(), nullable=False),
                    sa.Column('y', sa.Float(), nullable=False),
                    sa.Column('label_element_id', sa.String(), nullable=False),
                    sa.Column('order', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(['label_element_id'], ['LabelElements.id'], name=op.f('fk_ChainLabelElementPoints_label_element_id_LabelElements')),
                    sa.PrimaryKeyConstraint('id', name=op.f('pk_ChainLabelElementPoints'))
                    )
    op.create_table('ChainLabelElements',
                    sa.Column('id', sa.String(), nullable=False),
                    sa.Column('loop', sa.Boolean(), nullable=False),
                    sa.ForeignKeyConstraint(['id'], ['LabelElements.id'], name=op.f('fk_ChainLabelElements_id_LabelElements')),
                    sa.PrimaryKeyConstraint('id', name=op.f('pk_ChainLabelElements'))
                    )


def downgrade():
    op.drop_table('ChainLabelElements')
    op.drop_table('ChainLabelElementPoints')

    # Remove all elements that were labeled with Chain
    label_elements_table = sa.sql.table('LabelElements', sa.Column('tool', new_label_tool_enum, nullable=False))
    op.execute(label_elements_table.delete().where(label_elements_table.c.tool == 'CHAIN'))

    # Remove Chain as available Tool
    tmp_label_tool_enum.create(op.get_bind(), checkfirst=False)
    op.execute('ALTER TABLE "LabelElements" ALTER COLUMN tool TYPE label_tool_ USING tool::text::label_tool_')
    new_label_tool_enum.drop(op.get_bind(), checkfirst=False)
    old_label_tool_enum.create(op.get_bind(), checkfirst=False)
    op.execute('ALTER TABLE "LabelElements" ALTER COLUMN tool TYPE label_tool USING tool::text::label_tool')
    tmp_label_tool_enum.drop(op.get_bind(), checkfirst=False)
