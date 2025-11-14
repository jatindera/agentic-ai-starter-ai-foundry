from azure.identity import AzureCliCredential

def get_access_token():
    """SYNC access token fetcher for Azure SQL."""
    credential = AzureCliCredential()
    token = credential.get_token("https://database.windows.net/.default").token

    # MUST return UTF-16-LE encoded bytes
    return token.encode("utf-16-le")
