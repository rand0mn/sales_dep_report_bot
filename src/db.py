import os
from sqlalchemy import create_engine
import pandas as pd


engine = create_engine(os.getenv('DB_URI'))


def query(sql):
    with engine.connect() as con:
        return pd.read_sql(sql, con)
