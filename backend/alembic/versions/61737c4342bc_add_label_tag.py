"""Introduced Label Tags

Add label tag table. Changed LabelSelection to Label Elements with two additional columns: lab tag
and element status (label_element_status_enum). Changed Label state type to new enum (label_verification_status_enum).

Revision ID: 61737c4342bc
Revises: 729cd1e8cde1
Create Date: 2018-04-28 14:29:43.351037

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import table, column
from sqlalchemy.dialects.postgresql import ENUM

revision = '61737c4342bc'
down_revision = '729cd1e8cde1'
branch_labels = None
depends_on = None

label_status_enum = ENUM('VALID', 'INVALID', 'NOT_VERIFIED', name='label_status_enum', create_type=False)
label_element_status_enum = ENUM('VALID', 'INVALID', 'NOT_VERIFIED', name='label_element_status_enum',
                                 create_type=False)
label_verification_status_enum = ENUM('VERIFIED', 'NOT_VERIFIED', name='label_verification_status_enum',
                                      create_type=False)


def upgrade():
    label_verification_status_enum.create(op.get_bind(), checkfirst=True)
    label_element_status_enum.create(op.get_bind(), checkfirst=True)

    op.create_table('LabelTags',
                    sa.Column('_created', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
                    sa.Column('_modified', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('key', sa.String(length=50), nullable=False),
                    sa.Column('name', sa.String(length=100), nullable=False),
                    sa.Column('scan_category_id', sa.Integer(), nullable=True),
                    sa.ForeignKeyConstraint(['scan_category_id'], ['ScanCategories.id'],
                                            name=op.f('fk_LabelTags_scan_category_id_ScanCategories')),
                    sa.PrimaryKeyConstraint('id', name=op.f('pk_LabelTags')),
                    sa.UniqueConstraint('key', name=op.f('uq_LabelTags_key'))
                    )

    op.rename_table('LabelSelections', 'LabelElements')
    op.add_column('LabelElements', sa.Column('tag_id', sa.Integer(), nullable=True))
    op.add_column('LabelElements', sa.Column('status', label_element_status_enum,
                                             server_default='NOT_VERIFIED', nullable=False))
    op.create_foreign_key(op.f('fk_LabelElements_tag_id_LabelTags'), 'LabelElements', 'LabelTags', ['tag_id'], ['id'])

    op.add_column('Labels', sa.Column('tmp_status', label_verification_status_enum,
                                      server_default='NOT_VERIFIED', nullable=False))

    labels = table('Labels', column('status'), column('tmp_status'))
    op.execute(labels.update().where(labels.c.status == 'NOT_VERIFIED').values({'tmp_status': 'NOT_VERIFIED'}))
    op.execute(labels.update().where(labels.c.status == 'VALID').values({'tmp_status': 'VERIFIED'}))
    op.execute(labels.update().where(labels.c.status == 'INVALID').values({'tmp_status': 'VERIFIED'}))
    op.drop_column('Labels', 'status')
    op.alter_column('Labels', 'tmp_status', new_column_name='status')

    label_status_enum.drop(op.get_bind(), checkfirst=True)


def downgrade():
    label_status_enum.create(op.get_bind(), checkfirst=True)

    op.drop_constraint(op.f('fk_LabelElements_tag_id_LabelTags'), 'LabelElements', type_='foreignkey')
    op.drop_column('LabelElements', 'status')
    op.drop_column('LabelElements', 'tag_id')
    op.rename_table('LabelElements', 'LabelSelections')

    op.drop_table('LabelTags')
    op.add_column('Labels', sa.Column('tmp_status', label_status_enum, server_default='NOT_VERIFIED', nullable=False))

    labels = table('Labels', column('status'), column('tmp_status'))
    op.execute(labels.update().where(labels.c.status == 'NOT_VERIFIED').values({'tmp_status': 'NOT_VERIFIED'}))
    op.execute(labels.update().where(labels.c.status == 'VERIFIED').values({'tmp_status': 'NOT_VERIFIED'}))
    op.drop_column('Labels', 'status')
    op.alter_column('Labels', 'tmp_status', new_column_name='status')

    label_verification_status_enum.drop(op.get_bind(), checkfirst=True)
    label_element_status_enum.drop(op.get_bind(), checkfirst=True)
