"""Module responsible for definition of client for HBase database."""
import logging
from typing import Iterable, List, Mapping, Tuple, Any

import happybase
from retrying import retry
from thriftpy.transport import TTransportException

from medtagger.config import AppConfiguration

logger = logging.getLogger(__name__)

HBASE_CONNECTION_POOL = None


def create_hbase_connection_pool() -> None:
    """Create new HBase Connection Pool."""
    global HBASE_CONNECTION_POOL  # pylint: disable=global-statement
    configuration = AppConfiguration()
    host = configuration.get('hbase', 'host', fallback='localhost')
    port = configuration.getint('hbase', 'port', fallback=9090)
    size = configuration.getint('hbase', 'connection_pool_size', fallback=10)
    try:
        HBASE_CONNECTION_POOL = happybase.ConnectionPool(size, host=host, port=port)
    except (TTransportException, BrokenPipeError):
        logger.warning('Could not connect to HBase. Is it down?')


def is_alive() -> bool:
    """Return boolean information if HBase is alive or not."""
    configuration = AppConfiguration()
    host = configuration.get('hbase', 'host', fallback='localhost')
    port = configuration.getint('hbase', 'port', fallback=9090)
    try:
        happybase.ConnectionPool(1, host=host, port=port)
        return True
    except (TTransportException, BrokenPipeError):
        return False


class HBaseClient(object):
    """Client for HBase.

    How to use this client?
    -----------------------
    This is a wrapper for HappyBase Connection. Client uses HappyBase's Connection Pool, so don't worry about closing
    connection, etc. This client should do everything inside below methods.

    WATCH OUT: Script that migrates HBase schema may not work properly if you want to change column names!
               In such case please run your migration manually!

    Example:

        >>> hbase_client = HBaseClient()
        >>> data = hbase_client.get('my_table_name', 'row_key')
        >>> ...

    """

    ORIGINAL_SLICES_TABLE = 'original_slices'
    CONVERTED_SLICES_TABLE = 'converted_slices'
    LABEL_SELECTION_BINARY_MASK_TABLE = 'label_selection_binary_mask'

    HBASE_SCHEMA = {
        ORIGINAL_SLICES_TABLE: ['image'],
        CONVERTED_SLICES_TABLE: ['image'],
        LABEL_SELECTION_BINARY_MASK_TABLE: ['binary_mask'],
    }

    def __init__(self) -> None:
        """Initialize client."""
        pass

    @staticmethod
    @retry(stop_max_attempt_number=3, wait_random_min=200, wait_random_max=1000,
           retry_on_exception=lambda ex: isinstance(ex, (TTransportException, BrokenPipeError)))
    def get_all_keys(table_name: str, starts_with: str = None) -> Iterable[str]:
        """Fetch all keys for given table.

        :param table_name: name of a table
        :param starts_with: prefix for keys
        :return: iterator for table keys
        """
        assert HBASE_CONNECTION_POOL, 'There is no active Connection Pool to HBase!'
        with HBASE_CONNECTION_POOL.connection() as connection:
            row_prefix = str.encode(starts_with) if starts_with else None
            table = connection.table(table_name)
            for key, _ in table.scan(row_prefix=row_prefix, filter=str.encode('KeyOnlyFilter()')):
                yield key.decode('utf-8')

    @staticmethod
    @retry(stop_max_attempt_number=3, wait_random_min=200, wait_random_max=1000,
           retry_on_exception=lambda ex: isinstance(ex, (TTransportException, BrokenPipeError)))
    def get_all_rows(table_name: str, columns: List, starts_with: str = None) -> Iterable[Tuple[str, Any]]:
        """Fetch all rows for given table.

        :param table_name: name of a table
        :param starts_with: prefix for keys
        :param columns: list of columns to fetch
        :return: iterator for table keys
        """
        assert HBASE_CONNECTION_POOL, 'There is no active Connection Pool to HBase!'
        with HBASE_CONNECTION_POOL.connection() as connection:
            row_prefix = str.encode(starts_with) if starts_with else None
            table = connection.table(table_name)
            for key, value in table.scan(row_prefix=row_prefix, columns=columns):
                yield key.decode('utf-8'), value

    @staticmethod
    @retry(stop_max_attempt_number=3, wait_random_min=200, wait_random_max=1000,
           retry_on_exception=lambda ex: isinstance(ex, (TTransportException, BrokenPipeError)))
    def get(table_name: str, key: str, columns: List[str] = None) -> Mapping:
        """Fetch a single row from HBase table.

        :param table_name: name of a table
        :param key: key representing a row
        :param columns: columns which should be loaded (by default all)
        :return: mapping returned by HBase
        """
        assert HBASE_CONNECTION_POOL, 'There is no active Connection Pool to HBase!'
        hbase_key = str.encode(key)
        with HBASE_CONNECTION_POOL.connection() as connection:
            table = connection.table(table_name)
            return table.row(hbase_key, columns=columns)

    @staticmethod
    @retry(stop_max_attempt_number=3, wait_random_min=200, wait_random_max=1000,
           retry_on_exception=lambda ex: isinstance(ex, (TTransportException, BrokenPipeError)))
    def delete(table_name: str, key: str, columns: List[str] = None) -> None:
        """Delete a single row (or values from colums in given row) in HBase table.

        :param table_name: name of a table
        :param key: key representing a row
        :param columns: columns which should be cleared
        """
        hbase_key = str.encode(key)
        with HBASE_CONNECTION_POOL.connection() as connection:
            table = connection.table(table_name)
            table.delete(hbase_key, columns=columns)

    @staticmethod
    @retry(stop_max_attempt_number=3, wait_random_min=200, wait_random_max=1000,
           retry_on_exception=lambda ex: isinstance(ex, (TTransportException, BrokenPipeError)))
    def put(table_name: str, key: str, value: Any) -> None:
        """Add new entry into HBase table.

        :param table_name: name of a table
        :param key: key under value should be stored
        :param value: value which should be stored
        """
        assert HBASE_CONNECTION_POOL, 'There is no active Connection Pool to HBase!'
        hbase_key = str.encode(key)
        with HBASE_CONNECTION_POOL.connection() as connection:
            table = connection.table(table_name)
            table.put(hbase_key, value)

    @staticmethod
    @retry(stop_max_attempt_number=3, wait_random_min=200, wait_random_max=1000,
           retry_on_exception=lambda ex: isinstance(ex, (TTransportException, BrokenPipeError)))
    def check_if_exists(table_name: str, key: str) -> bool:
        """Scan database and check if given key exists.

        :param table_name: name of a table
        :param key: HBase key
        :return: boolean information if such key exists or not
        """
        assert HBASE_CONNECTION_POOL, 'There is no active Connection Pool to HBase!'
        hbase_key = str.encode(key)
        with HBASE_CONNECTION_POOL.connection() as connection:
            table = connection.table(table_name)
            results = table.scan(row_start=hbase_key, row_stop=hbase_key,
                                 filter=str.encode('KeyOnlyFilter() AND FirstKeyOnlyFilter()'), limit=1)
            return next(results, None) is not None
