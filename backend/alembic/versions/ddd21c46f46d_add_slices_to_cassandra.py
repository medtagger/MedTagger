"""Add Slices to Cassandra

Revision ID: ddd21c46f46d
Revises: 75a3481c4d0c
Create Date: 2018-05-04 20:54:48.560358

"""
from medtagger.storage import Storage
from medtagger.storage.cassandra import CassandraStorageBackend

# revision identifiers, used by Alembic.
revision = 'ddd21c46f46d'
down_revision = '75a3481c4d0c'
branch_labels = None
depends_on = None

storage = Storage()


def upgrade():
    # Create structure in Cassandra
    if isinstance(storage.storage_backend, CassandraStorageBackend):
        session = storage.storage_backend.create_session()

        # Create key space
        session.execute("""
            CREATE KEYSPACE IF NOT EXISTS medtagger
            WITH replication = { 'class': 'SimpleStrategy', 'replication_factor': '3' }
        """)

        # Create all tables
        session.set_keyspace('medtagger')
        session.execute("""
            CREATE TABLE IF NOT EXISTS original_slices (
                id text PRIMARY KEY,
                image blob
            )
        """)
        session.execute("""
            CREATE TABLE IF NOT EXISTS processed_slices (
                id text PRIMARY KEY,
                image blob
            )
        """)


def downgrade():
    # Remove structure from Cassandra
    if isinstance(storage.storage_backend, CassandraStorageBackend):
        session = storage.storage_backend.create_session()

        # Remove all tables
        session.set_keyspace('medtagger')
        session.execute('DROP TABLE processed_slices')
        session.execute('DROP TABLE original_slices')

        # Remove keyspace
        session.execute('DROP KEYSPACE medtagger')
