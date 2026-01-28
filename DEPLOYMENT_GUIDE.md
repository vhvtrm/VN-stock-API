# Deploy to Cloud - Step by Step

## Why Deploy?

Your API runs on `localhost:5001` - only accessible on YOUR computer.
Google AI Studio needs a public URL like: `https://your-api.railway.app`

## Option 1: Railway (Recommended - FREE & Easy)

### Step 1: Install Railway CLI
```bash
npm install -g @railway/cli
```

Or visit: https://railway.app and sign up

### Step 2: Initialize Git (if not already)
```bash
cd "/Users/vietvu/Coding/Getting market price"
git init
git add .
git commit -m "Initial commit - Vietnamese Stock API"
```

### Step 3: Deploy to Railway
```bash
# Login to Railway
railway login

# Create new project
railway init

# Add environment variables in Railway dashboard:
# Go to: railway.app -> your project -> Variables
# Add: DC_DB_STRING = "DRIVER={ODBC Driver 18 for SQL Server};SERVER=tcp:sqls-dclab.database.windows.net,1433;DATABASE=dclab;UID=dclab_readonly;PWD=DHS#@vGESADdf!;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"

# Deploy
railway up
```

### Step 4: Get Your Public URL
```bash
railway domain
# This will give you: https://your-app-name.railway.app
```

---

## Option 2: Render (Also FREE & Easy)

### Step 1: Create account at render.com

### Step 2: Create New Web Service
- Connect your GitHub repo
- OR upload your code

### Step 3: Configure
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `python api_server_real.py`

### Step 4: Add Environment Variables
In Render dashboard, add:
```
DC_DB_STRING=DRIVER={ODBC Driver 18 for SQL Server};SERVER=tcp:sqls-dclab.database.windows.net,1433;DATABASE=dclab;UID=dclab_readonly;PWD=DHS#@vGESADdf!;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;
ODBCSYSINI=/opt/render/project/src
```

### Step 5: Deploy
Click "Create Web Service" - Render will deploy automatically!

---

## Option 3: Use Ngrok (Quick Test - Not for Production)

**For quick testing only:**

```bash
# Install ngrok
brew install ngrok

# Create account at ngrok.com and get auth token
ngrok config add-authtoken YOUR_TOKEN

# Expose your local API
ngrok http 5001
```

This gives you a temporary public URL like: `https://abc123.ngrok.io`

⚠️ **Note**: Ngrok URLs change every restart - not for production!

---

## After Deployment

Once deployed, you'll have a public URL like:
- Railway: `https://vietnamese-stock-api.railway.app`
- Render: `https://vietnamese-stock-api.onrender.com`
- Ngrok: `https://abc123.ngrok.io`

**Test it:**
```bash
curl https://YOUR-URL/api/health
curl https://YOUR-URL/api/stock/VNM
```

**Then use this URL in Google AI Studio!**

---

## Next: Integrate with Google AI Studio

Once you have your public URL, proceed to the next step to integrate it with your Google AI Studio app.
