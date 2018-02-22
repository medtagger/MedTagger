#!/usr/bin/env bash
echo "Waiting for dependencies..."
. scripts/wait_for_dependencies.sh

echo "Migrating SQL database..."
alembic upgrade head

echo "Migrating HBase database..."
python3.6 scripts/migrate_hbase.py --yes

echo "Apply database fixtures..."
python3.6 medtagger/database/fixtures.py

echo "Populate database with default user accounts..."
python3.6 scripts/dev__add_default_accounts.py

