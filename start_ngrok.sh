#!/bin/bash

# Vietnamese Stock API - Ngrok Setup
echo "======================================================"
echo "Vietnamese Stock API - Ngrok Tunnel"
echo "======================================================"
echo ""

# Check if API is running
if ! pgrep -f "api_server_real.py" > /dev/null; then
    echo "❌ API server not running!"
    echo "Starting API server..."
    cd "/Users/vietvu/Coding/Getting market price"
    python api_server_real.py > server_real.log 2>&1 &
    sleep 3
    echo "✅ API server started"
fi

echo "✅ API server is running on localhost:5001"
echo ""

# Start ngrok
echo "Starting ngrok tunnel..."
echo "⚠️  Keep this terminal window open!"
echo ""
echo "======================================================"

ngrok http 5001 --log=stdout

echo ""
echo "Ngrok stopped."
