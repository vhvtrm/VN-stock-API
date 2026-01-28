"""
Database connection with Microsoft Entra ID authentication for DClab
"""

import os
import json
import struct
import pyodbc
from datetime import datetime, timedelta
from typing import Optional
from azure.identity import InteractiveBrowserCredential


# --------------------------------------------------------------------------------
# CONFIGURATION
# --------------------------------------------------------------------------------

TOKEN_FILE = os.path.expanduser("~/.sql_token.json")  # Cache file for token persistence
AZURE_SQL_SCOPE = "https://database.windows.net/.default"  # Required scope for Azure SQL

# In-memory cache (avoids file I/O on every request)
_token_cache = {
    'token': None,
    'expires_at': None
}


# --------------------------------------------------------------------------------
# AUTHENTICATION
# --------------------------------------------------------------------------------

def get_cached_token() -> Optional[str]:
    """
    Retrieve cached token from memory or file
    Returns None if no valid cached token exists
    """
    # Check in-memory cache first
    if _token_cache['token'] and _token_cache['expires_at']:
        if datetime.now() < _token_cache['expires_at']:
            return _token_cache['token']

    # Check file cache
    if os.path.exists(TOKEN_FILE):
        try:
            with open(TOKEN_FILE, 'r') as f:
                data = json.load(f)
                expires_at = datetime.fromisoformat(data['expires_at'])

                if datetime.now() < expires_at:
                    # Update in-memory cache
                    _token_cache['token'] = data['token']
                    _token_cache['expires_at'] = expires_at
                    return data['token']
        except Exception as e:
            print(f"Error reading token cache: {e}")

    return None


def save_token_to_cache(token: str, expires_on: datetime):
    """Save token to both memory and file cache"""
    # Update in-memory cache
    _token_cache['token'] = token
    _token_cache['expires_at'] = expires_on

    # Save to file
    try:
        with open(TOKEN_FILE, 'w') as f:
            json.dump({
                'token': token,
                'expires_at': expires_on.isoformat()
            }, f)
    except Exception as e:
        print(f"Error saving token cache: {e}")


def get_azure_sql_token() -> str:
    """
    Get Azure SQL access token using Microsoft Entra ID (formerly Azure AD)
    Uses cached token if available, otherwise authenticates interactively
    """
    # Try to use cached token first
    cached_token = get_cached_token()
    if cached_token:
        print("Using cached authentication token")
        return cached_token

    print("No valid cached token found. Starting interactive authentication...")

    # Interactive browser authentication
    credential = InteractiveBrowserCredential()

    # Get token for Azure SQL
    token = credential.get_token(AZURE_SQL_SCOPE)

    # Cache the token (subtract 5 minutes for safety margin)
    expires_at = datetime.fromtimestamp(token.expires_on) - timedelta(minutes=5)
    save_token_to_cache(token.token, expires_at)

    print(f"Successfully authenticated. Token valid until {expires_at}")

    return token.token


# --------------------------------------------------------------------------------
# DATABASE CONNECTION
# --------------------------------------------------------------------------------

def get_connection_string() -> str:
    """
    Get database connection string from environment variable
    Format: DRIVER={ODBC Driver 18 for SQL Server};SERVER=...;DATABASE=...
    """
    conn_string = os.getenv('DC_DB_STRING')

    if not conn_string:
        raise ValueError(
            "DC_DB_STRING environment variable not set.\n"
            "Please set it with your Azure SQL connection string:\n"
            "export DC_DB_STRING='DRIVER={ODBC Driver 18 for SQL Server};SERVER=tcp:sqls-dclab.database.windows.net,1433;DATABASE=dclab_readonly;PWD=DHS!R@v+GESADQF!;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;'"
        )

    return conn_string


def connect_to_database():
    """
    Create connection to Azure SQL Database using Entra ID authentication

    Returns:
        pyodbc.Connection: Active database connection
    """
    # Get access token
    access_token = get_azure_sql_token()

    # Get connection string
    conn_string = get_connection_string()

    # Convert token to the format required by ODBC
    # Token must be passed as a byte string with specific structure
    token_bytes = access_token.encode('utf-16-le')
    token_struct = struct.pack(f'<I{len(token_bytes)}s', len(token_bytes), token_bytes)

    # Create connection with token-based authentication
    # SQL_COPT_SS_ACCESS_TOKEN = 1256
    connection = pyodbc.connect(
        conn_string,
        attrs_before={1256: token_struct}
    )

    print("Successfully connected to Azure SQL Database")

    return connection


# --------------------------------------------------------------------------------
# USAGE EXAMPLE
# --------------------------------------------------------------------------------

def test_connection():
    """Test the database connection"""
    try:
        conn = connect_to_database()
        cursor = conn.cursor()

        # Test query
        cursor.execute("SELECT @@VERSION AS Version")
        row = cursor.fetchone()

        print("\nDatabase Version:")
        print(row.Version)

        cursor.close()
        conn.close()

        print("\n✅ Connection test successful!")

    except Exception as e:
        print(f"\n❌ Connection test failed: {e}")


if __name__ == "__main__":
    test_connection()
