"""Add Slices to Cassandra

Revision ID: ddd21c46f46d
Revises: 75a3481c4d0c
Create Date: 2018-05-04 20:54:48.560358

"""
from medtagger.storage import create_session

# revision identifiers, used by Alembic.
revision = 'ddd21c46f46d'
down_revision = '75a3481c4d0c'
branch_labels = None
depends_on = None

session = create_session()


def upgrade():
    # Create keyspace
    session.execute("""
        CREATE KEYSPACE medtagger
        WITH replication = { 'class': 'SimpleStrategy', 'replication_factor': '3' }
    """)

    # Create all tables
    session.set_keyspace('medtagger')
    session.execute("""
        CREATE TABLE original_slices (
            id text PRIMARY KEY,
            image blob
        )
    """)
    session.execute("""
        CREATE TABLE processed_slices (
            id text PRIMARY KEY,
            image blob
        )
    """)


def downgrade():
    # Remove all tables
    session.set_keyspace('medtagger')
    session.execute('DROP TABLE processed_slices')
    session.execute('DROP TABLE original_slices')

    # Remove keyspace
    session.execute('DROP KEYSPACE medtagger')
