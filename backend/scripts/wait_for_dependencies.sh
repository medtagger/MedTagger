#!/usr/bin/env bash

set -e

until python3.6 -c 'from medtagger.database import is_alive; exit(not is_alive())'; do
  >&2 echo "PostgreSQL is unavailable - waiting..."
  sleep 1
done

until python3.6 -c 'from medtagger.storage import is_alive; exit(not is_alive())'; do
  >&2 echo "Cassandra is unavailable - waiting..."
  sleep 1
done

>&2 echo "OK. PostgreSQL & Cassandra are ready! Let's move on..."

