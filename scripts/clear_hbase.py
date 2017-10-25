"""Script that can clear existing HBase tables"""
from starbase import Connection
from data_labeling import HBASE_SCHEMA
from data_labeling.config import ConfigurationFile


def ask_user_question(prompt_message: str) -> bool:
    """Ask user a question and ask him/her for True/False answer (default answer is False)

    :param prompt_message: message that will be prompted to user
    :return: boolean information if user agrees or not
    """
    answer = input(prompt_message + ' [y/N] ')
    return answer.lower() in ['y', 'yes', 't', 'true']


configuration = ConfigurationFile()
host = configuration.get('hbase', 'host', fallback='localhost')
port = configuration.getint('hbase', 'rest_port', fallback=8080)
connection = Connection(host=host, port=port)

existing_tables = set(connection.tables())

if ask_user_question('Are you sure you want to remove data from "{}:{}"?'.format(host, port)):
    for table_name in existing_tables:
        if ask_user_question('Do you want to remove data from "{}" table?'.format(table_name)):
            print('Clearing data from "{}" table.'.format(table_name))
            table = connection.table(table_name)
            table.drop()
            list_of_columns = HBASE_SCHEMA[table_name]
            table.create(*list_of_columns)
