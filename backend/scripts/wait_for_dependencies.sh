#!/usr/bin/env bash

set -e

until python3.7 -c 'from medtagger.database import is_alive; exit(not is_alive())'; do
  >&2 echo "PostgreSQL is unavailable - waiting..."
  sleep 1
done

until python3.7 -c 'from medtagger.storage import Storage; storage = Storage(); exit(not storage.is_alive())'; do
  >&2 echo "Cassandra is unavailable - waiting..."
  sleep 1
done

>&2 echo "OK. PostgreSQL & Cassandra are ready! Let's move on..."

