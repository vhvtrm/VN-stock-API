# Quick Start: Integrate with Google AI Studio

## 🚀 3-Step Setup

### Step 1: Install Dependencies (2 minutes)

```bash
pip install -r requirements.txt
```

### Step 2: Set Environment Variable (30 seconds)

```bash
export DC_DB_STRING="DRIVER={ODBC Driver 18 for SQL Server};SERVER=tcp:sqls-dclab.database.windows.net,1433;DATABASE=dclab_readonly;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"
```

### Step 3: Start API Server (10 seconds)

```bash
python api_server.py
```

✅ **Done!** Your API is now running at `http://localhost:5000`

---

## 🧪 Test It Works

Open `example_ai_app.html` in your browser to see a demo app using the API.

Or test with curl:
```bash
curl http://localhost:5000/api/stock/VNM
```

---

## 🤖 Use in Google AI Studio

### Method 1: Function Calling (Recommended)

Define these functions in Google AI Studio:

```json
{
  "name": "get_stock_price",
  "description": "Get current price for Vietnamese stock",
  "parameters": {
    "type": "object",
    "properties": {
      "symbol": {
        "type": "string",
        "description": "Stock ticker (VNM, VIC, etc.)"
      }
    },
    "required": ["symbol"]
  }
}
```

In your function handler:
```javascript
async function get_stock_price(symbol) {
  const response = await fetch(`http://localhost:5000/api/stock/${symbol}`);
  const data = await response.json();
  return data.data;
}
```

### Method 2: Direct API Calls

In your Google AI Studio app code:

```javascript
// Get single stock
async function getStock(symbol) {
  const res = await fetch(`http://localhost:5000/api/stock/${symbol}`);
  return await res.json();
}

// Get multiple stocks
async function getStocks(symbols) {
  const res = await fetch('http://localhost:5000/api/stocks', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({ symbols })
  });
  return await res.json();
}

// Get history
async function getHistory(symbol, days = 30) {
  const res = await fetch(`http://localhost:5000/api/stock/${symbol}/history?days=${days}`);
  return await res.json();
}
```

---

## 📊 Available Endpoints

| Endpoint | Method | Description | Example |
|----------|--------|-------------|---------|
| `/api/health` | GET | Check API status | - |
| `/api/stock/<symbol>` | GET | Get single stock | `/api/stock/VNM` |
| `/api/stocks` | POST | Get multiple stocks | `{"symbols": ["VNM", "VIC"]}` |
| `/api/stock/<symbol>/history` | GET | Price history | `/api/stock/VNM/history?days=30` |
| `/api/market/<market>` | GET | Market summary | `/api/market/HOSE` |

---

## 🎯 Example Google AI Studio Prompts

**Prompt 1: Stock Assistant**
```
You are a Vietnamese stock market assistant with access to real-time data.
When users ask about stocks, call get_stock_price() to get current prices.

User: What's VNM trading at?
AI: [Calls get_stock_price("VNM")] VNM is currently at 67,800 VND, up 0.15%.
```

**Prompt 2: Portfolio Tracker**
```
Help users track their Vietnamese stock portfolio.
Use get_stock_price() for individual stocks and get_stocks() for portfolios.

User: Check my portfolio: VNM, VIC, VHM
AI: [Calls get_stocks(["VNM", "VIC", "VHM"])]
Your portfolio:
- VNM: 67,800 VND (+0.15%)
- VIC: 42,500 VND (-1.16%)
- VHM: 65,000 VND (+1.56%)
```

**Prompt 3: Market Analyst**
```
Analyze Vietnamese stock trends using get_history() and get_market_summary().
Provide insights on price movements and market conditions.

User: How has VNM performed this month?
AI: [Calls get_history("VNM", 30)] VNM has shown...
```

---

## 🌐 Deploy to Production

### Option 1: Railway (Easiest)
```bash
# Install Railway CLI
npm install -g @railway/cli

# Deploy
railway login
railway init
railway up
```

### Option 2: Heroku
```bash
# Create Procfile
echo "web: python api_server.py" > Procfile

# Deploy
heroku create
git push heroku main
```

### Option 3: Google Cloud Run
```bash
gcloud run deploy stock-api \
  --source . \
  --platform managed \
  --region asia-southeast1
```

After deploying, update the `API_BASE_URL` in your code to the production URL.

---

## 🔐 Add API Authentication (Optional)

Update `api_server.py`:

```python
import os
from functools import wraps

API_KEY = os.getenv('API_KEY', 'your-secret-key')

def require_api_key(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        key = request.headers.get('X-API-Key')
        if key != API_KEY:
            return jsonify({'error': 'Unauthorized'}), 401
        return f(*args, **kwargs)
    return decorated

# Apply to endpoints
@app.route('/api/stock/<symbol>')
@require_api_key
def get_stock_price(symbol):
    # ... existing code
```

Then in your app:
```javascript
fetch(`${API_URL}/api/stock/VNM`, {
  headers: {
    'X-API-Key': 'your-secret-key'
  }
})
```

---

## 📱 Complete Example App

See `example_ai_app.html` for a complete working example with:
- Real-time stock prices
- Multiple stock queries
- Price history charts
- Market summaries
- Beautiful UI

Just open it in a browser while the API server is running!

---

## 🎓 Summary

**What you have:**
- ✅ REST API exposing stock database
- ✅ Multiple endpoints for different queries
- ✅ Ready for Google AI Studio integration
- ✅ Example app showing how to use it

**What your Google AI Studio app can do:**
- Get real-time Vietnamese stock prices
- Track portfolios
- Analyze price history
- Monitor market trends
- All with NO rate limits! 🎉

**Next steps:**
1. Start the API server
2. Test with example_ai_app.html
3. Integrate into Google AI Studio
4. Deploy to production
5. Build amazing stock market features!

Happy coding! 🚀
