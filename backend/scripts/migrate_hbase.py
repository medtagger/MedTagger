"""Script that can migrate existing HBase schema or prepare empty database with given schema.

How to use it?
--------------
Run this script just by executing following line in the root directory of this project:

    (venv) $ python3.6 scripts/migrate_hbase.py

"""
import argparse
import logging
import logging.config

from starbase import Table

from medtagger.clients.hbase_client import HBaseClient
from utils import get_connection_to_hbase, user_agrees

logging.config.fileConfig('logging.conf')
logger = logging.getLogger(__name__)

parser = argparse.ArgumentParser(description='HBase migration.')
parser.add_argument('-y', '--yes', dest='yes', action='store_const', const=True)
args = parser.parse_args()


def create_new_table(table: Table) -> None:
    """Create new table once user agrees on that."""
    table_name = table.name
    if args.yes or user_agrees('Do you want to create table "{}"?'.format(table_name)):
        list_of_columns = HBaseClient.HBASE_SCHEMA[table_name]
        logger.info('Creating table "%s" with columns %s.', table_name, list_of_columns)
        table.create(*list_of_columns)
        table.enable_if_exists_checks()


def update_table_schema(table: Table) -> None:
    """Update table schema once user agrees on that."""
    table_name = table.name
    existing_column_families = set(table.columns())
    schema_column_families = set(HBaseClient.HBASE_SCHEMA[table_name])
    columns_to_add = list(schema_column_families - existing_column_families)
    columns_to_drop = list(existing_column_families - schema_column_families)

    if columns_to_add:
        if args.yes or user_agrees('Do you want to add columns {} to "{}"?'.format(columns_to_add, table_name)):
            table.add_columns(*columns_to_add)

    if columns_to_drop:
        if args.yes or user_agrees('Do you want to drop columns {} from "{}"?'.format(columns_to_drop, table_name)):
            table.drop_columns(*columns_to_drop)


def drop_table(table: Table) -> None:
    """Drop table once user agrees on that."""
    table_name = table.name
    if args.yes or user_agrees('Do you want to drop table "{}"?'.format(table_name)):
        logger.info('Dropping table "%s".', table_name)
        table.drop()


def main() -> None:
    """Run main functionality of this script."""
    connection = get_connection_to_hbase()
    existing_tables = set(connection.tables())
    schema_tables = set(HBaseClient.HBASE_SCHEMA)
    tables_to_drop = list(existing_tables - schema_tables)

    for table_name in tables_to_drop:
        table = connection.table(table_name)
        drop_table(table)

    for table_name in HBaseClient.HBASE_SCHEMA:
        table = connection.table(table_name)
        if not table.exists():
            create_new_table(table)
        else:
            update_table_schema(table)


if __name__ == '__main__':
    main()
