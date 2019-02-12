"""Add Brush Label Element to PostgreSQL and Cassandra

Revision ID: 9a6cd75ba23f
Revises: 39c660178412
Create Date: 2018-05-29 22:48:21.679150

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import ENUM

from medtagger.storage import Storage
from medtagger.storage.cassandra import CassandraStorageBackend

# revision identifiers, used by Alembic.
revision = '9a6cd75ba23f'
down_revision = '39c660178412'
branch_labels = None
depends_on = None

storage = Storage()
old_label_tool_enum = ENUM('RECTANGLE', name='label_tool', create_type=False)
tmp_label_tool_enum = ENUM('RECTANGLE', 'BRUSH', name='label_tool_', create_type=False)
new_label_tool_enum = ENUM('RECTANGLE', 'BRUSH', name='label_tool', create_type=False)


def upgrade():
    # Do not use server default value on Tool column as it will have cause issues during Enum update
    # What's more, it shouldn't have any default value!
    op.alter_column('LabelElements', 'tool', server_default=None)

    # Add Brush as available Tool
    tmp_label_tool_enum.create(op.get_bind(), checkfirst=False)
    op.execute('ALTER TABLE "LabelElements" ALTER COLUMN tool TYPE label_tool_ USING tool::text::label_tool_')
    old_label_tool_enum.drop(op.get_bind(), checkfirst=False)
    new_label_tool_enum.create(op.get_bind(), checkfirst=False)
    op.execute('ALTER TABLE "LabelElements" ALTER COLUMN tool TYPE label_tool USING tool::text::label_tool')
    tmp_label_tool_enum.drop(op.get_bind(), checkfirst=False)

    # Create table in PostgreSQL
    op.create_table('BrushLabelElements',
                    sa.Column('id', sa.String(), nullable=False),
                    sa.Column('width', sa.Integer(), nullable=False),
                    sa.Column('height', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(['id'], ['LabelElements.id'], name=op.f('fk_BrushLabelElements_id_LabelElements')),
                    sa.PrimaryKeyConstraint('id', name=op.f('pk_BrushLabelElements'))
                    )

    # Create table in Cassandra
    if isinstance(storage.backend, CassandraStorageBackend):
        session = storage.backend.create_session()
        session.set_keyspace('medtagger')
        session.execute("""
            CREATE TABLE IF NOT EXISTS brush_label_elements (
                id text PRIMARY KEY,
                image blob
            )
        """)


def downgrade():
    # Remove all tables - both in PostgreSQL and Cassandra
    op.drop_table('BrushLabelElements')
    if isinstance(storage.backend, CassandraStorageBackend):
        session = storage.backend.create_session()
        session.set_keyspace('medtagger')
        session.execute('DROP TABLE brush_label_elements')

    # Remove all elements that were labeled with Brush
    label_elements_table = sa.sql.table('LabelElements', sa.Column('tool', new_label_tool_enum, nullable=False))
    op.execute(label_elements_table.delete().where(label_elements_table.c.tool == 'BRUSH'))

    # Remove Brush as available Tool
    tmp_label_tool_enum.create(op.get_bind(), checkfirst=False)
    op.execute('ALTER TABLE "LabelElements" ALTER COLUMN tool TYPE label_tool_ USING tool::text::label_tool_')
    new_label_tool_enum.drop(op.get_bind(), checkfirst=False)
    old_label_tool_enum.create(op.get_bind(), checkfirst=False)
    op.execute('ALTER TABLE "LabelElements" ALTER COLUMN tool TYPE label_tool USING tool::text::label_tool')
    tmp_label_tool_enum.drop(op.get_bind(), checkfirst=False)

    # Revert server default value on Tool column
    op.alter_column('LabelElements', 'tool', server_default='RECTANGLE')
