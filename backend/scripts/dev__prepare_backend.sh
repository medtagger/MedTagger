#!/usr/bin/env bash
echo "Waiting for dependencies..."
. scripts/wait_for_dependencies.sh

echo "Running migrations..."
make run_database_migrations

echo "Apply database fixtures..."
python3.7 medtagger/database/fixtures.py

echo "Configuration synchronization..."
cp -n .example.medtagger.yml .medtagger.yml || :
if [ -z "$1" ]; then
    python3.7 scripts/sync_configuration.py
else
    python3.7 scripts/sync_configuration.py --configuration=$1
fi

echo "Populate database with default user accounts..."
python3.7 scripts/dev__add_default_accounts.py
