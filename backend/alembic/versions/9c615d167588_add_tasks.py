"""Add Tasks

Revision ID: 9c615d167588
Revises: 617bf951f6a2
Create Date: 2018-07-14 19:07:16.544507

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '9c615d167588'
down_revision = '3f2c98c1710b'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('Tasks',
                    sa.Column('_created', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
                    sa.Column('_modified', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
                    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
                    sa.Column('key', sa.String(length=50), nullable=False),
                    sa.Column('name', sa.String(length=100), nullable=False),
                    sa.Column('image_path', sa.String(length=100), nullable=False),
                    sa.PrimaryKeyConstraint('id', name=op.f('pk_Tasks')),
                    sa.UniqueConstraint('key', name=op.f('uq_Tasks_key'))
                    )
    op.create_table('ScanCategories_Tasks',
                    sa.Column('scan_category_id', sa.Integer(), nullable=False),
                    sa.Column('task_id', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(['scan_category_id'], ['ScanCategories.id'],
                                            name=op.f('fk_ScanCategories_Tasks_scan_category_id_ScanCategories')),
                    sa.ForeignKeyConstraint(['task_id'], ['Tasks.id'],
                                            name=op.f('fk_ScanCategories_Tasks_task_id_Tasks'))
                    )
    op.add_column('LabelTags', sa.Column('task_id', sa.Integer(), nullable=False))
    op.create_foreign_key(op.f('fk_LabelTags_task_id_Tasks'), 'LabelTags', 'Tasks', ['task_id'], ['id'])
    op.add_column('Labels', sa.Column('task_id', sa.Integer(), nullable=False))
    op.create_foreign_key(op.f('fk_Labels_task_id_Tasks'), 'Labels', 'Tasks', ['task_id'], ['id'])

    # For each Category create one Task with the same name
    op.execute("""
        INSERT INTO "Tasks"(key, name, image_path)
        SELECT key, name, image_path FROM "ScanCategories"
    """)
    op.execute("""
        INSERT INTO "ScanCategories_Tasks"(scan_category_id, task_id)
        SELECT SC.id, T.id
        FROM "ScanCategories" SC JOIN "Tasks" T
        ON SC.key = T.key
    """)
    op.execute("""
        UPDATE "LabelTags"
        SET task_id = (
          SELECT T.id
          FROM "Tasks" T JOIN "ScanCategories" SC
          ON SC.key = T.key AND SC.id = "LabelTags".scan_category_id
        )
    """)

    op.drop_constraint('fk_LabelTags_scan_category_id_ScanCategories', 'LabelTags', type_='foreignkey')
    op.drop_column('LabelTags', 'scan_category_id')
    op.drop_column('ScanCategories', 'image_path')


def downgrade():
    op.add_column(sa.Column('image_path', sa.String(length=100), nullable=False))
    op.drop_constraint(op.f('fk_Labels_task_id_Tasks'), 'Labels', type_='foreignkey')
    op.drop_column('Labels', 'task_id')
    op.add_column('LabelTags', sa.Column('scan_category_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint(op.f('fk_LabelTags_task_id_Tasks'), 'LabelTags', type_='foreignkey')
    op.create_foreign_key('fk_LabelTags_scan_category_id_ScanCategories', 'LabelTags', 'ScanCategories',
                          ['scan_category_id'], ['id'])
    op.drop_column('LabelTags', 'task_id')
    op.drop_table('ScanCategories_Tasks')
    op.drop_table('Tasks')

    op.execute('DELETE FROM "LabelTags" CASCADE')
