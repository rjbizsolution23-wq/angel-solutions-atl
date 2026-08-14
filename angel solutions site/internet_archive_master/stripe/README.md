# Stripe Supreme Agent

![KaliVibeCoding](https://img.shields.io/badge/Built%20by-KaliVibeCoding-FF69B4?style=for-the-badge)
![Gemini Pro](https://img.shields.io/badge/Powered%20by-Gemini%20Pro-87CEEB?style=for-the-badge)

**Autonomous AI agent for complete Stripe automation and management.**

## 🚀 Features

- 🤖 **AI-Powered Agent**: Natural language interface powered by Gemini Pro
- 💳 **Complete Stripe Integration**: Payments, Subscriptions, Connect, Products, and more
- 🎨 **Beautiful UI**: California Neon-Noir themed dashboard
- 🔒 **Test/Live Mode**: Safe development with easy mode switching
- 📊 **Real-time Data**: Live Stripe account data visualization
- 🔔 **Webhook Handling**: Automatic webhook processing and storage
- 📝 **Audit Trail**: Complete log of all agent actions

## 🛠️ Tech Stack

- **Frontend**: Next.js 14 (App Router), Tailwind CSS, TypeScript
- **Backend**: FastAPI (Python), LangChain, Gemini Pro
- **Database**: Supabase (PostgreSQL)
- **AI**: Google Gemini Pro via LangChain
- **Payments**: Stripe SDK

## 📋 Prerequisites

- Node.js 18+
- Python 3.9+
- Supabase account
- Stripe account (test and/or live keys)
- Google AI API key (for Gemini Pro)

## 🏃 Quick Start

### 1. Clone and Setup

\`\`\`bash
cd stripe-supreme-agent
cp .env.example .env
# Edit .env with your API keys
\`\`\`

### 2. Setup Supabase Database

\`\`\`bash
# Run the schema in your Supabase SQL editor
cat backend/db/schema.sql
\`\`\`

### 3. Start Backend

\`\`\`bash
cd backend
pip install -r requirements.txt
python -m uvicorn main:app --reload
\`\`\`

Backend will run on http://localhost:8000

### 4. Start Frontend

\`\`\`bash
cd frontend
npm install
npm run dev
\`\`\`

Frontend will run on http://localhost:3000

## 🎯 Agent Capabilities

The Stripe Supreme Agent can handle:

### Payments
- Create payment intents
- Process refunds
- Generate checkout sessions
- Create payment links

### Products & Pricing
- Create products and prices
- Manage coupons and promotions
- List all products

### Customers & Subscriptions
- Create and manage customers
- Create subscriptions with trials
- Cancel subscriptions
- List all subscriptions

### Connect (Marketplaces)
- Create Connect accounts
- Generate onboarding links
- Process transfers to connected accounts

### Reporting
- Check account balance
- View recent transactions
- Monitor webhook events

## 💬 Example Commands

Try asking the agent:

- "Create a payment for $50"
- "Set up a monthly subscription for $99 with a 7-day trial"
- "Show me my account balance"
- "Create a product called 'Premium Plan'"
- "List all my customers"
- "Help me set up a marketplace with Connect"

## 🔐 Environment Variables

\`\`\`env
# Stripe
STRIPE_SECRET_KEY_TEST=sk_test_...
STRIPE_SECRET_KEY_LIVE=sk_live_...
STRIPE_PUBLISHABLE_KEY_TEST=pk_test_...
STRIPE_PUBLISHABLE_KEY_LIVE=pk_live_...
STRIPE_WEBHOOK_SECRET=whsec_...

# Google AI
GOOGLE_AI_API_KEY=AIzaSy...

# Supabase
SUPABASE_URL=https://...
SUPABASE_ANON_KEY=eyJ...
SUPABASE_SERVICE_KEY=eyJ...

# App Config
ENVIRONMENT=development
STRIPE_MODE=test
FRONTEND_URL=http://localhost:3000
BACKEND_URL=http://localhost:8000
\`\`\`

## 📡 API Endpoints

### Agent
- `POST /api/agent/chat` - Chat with the agent
- `GET /api/agent/conversations/{id}/messages` - Get conversation history
- `GET /api/agent/actions` - Get action audit log

### Stripe Data
- `GET /api/stripe/balance` - Get account balance
- `GET /api/stripe/customers` - List customers
- `GET /api/stripe/products` - List products
- `GET /api/stripe/subscriptions` - List subscriptions
- `GET /api/stripe/transactions` - List transactions

### Webhooks
- `POST /api/webhooks/stripe` - Stripe webhook endpoint
- `GET /api/webhooks/events` - Get webhook event history

## 🚀 Deployment

### Backend (Google Cloud Run)

\`\`\`bash
cd backend
gcloud run deploy stripe-agent-backend \\
  --source . \\
  --region us-central1 \\
  --allow-unauthenticated
\`\`\`

### Frontend (Vercel)

\`\`\`bash
cd frontend
vercel --prod
\`\`\`

## 🔧 Development

### Backend Structure

\`\`\`
backend/
├── main.py                 # FastAPI app
├── core/
│   ├── config.py          # Settings
│   ├── stripe_client.py   # Stripe SDK wrapper
│   └── agent_engine.py    # AI agent
├── tools/                 # LangChain tools
├── api/routes/           # API endpoints
└── services/             # External services
\`\`\`

### Frontend Structure

\`\`\`
frontend/
├── app/
│   ├── layout.tsx        # Root layout
│   ├── page.tsx          # Main dashboard
│   └── globals.css       # Global styles
└── components/
    ├── AgentChat.tsx     # Chat interface
    └── StripeDataCards.tsx # Data visualization
\`\`\`

## 📝 License

Built with 💜 by **KaliVibeCoding**

## 🤝 Support

For questions or custom builds:
- 📞 Call/Text: 945-308-8003
- 📧 Email: info@kalivibecoding.com

---

**Supreme Build Agent** • Powered by Gemini Pro • KaliVibeCoding Standard
