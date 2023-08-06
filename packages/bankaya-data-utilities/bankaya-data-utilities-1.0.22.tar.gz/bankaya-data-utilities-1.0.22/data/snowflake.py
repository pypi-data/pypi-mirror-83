from .util import get_data_yaml_dict
from snowflake.sqlalchemy import URL
from sqlalchemy import create_engine
import pandas as pd
import logging


class Snowflake:
    pool_connections = {}

    @classmethod
    def initialize_connections(cls, environment=None, conn=None):
        try:
            if conn is not None:
                connections = conn
            elif environment is None:
                connections = get_data_yaml_dict(cls.__name__.lower())
            else:
                connections = get_data_yaml_dict(cls.__name__.lower(), environment)

            for connection in connections.keys():
                c = connections[connection]
                db_url = {
                    'user': c['user'],
                    'password': c['password'],
                    'account': c['account'],
                    'warehouse': c['warehouse'],
                    'role': c['role'],
                    'database': c['database'],
                }
                Snowflake.pool_connections[connection] = create_engine(URL(**db_url),
                                                                   pool_size=int(c['pool_size']),
                                                                   max_overflow=int(c['max_overflow']),
                                                                   pool_timeout=int(c['pool_timeout']))
        except Exception as e:
            logging.exception("exception thrown in Snowflake.initialize_connections")

    def get_query_results(self, query, connection):
        try:
            logging.info(f'connection {connection} will run query {query}')
            return pd.read_sql(query, con=Snowflake.pool_connections[connection])
        except Exception as e:
            logging.exception("exception thrown in MYSQL.get_query_results")
            return None