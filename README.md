# Vietnamese Stock Price Fetcher - Database Version

Get real Vietnamese stock market data from DClab Azure SQL Database using Microsoft Entra ID authentication.

## 🎯 What This Does

This connects directly to a professional stock market database instead of using APIs with rate limits. You get:
- ✅ Real-time stock prices
- ✅ Complete historical data
- ✅ No rate limits
- ✅ Fast queries
- ✅ Professional data quality

## 📋 Prerequisites

1. **Microsoft Account**: You need access to the DClab database
2. **ODBC Driver**: SQL Server ODBC driver installed
3. **Python 3.8+**: Python environment

### Install ODBC Driver

**Mac:**
```bash
brew tap microsoft/mssql-release https://github.com/Microsoft/homebrew-mssql-release
brew update
brew install msodbcsql18
```

**Windows:**
Download from: https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server

**Linux:**
```bash
curl https://packages.microsoft.com/keys/microsoft.asc | sudo apt-key add -
sudo apt-get update
sudo apt-get install msodbcsql18
```

## 🚀 Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Set environment variable:
```bash
export DC_DB_STRING="DRIVER={ODBC Driver 18 for SQL Server};SERVER=tcp:sqls-dclab.database.windows.net,1433;DATABASE=dclab_readonly;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"
```

Add this to your `~/.bashrc` or `~/.zshrc` to make it permanent.

## 📖 Usage

### Test Connection

```bash
python database_connection.py
```

This will:
1. Open a browser for Microsoft login (first time only)
2. Cache your authentication token
3. Test the database connection

### Get Stock Prices

```bash
python get_stock_prices.py
```

### Use in Your Code

```python
from get_stock_prices import StockPriceFetcher

# Create fetcher
fetcher = StockPriceFetcher()

# Get latest price
price = fetcher.get_latest_price('VNM')
print(f"{price['symbol']}: {price['price']:,.0f} VND")

# Get multiple stocks
prices = fetcher.get_multiple_prices(['VIC', 'VHM', 'TCB'])
for symbol, data in prices.items():
    if data:
        fetcher.display_price(data)

# Get price history
history = fetcher.get_price_history('VNM', days=30)
print(history)

# Close connection
fetcher.close()
```

## 🔐 Authentication

### First Time
- Browser opens for Microsoft login
- Token saved to `~/.sql_token.json`
- Token cached in memory

### Subsequent Uses
- Uses cached token (no login needed)
- Token valid for ~1 hour
- Auto-refreshes when expired

## 📁 Files

| File | Purpose |
|------|---------|
| `database_connection.py` | Database authentication & connection |
| `get_stock_prices.py` | Stock price fetching functions |
| `requirements.txt` | Python dependencies |
| `EXPLANATION.md` | Detailed explanation of how it works |

## 🎪 Examples

### Example 1: Get Current Price
```python
from get_stock_prices import StockPriceFetcher

fetcher = StockPriceFetcher()
price = fetcher.get_latest_price('VNM')

if price:
    print(f"VNM Price: {price['price']:,.0f} VND")
    print(f"Change: {price['change']:,.0f} ({price['pct_change']:.2f}%)")

fetcher.close()
```

### Example 2: Monitor Portfolio
```python
from get_stock_prices import StockPriceFetcher

portfolio = ['VNM', 'VIC', 'VHM', 'TCB', 'VPB']

fetcher = StockPriceFetcher()
prices = fetcher.get_multiple_prices(portfolio)

print("Portfolio Summary:")
print("="*60)
for symbol, data in prices.items():
    if data:
        print(f"{symbol}: {data['price']:,.0f} VND ({'+' if data['change'] >= 0 else ''}{data['pct_change']:.2f}%)")

fetcher.close()
```

### Example 3: Price History Chart
```python
from get_stock_prices import StockPriceFetcher
import matplotlib.pyplot as plt

fetcher = StockPriceFetcher()
history = fetcher.get_price_history('VNM', days=30)

plt.figure(figsize=(12, 6))
plt.plot(history['trade_date'], history['close_price'])
plt.title('VNM - 30 Day Price History')
plt.xlabel('Date')
plt.ylabel('Price (VND)')
plt.grid(True)
plt.show()

fetcher.close()
```

### Example 4: Market Overview
```python
from get_stock_prices import StockPriceFetcher

fetcher = StockPriceFetcher()
market = fetcher.get_market_summary('HOSE')

print(f"\nHOSE Market - Top 10 by Volume:")
print(market.nlargest(10, 'volume')[['ticker', 'close_price', 'change_percent', 'volume']])

fetcher.close()
```

## 🆚 Comparison with API Approach

| Feature | Yahoo Finance API | DClab Database |
|---------|------------------|----------------|
| Rate Limits | ⚠️ Strict (429 errors) | ✅ No limits |
| Speed | 🐌 2-3 sec/request | ⚡ Instant |
| Historical Data | 📅 Limited | 📚 Complete |
| Reliability | ⚠️ Can go down | ✅ Enterprise-grade |
| Authentication | ✅ Not needed | 🔐 Microsoft login |
| Data Quality | ⚠️ Sometimes stale | ✅ Professional |

## ⚠️ Important Notes

1. **Database Schema**: The example code assumes certain table/column names. You may need to adjust based on the actual database schema.

2. **First Run**: Browser will open for authentication. This is normal and only happens when token expires.

3. **Token Storage**: Token is stored in `~/.sql_token.json`. Don't commit this file to git.

4. **Environment Variable**: Set `DC_DB_STRING` in your environment for the connection to work.

## 🔍 Troubleshooting

### "DC_DB_STRING environment variable not set"
Set the environment variable:
```bash
export DC_DB_STRING="DRIVER={ODBC Driver 18 for SQL Server};..."
```

### "ODBC Driver not found"
Install the Microsoft ODBC Driver (see Prerequisites section)

### "Authentication failed"
Delete token cache and try again:
```bash
rm ~/.sql_token.json
python database_connection.py
```

### "Table does not exist"
The example code uses assumed table names. Check actual database schema:
```python
conn = connect_to_database()
cursor = conn.cursor()
cursor.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES")
for row in cursor.fetchall():
    print(row.TABLE_NAME)
```

## 📚 Learn More

Read `EXPLANATION.md` for detailed explanation of:
- How authentication works
- Token caching mechanism
- Database connection process
- Security features

## 🤝 Contributing

This code is based on your friend's database connection pattern. Adjust table/column names based on your actual database schema.

## 📄 License

Use freely for your stock market analysis projects.
