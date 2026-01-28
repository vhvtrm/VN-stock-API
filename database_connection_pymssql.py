"""
Database connection using pymssql (no ODBC required)
Simpler for cloud deployments like Railway
"""

import pymssql
import os
from pathlib import Path


def get_connection():
    """
    Get database connection using pymssql (no ODBC needed)
    Parses connection string from environment variable
    """
    # Get connection string from environment
    conn_string = os.getenv('DC_DB_STRING')

    if not conn_string:
        # Try loading from .env file
        env_file = Path(__file__).parent / '.env'
        if env_file.exists():
            with open(env_file, 'r') as f:
                for line in f:
                    if line.startswith('DC_DB_STRING='):
                        conn_string = line.split('=', 1)[1].strip().strip('"')
                        break

    if not conn_string:
        raise ValueError("DC_DB_STRING environment variable not set")

    # Parse connection string
    params = {}
    for part in conn_string.split(';'):
        if '=' in part:
            key, value = part.split('=', 1)
            params[key.strip()] = value.strip()

    # Extract connection parameters
    server = params.get('SERVER', '').replace('tcp:', '').split(',')[0]
    database = params.get('DATABASE', '')
    uid = params.get('UID', '')
    pwd = params.get('PWD', '')

    # Connect using pymssql
    conn = pymssql.connect(
        server=server,
        user=uid,
        password=pwd,
        database=database,
        port=1433,
        tds_version='7.4'
    )

    return conn


def test_connection():
    """Test database connection"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT @@VERSION")
        version = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        print("✅ Connection successful!")
        print(f"Database: {version[:100]}...")
        return True
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False


if __name__ == '__main__':
    test_connection()
