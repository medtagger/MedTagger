#!/usr/bin/env bash
echo "Waiting for dependencies..."
. scripts/wait_for_dependencies.sh

echo "Migrating databases..."
alembic upgrade head

echo "Apply database fixtures..."
python3.6 medtagger/database/fixtures.py

echo "Populate database with default user accounts..."
python3.6 scripts/dev__add_default_accounts.py

