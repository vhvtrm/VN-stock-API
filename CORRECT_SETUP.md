# Correct Setup - SQL Authentication

## From Your Friend's Code

Looking at the connection string from your friend's code image, I can see it uses **SQL Server Authentication** with username and password.

## Correct Connection String Format

```bash
export DC_DB_STRING="DRIVER={ODBC Driver 18 for SQL Server};SERVER=tcp:sqls-dclab.database.windows.net,1433;DATABASE=dclab_readonly;UID=dclab_readonly;PWD=DHS!R@v+GESADQF!;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"
```

**Key parts:**
- `UID=dclab_readonly` - Username (readonly user)
- `PWD=DHS!R@v+GESADQF!` - Password from your friend's code

## Setup Commands

```bash
cd "/Users/vietvu/Coding/Getting market price"

# Set environment variable with full connection string
export ODBCSYSINI=~
export DC_DB_STRING="DRIVER={ODBC Driver 18 for SQL Server};SERVER=tcp:sqls-dclab.database.windows.net,1433;DATABASE=dclab_readonly;UID=dclab_readonly;PWD=DHS!R@v+GESADQF!;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"

# Test connection
python database_connection_simple.py

# If successful, start API server
pkill -f api_server_demo.py
python api_server_real.py
```

## What Was Wrong Before

❌ **Before:** Trying to use Microsoft Entra ID token authentication
✅ **Now:** Using SQL Server username/password authentication

Your friend's database uses simple SQL authentication, not Azure AD/Entra ID!

## Next Step

Run the test command to connect to the real database!
