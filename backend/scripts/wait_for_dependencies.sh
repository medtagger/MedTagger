#!/usr/bin/env bash

set -e

until python3.7 -c 'from medtagger.database import is_alive; exit(not is_alive())'; do
  >&2 echo "PostgreSQL is unavailable - waiting..."
  sleep 1
done

until python3.7 -c 'from medtagger.storage import is_alive; exit(not is_alive())'; do
  >&2 echo "Storage is unavailable - waiting..."
  sleep 1
done

>&2 echo "OK. PostgreSQL & Storage are ready! Let's move on..."

