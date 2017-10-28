"""Script that can migrate existing HBase schema or prepare empty database with given schema

How to use it?
--------------
Run this script just by executing following line in the root directory of this project:

    (venv) $ python3.6 scripts/migrate_hbase.py

"""
import argparse

from data_labeling import HBASE_SCHEMA
from utils import get_connection_to_hbase, user_agrees

parser = argparse.ArgumentParser(description='HBase migration.')
parser.add_argument('-y', '--yes', dest='yes', action='store_const', const=True)
args = parser.parse_args()


connection = get_connection_to_hbase()
existing_tables = set(connection.tables())
schema_tables = set(HBASE_SCHEMA)
tables_to_drop = list(existing_tables - schema_tables)
for table_name in tables_to_drop:
    if args.yes or user_agrees('Do you want to drop table "{}"?'.format(table_name)):
        print('Dropping table "{}".'.format(table_name))
        table = connection.table(table_name)
        table.drop()

for table_name in HBASE_SCHEMA:
    table = connection.table(table_name)
    if not table.exists():
        if args.yes or user_agrees('Do you want to create table "{}"?'.format(table_name)):
            list_of_columns = HBASE_SCHEMA[table_name]
            print('Creating table "{}" with columns {}.'.format(table_name, list_of_columns))
            table.create(*list_of_columns)
            table.enable_if_exists_checks()
    else:
        existing_column_families = set(table.columns())
        schema_column_families = set(HBASE_SCHEMA[table_name])
        columns_to_add = list(schema_column_families - existing_column_families)
        columns_to_drop = list(existing_column_families - schema_column_families)

        if columns_to_add:
            if args.yes or user_agrees('Do you want to add columns {} to "{}"?'.format(columns_to_add, table_name)):
                table.add_columns(*columns_to_add)

        if columns_to_drop:
            if args.yes or user_agrees('Do you want to drop columns {} from "{}"?'.format(columns_to_drop, table_name)):
                table.drop_columns(*columns_to_drop)
