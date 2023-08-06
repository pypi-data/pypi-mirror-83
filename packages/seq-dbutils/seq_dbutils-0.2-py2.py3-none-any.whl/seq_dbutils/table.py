import logging
import re
import sys

import pandas as pd
from sqlalchemy.engine import Engine

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s:%(levelname)s:%(message)s")


class Table:

    def __init__(self, df_table, session_instance, table_subclass):
        assert isinstance(df_table, pd.DataFrame)
        assert hasattr(session_instance, 'execute')
        assert hasattr(table_subclass, '__tablename__')

        self.df_table = df_table
        self.session_instance = session_instance
        self.table_subclass = table_subclass

    def bulk_insert_df_table(self):
        if not self.df_table.empty:
            try:
                logging.info(f"Bulk inserting into table '{self.table_subclass.__tablename__}'")
                self.session_instance.bulk_insert_mappings(self.table_subclass, self.df_table.to_dict(orient='records'))
            except Exception as ex:
                logging.error('Failed to load data into database. Rolling back...')
                self.session_instance.rollback()
                logging.error(str(ex))
                sys.exit(1)
        else:
            logging.info(f"Skipping bulk insert for table '{self.table_subclass.__tablename__}' and empty dataframe")

    def bulk_update_df_table(self):
        if not self.df_table.empty:
            try:
                logging.info(f"Bulk updating table '{self.table_subclass.__tablename__}'")
                self.session_instance.bulk_update_mappings(self.table_subclass, self.df_table.to_dict(orient='records'))
            except Exception as ex:
                logging.error('Failed to update data in database. Rolling back...')
                self.session_instance.rollback()
                logging.error(str(ex))
                sys.exit(1)
        else:
            logging.info(f"Skipping bulk update for table '{self.table_subclass.__tablename__}' and empty dataframe")


class TableUtils:
    def __init__(self, engine, table_name, id_name, id_prefix):
        assert isinstance(engine, Engine)
        assert isinstance(table_name, str)
        assert isinstance(id_name, str)
        assert isinstance(id_prefix, str)
        self.engine = engine
        self.table_name = table_name
        self.id_name = id_name
        self.id_prefix = id_prefix

    def add_prefixed_incremented_id(self, df_input, id_zero_padding=10):
        if self.id_name in list(df_input):
            df_with_id = df_input[~df_input[self.id_name].isnull()].copy()
            df_no_id = df_input[df_input[self.id_name].isnull()].copy()
            del df_no_id[self.id_name]
        else:
            df_with_id = pd.DataFrame()
            df_no_id = df_input.copy()

        pk_sql = f'SELECT {self.id_name} FROM {self.table_name} ORDER BY {self.id_name} DESC LIMIT 1;'
        result = self.engine.execute(pk_sql).fetchone()
        if result:
            # Extract the integer
            last_pk = int(re.sub(self.id_prefix, '', result[0]))
            df_no_id.loc[:, '_id'] = range(last_pk + 1, len(df_no_id) + last_pk + 1)
        else:
            # Start at 1
            df_no_id.loc[:, '_id'] = range(1, len(df_no_id) + 1)

        df_no_id.loc[:, self.id_name] = df_no_id['_id'].apply(lambda x: self.id_prefix + str(x).zfill(id_zero_padding))
        del df_no_id['_id']

        df_out = pd.concat([df_with_id, df_no_id], sort=False)
        return df_out
