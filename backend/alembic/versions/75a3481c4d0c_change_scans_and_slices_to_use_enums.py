"""Change Scans and Slices to use enums

Revision ID: 75a3481c4d0c
Revises: f49f6dc9b600
Create Date: 2018-04-29 17:34:56.544501

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import ENUM


# revision identifiers, used by Alembic.
revision = '75a3481c4d0c'
down_revision = 'f49f6dc9b600'
branch_labels = None
depends_on = None

scan_status_enum = ENUM('NEW', 'STORED', 'PROCESSING', 'AVAILABLE', name='scan_status_enum', create_type=False)
slice_status_enum = ENUM('NEW', 'STORED', 'PROCESSED', name='slice_status_enum', create_type=False)


def upgrade():
    # At first, create all enums
    scan_status_enum.create(op.get_bind(), checkfirst=True)
    slice_status_enum.create(op.get_bind(), checkfirst=True)

    # Add new columns with statuses
    op.add_column('Scans', sa.Column('status', scan_status_enum, server_default='NEW', nullable=False))
    op.add_column('Slices', sa.Column('status', slice_status_enum, server_default='NEW', nullable=False))

    # Run data migration
    scans = sa.table('Scans', sa.column('status'), sa.column('converted'))
    op.execute(scans.update().where(scans.c.converted).values({'status': 'AVAILABLE'}))
    slices = sa.table('Slices', sa.column('status'), sa.column('stored'), sa.column('converted'))
    op.execute(slices.update().where(slices.c.stored).values({'status': 'STORED'}))
    op.execute(slices.update().where(slices.c.converted).values({'status': 'PROCESSED'}))

    # Remove legacy columns
    op.drop_column('Scans', 'converted')
    op.drop_column('Slices', 'converted')
    op.drop_column('Slices', 'stored')


def downgrade():
    # Revert all previous columns
    op.add_column('Slices', sa.Column('stored', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.add_column('Slices', sa.Column('converted', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.add_column('Scans', sa.Column('converted', sa.BOOLEAN(), autoincrement=False, nullable=True))

    # Run data migration
    scans = sa.table('Scans', sa.column('status'), sa.column('converted'))
    op.execute(scans.update().where(scans.c.status == 'AVAILABLE').values({'converted': True}))
    slices = sa.table('Slices', sa.column('status'), sa.column('stored'), sa.column('converted'))
    op.execute(slices.update().where(slices.c.status == 'STORED').values({'stored': True}))
    op.execute(slices.update().where(slices.c.status == 'PROCESSED').values({'stored': True}))
    op.execute(slices.update().where(slices.c.status == 'PROCESSED').values({'converted': True}))

    # Remove newly added columns with statuses
    op.drop_column('Slices', 'status')
    op.drop_column('Scans', 'status')

    # Remove all enums
    scan_status_enum.drop(op.get_bind(), checkfirst=True)
    slice_status_enum.drop(op.get_bind(), checkfirst=True)
