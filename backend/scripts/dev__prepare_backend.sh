#!/usr/bin/env bash
echo "Waiting for dependencies..."
. scripts/wait_for_dependencies.sh

echo "Running migrations..."
make run_database_migrations

echo "Apply database fixtures..."
python3.6 medtagger/database/fixtures.py

echo "Configuration synchronization..."
cp -n ../.example.medtagger.yml .medtagger.yml
python3.6 scripts/sync_configuration.py

echo "Populate database with default user accounts..."
python3.6 scripts/dev__add_default_accounts.py

