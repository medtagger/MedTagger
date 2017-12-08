#!/bin/bash

set -e

until python3.6 -c 'from data_labeling.database import is_alive; exit(not is_alive())'; do
  >&2 echo "PostgreSQL is unavailable - waiting..."
  sleep 1
done

until python3.6 -c 'from data_labeling.clients.hbase_client import is_alive; exit(not is_alive())'; do
  >&2 echo "HBase is unavailable - waiting..."
  sleep 1
done

>&2 echo "PostgreSQL & HBase are ready! Let's move on..."

