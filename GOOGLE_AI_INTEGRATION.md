# Google AI Studio Integration - Step by Step

## 🎯 Quick Overview

**What you need to do:**
1. Deploy your API to the cloud (get a public URL)
2. Add the URL to your Google AI Studio app
3. Make API calls from your app

---

## Step 1: Deploy API to Cloud (Choose ONE)

### Option A: Railway (Easiest - 5 min)

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Initialize project
cd "/Users/vietvu/Coding/Getting market price"
railway init

# Deploy
railway up

# Get your URL
railway domain
```

**Then add environment variable in Railway dashboard:**
- Go to railway.app → Your Project → Variables
- Add: `DC_DB_STRING` = (your connection string from .env file)

### Option B: Ngrok (Quick Test - 2 min)

```bash
# Install
brew install ngrok

# Get auth token from ngrok.com
ngrok config add-authtoken YOUR_TOKEN

# Expose your local API
ngrok http 5001
```

You'll get a URL like: `https://abc123.ngrok.io`

---

## Step 2: Test Your Public URL

```bash
# Replace with your actual URL
curl https://YOUR-URL/api/health
curl https://YOUR-URL/api/stock/VNM
```

---

## Step 3: Integrate with Google AI Studio

### Method A: If Using Google AI Studio Function Calling

**In your Google AI Studio project, add this JavaScript:**

```javascript
// YOUR DEPLOYED API URL HERE
const API_URL = 'https://your-api-url-here.railway.app/api';

// Function to get stock price
async function getStockPrice(symbol) {
  try {
    const response = await fetch(`${API_URL}/stock/${symbol}`);
    const data = await response.json();

    if (data.success) {
      return `${data.data.symbol}: ${data.data.price} VND (${data.data.change >= 0 ? '+' : ''}${data.data.pct_change}%)`;
    }
    return `Error: ${data.error}`;
  } catch (error) {
    return `Error: ${error.message}`;
  }
}

// Function to get multiple stocks
async function getMultipleStocks(symbols) {
  try {
    const response = await fetch(`${API_URL}/stocks`, {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({symbols: symbols})
    });

    const data = await response.json();

    if (data.success) {
      let result = '';
      for (const [symbol, info] of Object.entries(data.data)) {
        if (info) {
          result += `${symbol}: ${info.price} VND (${info.change >= 0 ? '+' : ''}${info.pct_change}%)\n`;
        }
      }
      return result;
    }
    return `Error: ${data.error}`;
  } catch (error) {
    return `Error: ${error.message}`;
  }
}
```

### Method B: If Building a Custom Web App

**In your HTML/JavaScript:**

```html
<!DOCTYPE html>
<html>
<head>
    <title>Vietnamese Stock Assistant</title>
</head>
<body>
    <h1>Vietnamese Stock Prices</h1>

    <input type="text" id="symbol" placeholder="Enter stock (e.g., VNM)">
    <button onclick="getPrice()">Get Price</button>

    <div id="result"></div>

    <script>
        // YOUR DEPLOYED API URL HERE
        const API_URL = 'https://your-api-url-here/api';

        async function getPrice() {
            const symbol = document.getElementById('symbol').value;
            const response = await fetch(`${API_URL}/stock/${symbol}`);
            const data = await response.json();

            if (data.success) {
                const stock = data.data;
                document.getElementById('result').innerHTML = `
                    <h2>${stock.symbol}</h2>
                    <p>Price: ${stock.price} VND</p>
                    <p>Change: ${stock.change} (${stock.pct_change}%)</p>
                    <p>Volume: ${stock.volume.toLocaleString()}</p>
                `;
            }
        }
    </script>
</body>
</html>
```

---

## Step 4: Test Integration

**Test queries in your Google AI Studio app:**

1. "What's the price of VNM?"
2. "Show me VIC and VHM prices"
3. "How is VNM performing today?"

---

## Complete Example API Calls

```javascript
// Get single stock
fetch('https://your-api.railway.app/api/stock/VNM')
  .then(res => res.json())
  .then(data => console.log(data.data.price));

// Get multiple stocks
fetch('https://your-api.railway.app/api/stocks', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({symbols: ['VNM', 'VIC', 'VHM']})
})
  .then(res => res.json())
  .then(data => console.log(data.data));

// Get history
fetch('https://your-api.railway.app/api/stock/VNM/history?days=7')
  .then(res => res.json())
  .then(data => console.log(data.data));
```

---

## 🎯 Summary

1. **Deploy API** → Get public URL (Railway/Ngrok)
2. **Copy URL** → Replace `API_URL` in your code
3. **Test** → Make API calls from Google AI Studio
4. **Done!** → Your app now has real Vietnamese stock prices

---

## Troubleshooting

**Problem:** Can't access API
**Solution:** Make sure API is deployed and URL is correct

**Problem:** CORS error
**Solution:** Already fixed! Flask-CORS is enabled

**Problem:** No data returned
**Solution:** Check if stock symbol exists (try VNM, VIC, VHM first)

---

**Need help?** Check the example in `example_ai_app.html` - it shows exactly how to call the API!
