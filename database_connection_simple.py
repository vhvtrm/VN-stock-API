"""
Simple Database Connection - Direct ODBC without Entra ID
For read-only database access
"""

import os
import pyodbc
from pathlib import Path


def get_connection_string() -> str:
    """Get database connection string from environment variable or .env file"""
    # Try environment variable first
    conn_string = os.getenv('DC_DB_STRING')

    # If not in environment, try loading from .env file
    if not conn_string:
        env_file = Path(__file__).parent / '.env'
        if env_file.exists():
            with open(env_file, 'r') as f:
                for line in f:
                    if line.startswith('DC_DB_STRING='):
                        conn_string = line.split('=', 1)[1].strip().strip('"')
                        break

            # Also load ODBCSYSINI
            env_file_content = env_file.read_text()
            for line in env_file_content.split('\n'):
                if line.startswith('ODBCSYSINI='):
                    os.environ['ODBCSYSINI'] = line.split('=', 1)[1].strip()

    if not conn_string:
        raise ValueError(
            "DC_DB_STRING not found in environment or .env file.\n"
            "Please set it with your Azure SQL connection string."
        )

    return conn_string


def connect_to_database():
    """
    Create direct connection to Azure SQL Database
    No Entra ID authentication - uses connection string directly

    Returns:
        pyodbc.Connection: Active database connection
    """
    # Get connection string
    conn_string = get_connection_string()

    print("Connecting to database...")

    # Create direct connection
    connection = pyodbc.connect(conn_string)

    print("✅ Successfully connected to Azure SQL Database")

    return connection


def test_connection():
    """Test the database connection"""
    try:
        conn = connect_to_database()
        cursor = conn.cursor()

        # Test query
        print("\nTesting connection with query...")
        cursor.execute("SELECT @@VERSION AS Version")
        row = cursor.fetchone()

        print("\n" + "="*60)
        print("Database Version:")
        print(row.Version[:200] + "...")
        print("="*60)

        # Try to list tables
        print("\nListing tables...")
        cursor.execute("""
            SELECT TOP 5 TABLE_SCHEMA, TABLE_NAME
            FROM INFORMATION_SCHEMA.TABLES
            WHERE TABLE_TYPE = 'BASE TABLE'
            ORDER BY TABLE_NAME
        """)

        print("\nFirst 5 tables in database:")
        for row in cursor.fetchall():
            print(f"  - {row.TABLE_SCHEMA}.{row.TABLE_NAME}")

        cursor.close()
        conn.close()

        print("\n✅ Connection test successful!")
        return True

    except Exception as e:
        print(f"\n❌ Connection test failed: {e}")
        return False


if __name__ == "__main__":
    test_connection()
