# Understanding the Database Connection Code

## 🎯 What This Code Does

This code connects to an **Azure SQL Database** (Microsoft's cloud database) using **Microsoft Entra ID** (formerly called Azure Active Directory) authentication. It's designed to access a database called "DClab" that likely contains Vietnamese stock market data.

## 📚 Key Concepts Explained

### 1. **Microsoft Entra ID Authentication**
Instead of using a traditional username/password, this uses Microsoft's identity system:
- You log in once through a browser
- You get a "token" (like a temporary key)
- The token lets you access the database
- The token expires after some time (usually 1 hour)

### 2. **Token Caching**
To avoid logging in every time:
- **In-memory cache**: Stores token while the program runs
- **File cache**: Saves token to `~/.sql_token.json` so it persists between runs
- Checks if token is still valid before requesting a new one

### 3. **Connection String**
The database location and settings are stored in an environment variable `DC_DB_STRING`:
```
DRIVER={ODBC Driver 18 for SQL Server}
SERVER=tcp:sqls-dclab.database.windows.net,1433
DATABASE=dclab_readonly
```
This tells the code:
- Where the database is (sqls-dclab.database.windows.net)
- Which database to use (dclab_readonly)
- How to connect securely (encrypted)

## 🔧 How It Works (Step by Step)

### Step 1: Check for Cached Token
```python
get_cached_token()
```
- Looks in memory first (fastest)
- Then checks the file `~/.sql_token.json`
- If token is still valid, use it immediately

### Step 2: Get New Token (if needed)
```python
get_azure_sql_token()
```
- Opens a browser window
- You log in with your Microsoft account
- Gets an access token from Microsoft
- Caches it for future use

### Step 3: Connect to Database
```python
connect_to_database()
```
- Takes the access token
- Converts it to a special format ODBC understands
- Connects to the Azure SQL database
- Returns a connection object you can use to query data

### Step 4: Query Data
```python
cursor.execute("SELECT * FROM stock_prices")
```
- Use standard SQL queries
- Get Vietnamese stock market data

## 📦 What You Need to Install

```bash
pip install pyodbc azure-identity
```

- **pyodbc**: Python library to connect to SQL databases
- **azure-identity**: Microsoft library for authentication

You also need the ODBC driver installed on your system:
- Windows: Usually pre-installed
- Mac: `brew install microsoft-odbc-driver`
- Linux: Install via package manager

## 🔐 Security Features

1. **No passwords in code**: Uses token-based authentication
2. **Encrypted connection**: All data encrypted in transit
3. **Token expiration**: Tokens expire automatically
4. **Read-only access**: The database name suggests read-only permissions

## 💡 Real-World Usage Example

```python
from database_connection import connect_to_database

# Connect to database
conn = connect_to_database()
cursor = conn.cursor()

# Get Vietnamese stock prices
cursor.execute("""
    SELECT ticker, price, date
    FROM stock_prices
    WHERE date = '2026-01-27'
""")

# Display results
for row in cursor.fetchall():
    print(f"{row.ticker}: {row.price:,.0f} VND")

# Close connection
cursor.close()
conn.close()
```

## 🎪 What Happens on First Run

1. **First time**: Browser opens → You log in → Token saved
2. **Next hour**: Uses cached token, no login needed
3. **After token expires**: Browser opens again for new login

## 🗂️ Database Structure (Likely)

Based on the code, the DClab database probably contains:

```
dclab_readonly/
├── stock_prices        (Daily stock prices)
├── company_info        (Company details)
├── financial_data      (Financial statements)
├── market_indices      (VN-Index, VN30, etc.)
└── trading_volume      (Volume data)
```

## ⚙️ Environment Setup

Before using this code, you need to set the environment variable:

**Mac/Linux:**
```bash
export DC_DB_STRING="DRIVER={ODBC Driver 18 for SQL Server};SERVER=tcp:sqls-dclab.database.windows.net,1433;DATABASE=dclab_readonly;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"
```

**Windows (PowerShell):**
```powershell
$env:DC_DB_STRING="DRIVER={ODBC Driver 18 for SQL Server};SERVER=tcp:sqls-dclab.database.windows.net,1433;DATABASE=dclab_readonly;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"
```

## 🎯 Key Advantages

1. **No API rate limits**: Direct database access
2. **Fast**: Query exactly what you need
3. **Historical data**: Likely has years of stock data
4. **Reliable**: Enterprise-grade database
5. **Secure**: Microsoft's authentication system

## 🚀 Compared to Yahoo Finance API

| Feature | Yahoo Finance | DClab Database |
|---------|--------------|----------------|
| Rate Limits | ⚠️ Yes (strict) | ✅ No limits |
| Speed | 🐌 Slow (HTTP) | ⚡ Fast (direct) |
| Historical Data | 📅 Limited | 📚 Full history |
| Authentication | ✅ None needed | 🔐 Microsoft login |
| Cost | 💰 Free | 💰 Free (if you have access) |

## 🎓 Summary

**In simple terms**: This code is a smart way to connect to your friend's stock market database. Instead of scraping websites or using limited APIs, you get direct access to a professional database with complete Vietnamese stock market data. The authentication is secure (uses Microsoft login), and it remembers your login so you don't have to authenticate every time.

This is much better than the Yahoo Finance approach because:
- ✅ No rate limiting
- ✅ Complete historical data
- ✅ Faster queries
- ✅ More reliable
- ✅ Can get exactly the data you need
