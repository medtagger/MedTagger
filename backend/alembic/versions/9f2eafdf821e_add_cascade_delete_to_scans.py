"""Add cascade delete

Added Cascade delete to:
- Scan,
- Slices,
- Labels,
- LabelElements,
- every type of LabelElements for given tool.

Fixed few naming bugs.

Revision ID: 9f2eafdf821e
Revises: 0707294d0a96
Create Date: 2018-08-24 20:05:43.171568

"""
from alembic import op
import sqlalchemy as sa

revision = '9f2eafdf821e'
down_revision = '0707294d0a96'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_constraint('fk_Slices_scan_id_Scans', 'Slices')
    op.create_foreign_key('fk_Slices_scan_id_Scans', 'Slices', 'Scans', ['scan_id'], ['id'], ondelete='CASCADE')

    op.drop_constraint('fk_Labels_scan_id_Scans', 'Labels')
    op.create_foreign_key('fk_Labels_scan_id_Scans', 'Labels', 'Scans', ['scan_id'], ['id'], ondelete='CASCADE')

    # Droping LabelSelections foreign key (instead of LabelElements) due to naming bug
    op.drop_constraint('fk_LabelSelections_label_id_Labels', 'LabelElements')
    op.create_foreign_key('fk_LabelElements_label_id_Labels', 'LabelElements', 'Labels', ['label_id'], ['id'],
                          ondelete='CASCADE')

    op.drop_constraint('fk_RectangularLabelElements_id_LabelElements', 'RectangularLabelElements')
    op.create_foreign_key(
        'fk_RectangularLabelElements_id_LabelElements', 'RectangularLabelElements', 'LabelElements', ['id'], ['id'],
        ondelete='CASCADE')

    # Altering primary key name from LabelSelections to LabelElements
    op.execute('ALTER INDEX "pk_LabelSelections" RENAME TO "pk_LabelElements"')

    # Dropping PointLabelElement (without 's') due to naming bug
    op.drop_constraint('fk_PointLabelElement_id_LabelElements', 'PointLabelElements')
    op.create_foreign_key(
        'fk_PointLabelElements_id_LabelElements', 'PointLabelElements', 'LabelElements', ['id'], ['id'],
        ondelete='CASCADE')

    op.drop_constraint('fk_ChainLabelElements_id_LabelElements', 'ChainLabelElements')
    op.create_foreign_key(
        'fk_ChainLabelElements_id_LabelElements', 'ChainLabelElements', 'LabelElements', ['id'], ['id'],
        ondelete='CASCADE')

    op.drop_constraint('fk_ChainLabelElementPoints_label_element_id_LabelElements', 'ChainLabelElementPoints')
    op.create_foreign_key(
        'fk_ChainLabelElementPoints_label_element_id_LabelElements', 'ChainLabelElementPoints', 'LabelElements',
        ['label_element_id'], ['id'], ondelete='CASCADE')

    op.drop_constraint('fk_BrushLabelElements_id_LabelElements', 'BrushLabelElements')
    op.create_foreign_key(
        'fk_BrushLabelElements_id_LabelElements', 'BrushLabelElements', 'LabelElements', ['id'], ['id'],
        ondelete='CASCADE')


def downgrade():
    op.drop_constraint('fk_Slices_scan_id_Scans', 'Slices')
    op.create_foreign_key('fk_Slices_scan_id_Scans', 'Slices', 'Scans', ['scan_id'], ['id'])

    op.drop_constraint('fk_Labels_scan_id_Scans', 'Labels')
    op.create_foreign_key('fk_Labels_scan_id_Scans', 'Labels', 'Scans', ['scan_id'], ['id'])

    op.drop_constraint('fk_LabelElements_label_id_Labels', 'LabelElements')
    op.create_foreign_key('fk_LabelSelections_label_id_Labels', 'LabelElements', 'Labels', ['label_id'], ['id'])

    op.execute('ALTER INDEX "pk_LabelElements" RENAME TO "pk_LabelSelections"')

    op.drop_constraint('fk_RectangularLabelElements_id_LabelElements', 'RectangularLabelElements')
    op.create_foreign_key(
        'fk_RectangularLabelElements_id_LabelElements', 'RectangularLabelElements', 'LabelElements', ['id'], ['id'])

    op.drop_constraint('fk_PointLabelElements_id_LabelElements', 'PointLabelElements')
    op.create_foreign_key(
        'fk_PointLabelElement_id_LabelElements', 'PointLabelElements', 'LabelElements', ['id'], ['id'])

    op.drop_constraint('fk_ChainLabelElements_id_LabelElements', 'ChainLabelElements')
    op.create_foreign_key(
        'fk_ChainLabelElements_id_LabelElements', 'ChainLabelElements', 'LabelElements', ['id'], ['id'])

    op.drop_constraint('fk_ChainLabelElementPoints_label_element_id_LabelElements', 'ChainLabelElementPoints')
    op.create_foreign_key(
        'fk_ChainLabelElementPoints_label_element_id_LabelElements', 'ChainLabelElementPoints', 'LabelElements',
        ['label_element_id'], ['id'])

    op.drop_constraint('fk_BrushLabelElements_id_LabelElements', 'BrushLabelElements')
    op.create_foreign_key(
        'fk_BrushLabelElements_id_LabelElements', 'BrushLabelElements', 'LabelElements', ['id'], ['id'])
