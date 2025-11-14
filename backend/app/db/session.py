import pyodbc
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.config import db_settings
from app.db.connection import get_access_token

SQL_COPT_SS_ACCESS_TOKEN = 1256  # ODBC token key


def get_sync_connection():
    token_bytes = get_access_token()

    conn_str = (
        f"DRIVER={{{db_settings.ODBC_DRIVER}}};"
        f"SERVER=tcp:{db_settings.AZURE_SQL_SERVER},1433;"
        f"DATABASE={db_settings.AZURE_SQL_DATABASE};"
        f"Encrypt=yes;"
        f"TrustServerCertificate=no;"
        f"Authentication=ActiveDirectoryAccessToken;"
    )

    return pyodbc.connect(
        conn_str,
        attrs_before={SQL_COPT_SS_ACCESS_TOKEN: token_bytes}
    )


sync_engine = create_engine(
    "mssql+pyodbc://",
    creator=get_sync_connection,
    pool_size=5,
    max_overflow=10,
    echo=False,
    fast_executemany=True,
)

SessionLocal = sessionmaker(bind=sync_engine, autocommit=False, autoflush=False)
