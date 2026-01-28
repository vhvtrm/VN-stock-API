# Switch from Demo to Real API

## Current Situation
- ✅ Running: `api_server_demo.py` (mock/fake data)
- ❌ Not running: `api_server.py` (real database data)

## Why Demo vs Real?

### Demo API (`api_server_demo.py`)
- ✅ Works immediately (no setup)
- ✅ No database connection needed
- ❌ Fake prices (randomly generated)
- ❌ Not real market data

### Real API (`api_server.py`)
- ✅ Real Vietnamese stock prices
- ✅ Live data from Azure SQL Database
- ❌ Requires database access
- ❌ Requires Microsoft authentication

## How to Switch to Real API

### Step 1: Set Environment Variable

```bash
export DC_DB_STRING="DRIVER={ODBC Driver 18 for SQL Server};SERVER=tcp:sqls-dclab.database.windows.net,1433;DATABASE=dclab_readonly;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"
```

Add this to your `~/.zshrc` or `~/.bashrc` to make it permanent:
```bash
echo 'export DC_DB_STRING="DRIVER={ODBC Driver 18 for SQL Server};SERVER=tcp:sqls-dclab.database.windows.net,1433;DATABASE=dclab_readonly;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"' >> ~/.zshrc
source ~/.zshrc
```

### Step 2: Stop Demo API

```bash
# Stop the demo server
pkill -f api_server_demo.py
```

### Step 3: Test Database Connection

```bash
python database_connection.py
```

This will:
1. Open a browser for Microsoft login (first time only)
2. Test the database connection
3. Cache your authentication token

### Step 4: Start Real API

```bash
python api_server.py
```

**Note:** Make sure to update `api_server.py` to use port 5001 (same as demo):
- Change `port=5000` to `port=5001` in the code

### Step 5: Test Real API

```bash
# Test with real data
curl http://localhost:5001/api/stock/VNM
```

You should now see REAL Vietnamese stock prices! 🎉

## Quick Command to Switch

Run this single command to switch:

```bash
# Stop demo, start real API
pkill -f api_server_demo.py && \
export DC_DB_STRING="DRIVER={ODBC Driver 18 for SQL Server};SERVER=tcp:sqls-dclab.database.windows.net,1433;DATABASE=dclab_readonly;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;" && \
python api_server.py
```

## Troubleshooting

### "DC_DB_STRING environment variable not set"
→ You forgot to set the environment variable (Step 1)

### "Authentication failed"
→ You need to log in with Microsoft account (Step 3)

### "Table does not exist"
→ The database schema might be different than assumed
→ Check actual table names in the database

### "Can't connect to database"
→ Check if you have access to the DClab database
→ Contact your friend who shared the connection string

## Comparison

| Feature | Demo API | Real API |
|---------|----------|----------|
| Data Source | Random/Mock | Azure SQL Database |
| Prices | Fake | Real market prices |
| Setup Time | Instant | ~5 minutes |
| Database Required | No | Yes |
| Authentication | No | Microsoft login |
| Rate Limits | None | None |
| Cost | Free | Free (if you have access) |

## Current Demo Base Prices

The demo uses these hardcoded base prices:
- VNM: 67,800 VND
- VIC: 42,500 VND
- VHM: 65,000 VND
- TCB: 28,000 VND
- VPB: 23,500 VND
- HPG: 24,800 VND
- MWG: 52,000 VND
- FPT: 128,000 VND
- MSN: 67,500 VND
- SSI: 45,000 VND

Then adds random variation each time, so prices look different every refresh.

## Summary

**To get REAL prices:**
1. Set `DC_DB_STRING` environment variable
2. Stop demo API
3. Authenticate with Microsoft (first time)
4. Start real API server
5. Your web app will now show real Vietnamese stock prices!

The demo is great for testing, but when you're ready to integrate with Google AI Studio for real, switch to the real API to get actual market data.
