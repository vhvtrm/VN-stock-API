# Integrating Stock Data with Google AI Studio

## 🎯 Overview

To use this database in your Google AI Studio app, you need:
1. **Backend API** (Flask server) - Exposes database as REST API
2. **Google AI Studio** - Calls the API to get stock data

## 🏗️ Architecture

```
Google AI Studio App
        ↓ (HTTP Request)
    Flask API Server
        ↓ (SQL Query)
    Azure SQL Database
```

## 📋 Step-by-Step Setup

### Step 1: Install Additional Dependencies

```bash
pip install flask flask-cors
```

Update your requirements.txt:
```bash
echo "flask>=3.0.0" >> requirements.txt
echo "flask-cors>=4.0.0" >> requirements.txt
```

### Step 2: Start the API Server

```bash
python api_server.py
```

You should see:
```
Vietnamese Stock Price API Server
============================================================
Available Endpoints:
  GET  /api/health
  GET  /api/stock/<symbol>
  POST /api/stocks
  GET  /api/stock/<symbol>/history?days=30
  GET  /api/market/<market>
  GET  /api/search?q=keyword

============================================================
Starting server on http://localhost:5000
```

### Step 3: Test the API

Open another terminal and test:

```bash
# Test health check
curl http://localhost:5000/api/health

# Get VNM price
curl http://localhost:5000/api/stock/VNM

# Get multiple stocks
curl -X POST http://localhost:5000/api/stocks \
  -H "Content-Type: application/json" \
  -d '{"symbols": ["VNM", "VIC", "VHM"]}'

# Get price history
curl http://localhost:5000/api/stock/VNM/history?days=7

# Get market summary
curl http://localhost:5000/api/market/HOSE
```

## 🤖 Using in Google AI Studio

### Option A: Use Function Calling

In Google AI Studio, define these tools/functions:

```javascript
{
  "name": "get_stock_price",
  "description": "Get current price for a Vietnamese stock",
  "parameters": {
    "type": "object",
    "properties": {
      "symbol": {
        "type": "string",
        "description": "Stock ticker symbol (e.g., VNM, VIC, VHM)"
      }
    },
    "required": ["symbol"]
  }
}
```

```javascript
{
  "name": "get_stock_history",
  "description": "Get historical prices for a stock",
  "parameters": {
    "type": "object",
    "properties": {
      "symbol": {
        "type": "string",
        "description": "Stock ticker symbol"
      },
      "days": {
        "type": "integer",
        "description": "Number of days of history (1-365)",
        "default": 30
      }
    },
    "required": ["symbol"]
  }
}
```

### Option B: Direct HTTP Calls in Your App

If you're building a web app with Google AI Studio:

```javascript
// Get single stock price
async function getStockPrice(symbol) {
  const response = await fetch(`http://localhost:5000/api/stock/${symbol}`);
  const data = await response.json();
  return data;
}

// Get multiple stocks
async function getMultipleStocks(symbols) {
  const response = await fetch('http://localhost:5000/api/stocks', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ symbols: symbols })
  });
  const data = await response.json();
  return data;
}

// Get price history
async function getStockHistory(symbol, days = 30) {
  const response = await fetch(
    `http://localhost:5000/api/stock/${symbol}/history?days=${days}`
  );
  const data = await response.json();
  return data;
}

// Example usage
const vnmPrice = await getStockPrice('VNM');
console.log(vnmPrice.data);

const portfolio = await getMultipleStocks(['VNM', 'VIC', 'VHM']);
console.log(portfolio.data);

const history = await getStockHistory('VNM', 7);
console.log(history.data);
```

## 🌐 Deploy to Production

### Option 1: Deploy to Heroku

1. Create `Procfile`:
```
web: python api_server.py
```

2. Create `runtime.txt`:
```
python-3.11
```

3. Deploy:
```bash
heroku create your-stock-api
git push heroku main
```

### Option 2: Deploy to Google Cloud Run

1. Create `Dockerfile`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "api_server.py"]
```

2. Deploy:
```bash
gcloud run deploy stock-api \
  --source . \
  --platform managed \
  --region asia-southeast1 \
  --allow-unauthenticated
```

### Option 3: Deploy to AWS Lambda

Use Zappa for serverless deployment:
```bash
pip install zappa
zappa init
zappa deploy production
```

## 🔐 Important: Environment Variables in Production

When deployed, set these environment variables:

```bash
# Database connection string
export DC_DB_STRING="DRIVER={ODBC Driver 18 for SQL Server};..."

# API key for authentication (optional but recommended)
export API_KEY="your-secret-key"
```

Then update api_server.py to require API key:

```python
from functools import wraps

def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        if api_key != os.getenv('API_KEY'):
            return jsonify({'error': 'Invalid API key'}), 401
        return f(*args, **kwargs)
    return decorated_function

@app.route('/api/stock/<symbol>')
@require_api_key
def get_stock_price(symbol):
    # ... existing code
```

## 📱 Example Google AI Studio Prompt

```
You are a Vietnamese stock market assistant. You have access to real-time
stock prices from the Vietnamese stock market via these functions:

1. get_stock_price(symbol) - Get current price
2. get_stock_history(symbol, days) - Get historical data
3. get_market_summary(market) - Get market overview

Help users analyze stocks, track their portfolio, and make informed decisions.

User: What's the current price of VNM?
Assistant: [Calls get_stock_price("VNM")]
VNM (Vinamilk) is currently trading at 67,800 VND, up 0.15% today.

User: Show me the last 7 days for VIC
Assistant: [Calls get_stock_history("VIC", 7)]
Here's VIC's performance over the last week...
```

## 🎨 Example React Component (if building web UI)

```jsx
import React, { useState, useEffect } from 'react';

function StockPrice({ symbol }) {
  const [price, setPrice] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch(`http://localhost:5000/api/stock/${symbol}`)
      .then(res => res.json())
      .then(data => {
        if (data.success) {
          setPrice(data.data);
        }
        setLoading(false);
      });
  }, [symbol]);

  if (loading) return <div>Loading...</div>;
  if (!price) return <div>No data</div>;

  return (
    <div className="stock-card">
      <h2>{price.symbol}</h2>
      <div className="price">{price.price.toLocaleString()} VND</div>
      <div className={price.change >= 0 ? 'positive' : 'negative'}>
        {price.change >= 0 ? '+' : ''}{price.change.toFixed(2)}
        ({price.pct_change.toFixed(2)}%)
      </div>
    </div>
  );
}

export default StockPrice;
```

## 🔧 Troubleshooting

### CORS Errors
If you get CORS errors in browser:
```python
# In api_server.py, already included:
from flask_cors import CORS
CORS(app)
```

### Connection Timeout
If Google AI Studio times out:
- Deploy API to cloud (not localhost)
- Use a longer timeout in your requests

### Rate Limiting
Add rate limiting to prevent abuse:
```bash
pip install flask-limiter
```

```python
from flask_limiter import Limiter

limiter = Limiter(app, key_func=lambda: request.remote_addr)

@app.route('/api/stock/<symbol>')
@limiter.limit("100 per hour")
def get_stock_price(symbol):
    # ... existing code
```

## 📊 API Response Format

All endpoints return JSON in this format:

**Success:**
```json
{
  "success": true,
  "data": {
    "symbol": "VNM",
    "price": 67800,
    "change": 100,
    "pct_change": 0.15
  }
}
```

**Error:**
```json
{
  "success": false,
  "error": "Error message here"
}
```

## 🎯 Next Steps

1. ✅ Start the API server locally
2. ✅ Test all endpoints with curl
3. ✅ Integrate with Google AI Studio
4. ✅ Deploy to production
5. ✅ Add authentication if needed
6. ✅ Monitor usage and performance

## 💡 Pro Tips

1. **Cache responses** to reduce database load
2. **Add API authentication** for security
3. **Monitor API usage** to prevent abuse
4. **Deploy close to database** (Asia region) for best performance
5. **Use environment variables** for all secrets

Your Google AI Studio app can now access real Vietnamese stock market data! 🚀
