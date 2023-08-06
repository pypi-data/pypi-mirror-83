# A small package for truncating a table before writing to it

## Install

```powershell
pip install truncate-and-write-to-sql
```

## Example usage

```python
import pandas as pd
from sqlalchemy import create_engine

from truncat_and_write_to_sql.methods import truncate_and_write_sql

# Establish a connection to a SQL database
connection_string = 'a connection string to a database'
engine = create_engine(connection_string)

# Create a dataframe to write to the database
data = {'First Column Name':  ['First value', 'Second value'],
        'Second Column Name': ['First value', 'Second value']}
df = pd.DataFrame(data)

# Truncate existing values and write in new ones
truncate_and_write_sql(
    con=engine,
    df=df,
    table='name of database table',
    schema='database schema e.g. stg',
    if_exists='append',
    mulit=True
)
```