"""Rename Scan Category to Dataset

Revision ID: 569a3b109b71
Revises: 14898bcabb8a
Create Date: 2018-08-15 16:15:16.166709

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '569a3b109b71'
down_revision = '14898bcabb8a'
branch_labels = None
depends_on = None


def upgrade():
    op.rename_table('ScanCategories', 'Datasets')
    op.execute('ALTER INDEX "pk_ScanCategories" RENAME TO "pk_Datasets"')
    op.execute('ALTER INDEX "uq_ScanCategories_key" RENAME TO "uq_Datasets_key"')

    op.rename_table('ScanCategories_Tasks', 'Datasets_Tasks')
    op.alter_column('Datasets_Tasks', 'scan_category_id', new_column_name='dataset_id')
    op.drop_constraint('fk_ScanCategories_Tasks_scan_category_id_ScanCategories', 'Datasets_Tasks')
    op.create_foreign_key('fk_Datasets_Tasks_dataset_id_Datasets', 'Datasets_Tasks', 'Datasets', ['dataset_id'], ['id'])
    op.drop_constraint('fk_ScanCategories_Tasks_task_id_Tasks', 'Datasets_Tasks')
    op.create_foreign_key('fk_Datasets_Tasks_task_id_Tasks', 'Datasets_Tasks', 'Tasks', ['task_id'], ['id'])

    op.alter_column('Scans', 'category_id', new_column_name='dataset_id')
    op.drop_constraint('fk_Scans_category_id_ScanCategories', 'Scans')
    op.create_foreign_key('fk_Scans_dataset_id_Datasets', 'Scans', 'Datasets', ['dataset_id'], ['id'])


def downgrade():
    op.rename_table('Datasets', 'ScanCategories')
    op.execute('ALTER INDEX "pk_Datasets" RENAME TO "pk_ScanCategories"')
    op.execute('ALTER INDEX "uq_Datasets_key" RENAME TO "uq_ScanCategories_key"')

    op.rename_table('Datasets_Tasks', 'ScanCategories_Tasks')
    op.alter_column('ScanCategories_Tasks', 'dataset_id', new_column_name='scan_category_id')
    op.drop_constraint('fk_Datasets_Tasks_dataset_id_Datasets', 'ScanCategories_Tasks')
    op.create_foreign_key('fk_ScanCategories_Tasks_scan_category_id_ScanCategories', 'ScanCategories_Tasks',
                          'ScanCategories', ['scan_category_id'], ['id'])
    op.drop_constraint('fk_Datasets_Tasks_task_id_Tasks', 'ScanCategories_Tasks')
    op.create_foreign_key('fk_ScanCategories_Tasks_task_id_Tasks', 'ScanCategories_Tasks', 'Tasks', ['task_id'], ['id'])

    op.alter_column('Scans', 'dataset_id', new_column_name='category_id')
    op.drop_constraint('fk_Scans_dataset_id_Datasets', 'Scans')
    op.create_foreign_key('fk_Scans_category_id_ScanCategories', 'Scans', 'ScanCategories', ['category_id'], ['id'])
