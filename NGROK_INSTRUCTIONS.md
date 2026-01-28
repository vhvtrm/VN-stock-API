# Ngrok Setup - Step by Step

## ✅ Status Check

- [x] Ngrok installed
- [x] API server running
- [x] Real data working
- [ ] Ngrok authtoken configured
- [ ] Ngrok tunnel started

---

## 📋 Instructions

### Step 1: Configure Ngrok (One-time setup)

The ngrok dashboard should be open in your browser at:
https://dashboard.ngrok.com/get-started/your-authtoken

**Do this:**

1. Sign up/login to ngrok (it's free!)
2. Copy your authtoken (long string like: `2abc...XYZ`)
3. Run this command with YOUR token:

```bash
ngrok config add-authtoken YOUR_TOKEN_HERE
```

Example:
```bash
ngrok config add-authtoken 2abcdef1234567890XYZ
```

---

### Step 2: Start Ngrok Tunnel

Once you've configured the token, run:

```bash
cd "/Users/vietvu/Coding/Getting market price"
./start_ngrok.sh
```

**You'll see something like:**

```
ngrok

Session Status                online
Account                       Your Name (Plan: Free)
Version                       3.x.x
Region                        United States (us)
Latency                       20ms
Web Interface                 http://127.0.0.1:4040
Forwarding                    https://abc-123-xyz.ngrok.io -> http://localhost:5001

Connections                   ttl     opn     rt1     rt5     p50     p90
                              0       0       0.00    0.00    0.00    0.00
```

**Copy the Forwarding URL:** `https://abc-123-xyz.ngrok.io`

⚠️ **Keep this terminal open!** If you close it, the tunnel stops.

---

### Step 3: Test Your Public URL

Open a NEW terminal and test:

```bash
# Replace with your actual ngrok URL
curl https://YOUR-NGROK-URL.ngrok.io/api/health

# Should return:
# {"status":"ok","message":"Vietnamese Stock Price API is running (REAL DATA)"}
```

Test stock price:
```bash
curl https://YOUR-NGROK-URL.ngrok.io/api/stock/VNM
```

---

### Step 4: Use in Google AI Studio

Copy this code and paste it in your Google AI Studio app.
**Replace `YOUR_NGROK_URL` with your actual URL:**

```javascript
// ========================================
// CONFIGURATION - REPLACE THIS URL!
// ========================================
const API_URL = 'https://YOUR-NGROK-URL.ngrok.io/api';

// ========================================
// FUNCTIONS
// ========================================

// Get single stock price
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
        open: data.data.open,
        high: data.data.high,
        low: data.data.low,
        volume: data.data.volume,
        date: data.data.date
      };
    }
    return null;
  } catch (error) {
    console.error('Error fetching stock:', error);
    return null;
  }
}

// Get multiple stocks
async function getMultipleStocks(symbols) {
  try {
    const response = await fetch(`${API_URL}/stocks`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ symbols: symbols })
    });
    const data = await response.json();

    if (data.success) {
      return data.data;
    }
    return null;
  } catch (error) {
    console.error('Error fetching stocks:', error);
    return null;
  }
}

// ========================================
// USAGE EXAMPLES
// ========================================

// Example 1: Get VNM price
const vnm = await getStockPrice('VNM');
if (vnm) {
  console.log(`${vnm.symbol}: ${vnm.price} VND (${vnm.pct_change}%)`);
}

// Example 2: Get multiple stocks
const stocks = await getMultipleStocks(['VNM', 'VIC', 'VHM']);
if (stocks) {
  for (const [symbol, data] of Object.entries(stocks)) {
    if (data) {
      console.log(`${symbol}: ${data.price} VND`);
    }
  }
}

// Example 3: Display in UI
async function displayStock(symbol) {
  const stock = await getStockPrice(symbol);
  if (stock) {
    return `
      <div>
        <h2>${stock.symbol}</h2>
        <p>Price: ${stock.price.toLocaleString()} VND</p>
        <p>Change: ${stock.change > 0 ? '+' : ''}${stock.pct_change}%</p>
        <p>Volume: ${stock.volume.toLocaleString()}</p>
      </div>
    `;
  }
}
```

---

### Step 5: Test in Your Google AI Studio App

Try these queries:

1. **"What's the price of VNM?"**
   - Should return: Real VNM price

2. **"Show me VIC and VHM"**
   - Should return: Both stocks with real prices

3. **"How is VNM performing today?"**
   - Should return: VNM with change percentage

---

## 🎯 Quick Reference

### Your Setup:
- **Local API**: http://localhost:5001
- **Public URL**: https://YOUR-NGROK-URL.ngrok.io
- **API Endpoints**:
  - Health: `/api/health`
  - Single stock: `/api/stock/{SYMBOL}`
  - Multiple stocks: `/api/stocks` (POST)
  - History: `/api/stock/{SYMBOL}/history?days=7`

---

## ⚠️ Important Notes

1. **Keep terminal open**: If you close the ngrok terminal, the tunnel stops
2. **URL changes on restart**: Each time you restart ngrok, you get a new URL
3. **Free tier limits**: 40 requests/minute, 1 tunnel at a time
4. **For production**: Deploy to Railway instead (permanent URL)

---

## 🐛 Troubleshooting

### "ngrok config add-authtoken" not working
**Solution:** Make sure you copied the full token from ngrok dashboard

### Can't access ngrok URL
**Solution:**
- Check ngrok terminal is still running
- Check API server is running: `ps aux | grep api_server_real`
- Test local first: `curl http://localhost:5001/api/health`

### CORS errors
**Solution:** Already fixed! Flask-CORS is enabled

### "Failed to fetch" in Google AI Studio
**Solution:**
- Make sure you replaced `YOUR_NGROK_URL` with actual URL
- Test in browser console first
- Check ngrok is still running

---

## 🎉 Success Checklist

- [ ] Ngrok authtoken configured
- [ ] Ngrok tunnel running
- [ ] Got public URL (e.g., https://abc123.ngrok.io)
- [ ] Tested URL with curl (both health and stock endpoints)
- [ ] Copied JavaScript code to Google AI Studio
- [ ] Replaced API_URL with actual ngrok URL
- [ ] Tested queries in Google AI Studio
- [ ] Getting real Vietnamese stock prices!

---

**You're almost there! Just configure the ngrok token and run the script!** 🚀
