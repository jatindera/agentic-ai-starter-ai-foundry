import pyodbc
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.connection import get_connection_params, build_local_sql_token
from app.db.config import db_settings
import os

SQL_COPT_SS_ACCESS_TOKEN = 1256
ENVIRONMENT = os.getenv("ENVIRONMENT", "LOCAL").upper()


def get_sync_connection():
    conn_str = get_connection_params()

    if ENVIRONMENT == "AZURE":
        # Inside Azure — Managed Identity
        return pyodbc.connect(conn_str)

    # LOCAL — need the AD token
    token_struct = build_local_sql_token()
    return pyodbc.connect(conn_str, attrs_before={SQL_COPT_SS_ACCESS_TOKEN: token_struct})


sync_engine = create_engine(
    "mssql+pyodbc://",
    creator=get_sync_connection,
    pool_size=10,
    max_overflow=20,
    fast_executemany=True,
    echo=False,
)

SessionLocal = sessionmaker(bind=sync_engine, autocommit=False, autoflush=False)
