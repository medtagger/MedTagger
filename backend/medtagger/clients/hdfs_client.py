"""Module responsible for definition of client for Hadoop Distributed File System."""
from hdfs3 import HDFileSystem

from medtagger.config import AppConfiguration


class HDFSClient(HDFileSystem):
    """Client for Hadoop Distributed File System.

    How to use this client?
    -----------------------
    It's just a wrapper for HDFileSystem so please follow docs (https://hdfs3.readthedocs.io/en/latest/).

    Example:

        >>> hdfs = HDFSClient()
        >>> with hdfs.open('/tmp/myfile.txt', 'wb') as file:
        ...     file.write('Hello, world!')

    """

    def __init__(self) -> None:
        """Initialize client."""
        configuration = AppConfiguration()
        host = configuration.get('hadoop', 'host', fallback='localhost')
        port = configuration.getint('hadoop', 'namenode_port', fallback=9000)
        super(HDFSClient, self).__init__(host=host, port=port)
