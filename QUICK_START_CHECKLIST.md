# Quick Start Checklist - Get Real Prices in Google AI Studio

## ✅ Step-by-Step (Choose Your Path)

---

### PATH A: Quick Test with Ngrok (2 minutes)

**Best for:** Testing immediately without deployment

```bash
# 1. Install ngrok
brew install ngrok

# 2. Get free auth token from ngrok.com (sign up)
ngrok config add-authtoken YOUR_TOKEN_FROM_NGROK

# 3. Expose your local API (keep terminal open!)
ngrok http 5001
```

**You'll see:**
```
Forwarding  https://abc123-xyz.ngrok.io -> http://localhost:5001
```

**Copy that URL** (e.g., `https://abc123-xyz.ngrok.io`)

**4. Use in Google AI Studio:**

```javascript
const API_URL = 'https://abc123-xyz.ngrok.io/api';

async function getStockPrice(symbol) {
  const response = await fetch(`${API_URL}/stock/${symbol}`);
  const data = await response.json();
  return data.data;
}

// Test it
const vnm = await getStockPrice('VNM');
console.log(vnm); // Real price!
```

⚠️ **Note:** Ngrok URL changes every restart - good for testing only!

---

### PATH B: Deploy to Railway (10 minutes)

**Best for:** Production use, permanent URL

```bash
# 1. Install Railway CLI
npm install -g @railway/cli

# 2. Login to Railway
railway login

# 3. Go to your project folder
cd "/Users/vietvu/Coding/Getting market price"

# 4. Initialize git (if not done)
git init
git add .
git commit -m "Vietnamese Stock API"

# 5. Create Railway project
railway init

# 6. Deploy!
railway up
```

**7. Add environment variable:**
- Go to: https://railway.app
- Click your project
- Go to "Variables" tab
- Click "New Variable"
- Name: `DC_DB_STRING`
- Value: (copy from your .env file)
- Save!

**8. Get your permanent URL:**
```bash
railway domain
```

You'll get: `https://your-project-name.railway.app`

**9. Use in Google AI Studio:**
```javascript
const API_URL = 'https://your-project-name.railway.app/api';
```

✅ **This URL never changes!**

---

## 📝 Copy-Paste Code for Google AI Studio

**Replace `YOUR_API_URL` with your actual URL:**

```javascript
// ===== CONFIGURATION =====
const API_URL = 'YOUR_API_URL/api'; // e.g., https://abc123.ngrok.io/api

// ===== FUNCTIONS =====
async function getStockPrice(symbol) {
  try {
    const response = await fetch(`${API_URL}/stock/${symbol}`);
    const data = await response.json();

    if (data.success) {
      return {
        symbol: data.data.symbol,
        price: data.data.price,
        change: data.data.change,
        pct_change: data.data.pct_change,
        volume: data.data.volume,
        date: data.data.date
      };
    }
    return null;
  } catch (error) {
    console.error('Error:', error);
    return null;
  }
}

async function getMultipleStocks(symbols) {
  try {
    const response = await fetch(`${API_URL}/stocks`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ symbols: symbols })
    });
    const data = await response.json();
    return data.success ? data.data : null;
  } catch (error) {
    console.error('Error:', error);
    return null;
  }
}

// ===== USAGE EXAMPLES =====
// Single stock
const vnm = await getStockPrice('VNM');
console.log(`VNM: ${vnm.price} VND (${vnm.pct_change}%)`);

// Multiple stocks
const stocks = await getMultipleStocks(['VNM', 'VIC', 'VHM']);
for (const [symbol, data] of Object.entries(stocks)) {
  if (data) {
    console.log(`${symbol}: ${data.price} VND`);
  }
}
```

---

## 🧪 Test Your Integration

**1. Test health endpoint:**
```javascript
fetch('YOUR_API_URL/api/health')
  .then(res => res.json())
  .then(data => console.log(data));
```

Should return: `{status: "ok", message: "...REAL DATA..."}`

**2. Test stock price:**
```javascript
fetch('YOUR_API_URL/api/stock/VNM')
  .then(res => res.json())
  .then(data => console.log(data.data.price));
```

Should return: Real VNM price (e.g., 68900)

---

## 🎯 Which Path Should You Choose?

| Feature | Ngrok (Quick Test) | Railway (Production) |
|---------|-------------------|---------------------|
| Setup Time | 2 minutes | 10 minutes |
| URL Stability | Changes on restart | Permanent |
| Best For | Testing | Production app |
| Cost | Free | Free (with limits) |
| Recommendation | Start here! | Deploy here after testing |

---

## 📋 Final Checklist

Before using in Google AI Studio:

- [ ] API is running (locally or deployed)
- [ ] You have a public URL (ngrok or Railway)
- [ ] Test URL works: `curl YOUR_URL/api/health`
- [ ] Test stock endpoint: `curl YOUR_URL/api/stock/VNM`
- [ ] Copied the JavaScript code above
- [ ] Replaced `YOUR_API_URL` with actual URL
- [ ] Tested in browser console first
- [ ] Added to Google AI Studio app

---

## 🆘 Need Help?

**Common issues:**

1. **"Failed to fetch"**
   - Check API is running: `curl YOUR_URL/api/health`
   - Check URL is correct (don't forget `/api`)

2. **"CORS error"**
   - Already fixed! Flask-CORS is enabled

3. **"No data"**
   - Try these stocks first: VNM, VIC, VHM (they definitely exist)

4. **Ngrok URL not working**
   - Make sure local API is still running: `ps aux | grep api_server_real`
   - Ngrok terminal must stay open!

---

**🎉 You're ready to go! Choose a path and start getting real Vietnamese stock prices in your Google AI Studio app!**
