"""Script that can clear existing HBase tables.

How to use it?
--------------
Run this script just by executing following line in the root directory of this project:

    (venv) $ python3.6 scripts/clear_hbase.py

"""
from data_labeling.clients.hbase_client import HBaseClient
from utils import get_connection_to_hbase, user_agrees


HBASE_SCHEMA = HBaseClient.HBASE_SCHEMA
connection = get_connection_to_hbase()
existing_tables = set(connection.tables())

if user_agrees('Are you sure you want to remove data from "{}:{}"?'.format(connection.host, connection.port)):
    for table_name in existing_tables:
        if user_agrees('Do you want to remove data from "{}" table?'.format(table_name)):
            print('Clearing data from "{}" table.'.format(table_name))
            table = connection.table(table_name)
            table.drop()
            list_of_columns = HBASE_SCHEMA[table_name]
            table.create(*list_of_columns)
