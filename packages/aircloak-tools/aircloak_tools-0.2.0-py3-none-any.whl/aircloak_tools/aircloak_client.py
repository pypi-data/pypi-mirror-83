import psycopg2
import pandas as pds
import logging

logger = logging.getLogger(__name__)


class AircloakConnection():
    def __init__(self, *, host: str, port: int, user: str, password: str, dataset: str):
        logger.debug(f'Aircloak: Connecting to {dataset} @ {host}:{port}.')
        self.host = host
        self.port = port
        self.dataset = dataset

        try:
            self.conn = psycopg2.connect(
                user=user,
                host=host,
                port=port,
                dbname=dataset,
                password=password)
        except psycopg2.OperationalError as err:
            logger.error(f'internal psycopg2 error: {err}')
            raise

    def close(self):
        logger.debug('Closing Aircloak connection.')
        self.conn.close()

    def is_connected(self):
        return self.conn.closed == 0

    def query(self, statement: str) -> pds.DataFrame:
        logger.debug(f'Sending query {statement}...')
        df = pds.read_sql_query(statement, self.conn)
        logger.debug(f'Got result: {df[:5]}')

        return df

    def get_tables(self) -> pds.DataFrame:
        return self.query("SHOW TABLES")

    def get_columns_for_table(self, table) -> pds.DataFrame:
        return self.query(f'SHOW COLUMNS FROM {table}')

    def count_distinct_values(self, table, column, order_by='count') -> pds.DataFrame:
        return self.query(f'''
            SELECT {column}, count(*) as count
            FROM {table} 
            GROUP BY {column}
            ORDER BY {order_by} DESC''')
