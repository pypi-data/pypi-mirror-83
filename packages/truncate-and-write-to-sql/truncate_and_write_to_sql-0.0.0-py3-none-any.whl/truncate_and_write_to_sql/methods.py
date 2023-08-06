import pandas as pd
from sqlalchemy.sql import text

def truncate_and_write_sql(engine, df, table, schema='stg', if_exists='append', multi=False, truncate=True):
    write_to_sql(engine, df, table, schema, if_exists, multi)
    truncate_sql(engine, table)
    write_to_sql(engine, df, table, schema, if_exists, multi)


def truncate_sql(engine, table):
    # Truncate table before writing
    engine.execute(text(f'''TRUNCATE TABLE [stg].[{table}]''').execution_options(autocommit=True))


def write_to_sql(engine, df, table, schema, if_exists, multi=False):
    try:
        df.to_sql(table,
                  schema=schema,
                  con=engine,
                  if_exists=if_exists,
                  chunksize=2100//df.shape[1]-1 if multi else 1000,
                  method='multi' if multi else None,
                  index=False)
    except:
        df.to_sql(table,
                  schema=schema,
                  con=engine,
                  if_exists=if_exists,
                  chunksize=1000 if multi else 2100//df.shape[1]-1,
                  method=None if multi else 'multi',
                  index=False)