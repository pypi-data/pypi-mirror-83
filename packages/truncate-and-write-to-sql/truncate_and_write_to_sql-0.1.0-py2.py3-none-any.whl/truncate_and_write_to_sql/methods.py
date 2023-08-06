import traceback
import pandas as pd
from sqlalchemy.engine.base import Engine
from sqlalchemy.sql import text

def truncate_and_write_sql(
    con:Engine,
    df:pd.DataFrame,
    table:str,
    schema:str='stg',
    if_exists:str='append',
    multi:bool=False):
        """
        This function truncates a given table then writes the given dataframe
        to that table.

        :param com: The connection to the SQL database
        :param df: The dataframe to be written to the table
        :param table: The name of the table in the database
        :param schema: The database schema, same as for df.to_sql defaults to stg
        :param if_exists: What to do if the table exists in the database, same as
                          for df.to_sql and defaults to Append
        :param multi: Whether or not to use the mulit as method for df.to_sql
        """
        try:
            write_to_sql(con, df, table, schema, if_exists, multi)
            truncate_sql(con, table)
            write_to_sql(con, df, table, schema, if_exists, multi)
        except:
            traceback.print_exc()


def truncate_sql(con:Engine, table:str):
    """
    This function truncates a given table.

    :param com: The connection to the SQL database
    :param table: The name of the table in the database
    """
    con.execute(text(f'''TRUNCATE TABLE [stg].[{table}]''').execution_options(autocommit=True))


def write_to_sql(
    con:Engine,
    df:pd.DataFrame,
    table:str,
    schema:str='stg',
    if_exists:str='append',
    multi:bool=False):
        """
        This function writes the given dataframe to that table.

        :param con: The connection to the SQL database
        :param df: The dataframe to be written to the table
        :param table: The name of the table in the database
        :param schema: The database schema, same as for df.to_sql defaults to stg
        :param if_exists: What to do if the table exists in the database, same as
                          for df.to_sql and defaults to Append
        :param multi: Whether or not to use the mulit as method for df.to_sql
        """
        try:
            df.to_sql(table,
                      schema=schema,
                      con=con,
                      if_exists=if_exists,
                      chunksize=2100//df.shape[1]-1 if multi else 1000,
                      method='multi' if multi else None,
                      index=False)
        except:
            df.to_sql(table,
                      schema=schema,
                      con=con,
                      if_exists=if_exists,
                      chunksize=1000 if multi else 2100//df.shape[1]-1,
                      method=None if multi else 'multi',
                      index=False)