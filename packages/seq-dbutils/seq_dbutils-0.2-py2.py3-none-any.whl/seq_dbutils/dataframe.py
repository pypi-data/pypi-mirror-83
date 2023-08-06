import logging
import sys
from datetime import datetime
from os.path import isfile

import pandas as pd

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s:%(levelname)s:%(message)s")


class DataFrameUtils:

    @staticmethod
    def read_csv_with_header_mapping(csv_filepath, col_name_mapping_dict=None):
        if isfile(csv_filepath):
            df = pd.read_csv(csv_filepath, header='infer', low_memory=False)
            logging.info(f'Read file {csv_filepath} with lines: %s', len(df))
            if col_name_mapping_dict:
                df.rename(columns=col_name_mapping_dict, inplace=True)
            return df
        else:
            logging.error(f'File {csv_filepath} does not exist. Exiting...')
            sys.exit(1)

    @staticmethod
    def apply_date_format(input_date, format_date):
        if input_date:
            if input_date == '-':
                input_date = None
            else:
                format_time = format_date + ' %H:%M:%S'
                try:
                    input_date = datetime.strptime(input_date, format_date).date()
                except ValueError as ex:
                    if 'unconverted data remains:' in ex.args[0]:
                        input_date = datetime.strptime(input_date, format_time).date()
                    else:
                        logging.error(str(ex))
                        sys.exit(1)
        else:
            input_date = None
        return input_date

    @staticmethod
    def remove_rows_with_blank_col_subset(df, col_list):
        assert isinstance(col_list, list)
        df_subset = df.filter(col_list, axis=1)
        df_na_subset = df_subset[pd.isnull(df_subset).all(axis=1)]
        if not df_na_subset.empty:
            df_no_nas = df.dropna(subset=col_list, how='all')
            df_no_nas.reset_index(inplace=True, drop=True)
        else:
            df_no_nas = df.copy()
        return df_no_nas
