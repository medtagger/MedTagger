"""Module responsible for definition of client for HBase database"""
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

    def __init__(self) -> None:
        """Initializer for client"""
        configuration = ConfigurationFile()
        host = configuration.get('hbase', 'host', fallback='localhost')
        port = configuration.getint('hbase', 'port', fallback=9090)
        super(HBaseClient, self).__init__(host, port)
