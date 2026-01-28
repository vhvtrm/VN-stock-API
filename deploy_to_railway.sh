#!/bin/bash

# Vietnamese Stock API - Railway Deployment Script
echo "========================================================"
echo "Railway Deployment for Vietnamese Stock API"
echo "========================================================"
echo ""

# Step 1: Login
echo "Step 1: Login to Railway"
echo "This will open a browser window for authentication..."
railway login

if [ $? -ne 0 ]; then
    echo "❌ Login failed. Please try again."
    exit 1
fi

echo "✅ Login successful"
echo ""

# Step 2: Initialize Railway project
echo "Step 2: Initialize Railway project"
railway init

if [ $? -ne 0 ]; then
    echo "❌ Project initialization failed."
    exit 1
fi

echo "✅ Project initialized"
echo ""

# Step 3: Add environment variable
echo "Step 3: Add database connection string"
echo "Adding DC_DB_STRING variable..."

# Read from .env file
DB_STRING=$(grep "^DC_DB_STRING=" .env | cut -d'"' -f2)

railway variables --set DC_DB_STRING="$DB_STRING"

if [ $? -ne 0 ]; then
    echo "⚠️  Could not add variable automatically."
    echo "Please add it manually in Railway dashboard:"
    echo ""
    echo "Variable name: DC_DB_STRING"
    echo "Variable value: $DB_STRING"
    echo ""
fi

echo ""

# Step 4: Deploy
echo "Step 4: Deploy to Railway"
echo "Deploying your API..."
railway up

if [ $? -ne 0 ]; then
    echo "❌ Deployment failed."
    exit 1
fi

echo "✅ Deployment successful!"
echo ""

# Step 5: Generate domain
echo "Step 5: Generate public domain"
railway domain

echo ""
echo "========================================================"
echo "Deployment Complete!"
echo "========================================================"
echo ""
echo "Next steps:"
echo "1. Go to https://railway.app"
echo "2. Find your project and get the public URL"
echo "3. Test: curl https://YOUR-URL.railway.app/api/health"
echo "4. Update your Google AI Studio code with the new URL"
echo ""
