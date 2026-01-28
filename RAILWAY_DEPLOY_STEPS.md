# Railway Deployment - Step by Step

## Quick Deploy (Recommended)

Open a **new terminal window** and run:

```bash
cd "/Users/vietvu/Coding/Getting market price"
./deploy_to_railway.sh
```

This script will:
1. Login to Railway (opens browser)
2. Create a new project
3. Add your database credentials
4. Deploy your API
5. Generate a public URL

---

## Manual Deploy (Alternative)

If you prefer to run commands manually:

### Step 1: Login

```bash
cd "/Users/vietvu/Coding/Getting market price"
railway login
```

This will open a browser. Login with GitHub or email.

### Step 2: Initialize Project

```bash
railway init
```

Choose:
- Create a new project
- Give it a name (e.g., "vietnamese-stock-api")

### Step 3: Add Environment Variable

```bash
railway variables --set DC_DB_STRING="DRIVER={ODBC Driver 18 for SQL Server};SERVER=tcp:sqls-dclab.database.windows.net,1433;DATABASE=dclab;UID=dclab_readonly;PWD=DHS#@vGESADdf!;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"
```

### Step 4: Deploy

```bash
railway up
```

Wait for deployment to complete (usually 2-3 minutes).

### Step 5: Generate Domain

```bash
railway domain
```

This creates a public URL for your API.

### Step 6: Get Your URL

```bash
railway status
```

Or visit: https://railway.app and find your project.

---

## After Deployment

### Test Your Railway URL

Once deployed, you'll get a URL like: `https://vietnamese-stock-api-production.up.railway.app`

Test it:

```bash
# Health check
curl https://YOUR-URL.railway.app/api/health

# Stock price
curl https://YOUR-URL.railway.app/api/stock/VNM
```

### Update Google AI Studio

Replace your ngrok URL with the Railway URL:

```javascript
// OLD (ngrok - temporary)
const API_URL = 'https://telegrammic-libbie-invulnerably.ngrok-free.dev/api';

// NEW (Railway - permanent)
const API_URL = 'https://YOUR-PROJECT-NAME.up.railway.app/api';
```

---

## Troubleshooting

### "Cannot find railway command"
```bash
npm install -g @railway/cli
```

### "Login failed"
- Make sure you have a Railway account at https://railway.app
- Try the web browser login instead

### "Deployment failed"
- Check Railway dashboard for logs
- Make sure requirements.txt is correct
- Verify environment variable is set

### "Database connection error"
- Go to Railway dashboard → Your project → Variables
- Make sure `DC_DB_STRING` is set correctly
- Check the value matches your .env file

---

## Railway Dashboard

View your project at: https://railway.app

You can:
- See deployment logs
- Monitor usage
- Manage environment variables
- View domains
- Check errors

---

## Advantages of Railway vs Ngrok

| Feature | Ngrok | Railway |
|---------|-------|---------|
| URL | Changes on restart | Permanent |
| Uptime | Only when your Mac is on | Always online |
| Speed | Depends on your internet | Fast CDN |
| SSL | Automatic | Automatic |
| Cost | Free tier | Free tier |
| Best for | Testing | Production |

---

**Ready to deploy? Open a new terminal and run:**

```bash
cd "/Users/vietvu/Coding/Getting market price"
./deploy_to_railway.sh
```

🚀 Your API will be live in minutes!
