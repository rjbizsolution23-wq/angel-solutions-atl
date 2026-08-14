#!/bin/bash

# Stripe Supreme Agent - Quick Start Script
# KaliVibeCoding Build

echo "🚀 Starting Stripe Supreme Agent..."
echo ""

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "⚠️  No .env file found. Copying from .env.example..."
    cp .env.example .env
    echo "✅ Created .env file. Please edit it with your API keys before proceeding."
    exit 1
fi

echo "📊 Step 1: Setting up Supabase database..."
echo "Please run the SQL schema from backend/db/schema.sql in your Supabase SQL Editor"
echo "Press Enter when done..."
read

echo ""
echo "🔧 Step 2: Starting Backend (FastAPI)..."
cd backend
python -m uvicorn main:app --reload --port 8000 &
BACKEND_PID=$!
echo "✅ Backend started on http://localhost:8000 (PID: $BACKEND_PID)"

echo ""
echo "🎨 Step 3: Starting Frontend (Next.js)..."
cd ../frontend
npm run dev &
FRONTEND_PID=$!
echo "✅ Frontend starting on http://localhost:3000 (PID: $FRONTEND_PID)"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🎉 Stripe Supreme Agent is LIVE!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📍 Frontend: http://localhost:3000"
echo "📍 Backend API: http://localhost:8000"
echo "📍 API Docs: http://localhost:8000/docs"
echo ""
echo "💡 Try asking the agent:"
echo "   - 'Create a payment for $50'"
echo "   - 'Show me my account balance'"
echo "   - 'Set up a monthly subscription for $99'"
echo ""
echo "Press Ctrl+C to stop all services"
echo ""

# Wait for Ctrl+C
trap "kill $BACKEND_PID $FRONTEND_PID; exit" INT
wait
