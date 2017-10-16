"""Module responsible for definition of client for HBase database"""
from typing import Iterable

import happybase

from data_labeling.config import ConfigurationFile


class HBaseClient(happybase.Connection):
    """Client that wraps connection to the HBase

    How to use this client?
    -----------------------
    It's just a wrapper for happybase.Connection so please follow docs (https://happybase.readthedocs.io/en/latest/).

    Example:

        >>> database = HBaseClient()
        >>> table = database.table('my_table_name')
        >>> ...

    """

    SCANS = 'scans'
    ORIGINAL_SLICES_TABLE = 'original_slices'
    CONVERTED_SLICES_TABLE = 'converted_slices'

    def __init__(self) -> None:
        """Initializer for client"""
        configuration = ConfigurationFile()
        host = configuration.get('hbase', 'host', fallback='localhost')
        port = configuration.getint('hbase', 'port', fallback=9090)
        super(HBaseClient, self).__init__(host, port)

    def get_all_keys(self, table_name: str, starts_with: str = None) -> Iterable[str]:
        """Fetch all keys for given table

        :param table_name: name of a table
        :param starts_with: prefix for keys
        :return: iterator for table keys
        """
        row_prefix = str.encode(starts_with) if starts_with else None
        table = self.table(table_name)
        for key, _ in table.scan(row_prefix=row_prefix, filter=str.encode('KeyOnlyFilter()')):
            yield key

    def check_if_exists(self, table_name: str, key: str) -> bool:
        """Scan database and check if given key exists

        :param table_name: name of a table
        :param key: HBase key
        :return: boolean information if such key exists or not
        """
        hbase_key = str.encode(key)
        table = self.table(table_name)
        results = table.scan(row_start=hbase_key, row_stop=hbase_key,
                             filter=str.encode('KeyOnlyFilter() AND FirstKeyOnlyFilter()'), limit=1)
        return next(results, None) is not None
