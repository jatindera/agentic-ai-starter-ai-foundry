import struct
import os
from azure.identity import AzureCliCredential
from app.db.config import db_settings

ENVIRONMENT = os.getenv("ENVIRONMENT", "LOCAL").upper()


def build_local_sql_token():
    """
    Build the packed SQL access token for LOCAL development using Azure CLI.
    """
    credential = AzureCliCredential()
    token = credential.get_token("https://database.windows.net/.default").token

    # Convert token to expanded token format
    token_bytes = token.encode("UTF-8")
    expanded = b""
    for b in token_bytes:
        expanded += bytes([b])
        expanded += bytes(1)

    return struct.pack("=i", len(expanded)) + expanded


def get_connection_params():
    """
    Returns the correct ODBC connection string
    depending on environment (LOCAL vs AZURE).
    """
    if ENVIRONMENT == "AZURE":
        # App Service / Function with Managed Identity
        return (
            f"Driver={{{db_settings.ODBC_DRIVER}}};"
            f"Server=tcp:{db_settings.AZURE_SQL_SERVER},1433;"
            f"Database={db_settings.AZURE_SQL_DATABASE};"
            f"Authentication=ActiveDirectoryMsi;"
            f"Encrypt=yes;"
            f"TrustServerCertificate=no;"
        )

    # LOCAL DEV with Azure CLI RBAC
    return (
        f"Driver={{{db_settings.ODBC_DRIVER}}};"
        f"Server=tcp:{db_settings.AZURE_SQL_SERVER},1433;"
        f"Database={db_settings.AZURE_SQL_DATABASE};"
        f"Encrypt=yes;"
        f"TrustServerCertificate=no;"
    )
