# 🔥 Prometheus Archive Engine v2.0

**The Ultimate Internet Archive Monetization Platform**

Transform Internet Archive content into premium digital products with AI-powered automation.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.136-green.svg)](https://fastapi.tiangolo.com)

---

## 🎯 What It Does

Prometheus Archive Engine is an AI-powered system that:

1. **Discovers** content on Internet Archive (books, games, software, APKs)
2. **Transforms** it with AI enhancement (update, rebrand, improve)
3. **Packages** it into professional bundles and courses
4. **Monetizes** it automatically with Stripe integration
5. **Scales** infinitely with multi-agent orchestration

### Natural Language Interface

```python
# Just tell it what you want!
"Find 10 programming books from the 1990s, update them with modern 
frameworks, rebrand with my company logo, and create a course bundle"

"Download all NES Mario games with emulators and create a 
'Classic Nintendo Collection' I can sell"

"Get top 50 productivity software for Windows 95, package with DOSBox,
and set up automated delivery"
```

---

## ⚡ Quick Start

### Prerequisites
- Python 3.12+
- PostgreSQL 18+
- Redis 7+
- Internet Archive account ([sign up](https://archive.org/account/signup))
- Anthropic API key ([get key](https://console.anthropic.com/))
- Stripe account ([sign up](https://stripe.com))

### Installation

```bash
# Clone repository
git clone https://github.com/rjbizsolution23-wq/prometheus-archive-engine.git
cd prometheus-archive-engine

# Create virtual environment
python3.12 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
cd backend
pip install -r requirements.txt

# Setup database
createdb prometheus_archive
python ../scripts/setup_db.py

# Configure environment
cp .env.example .env
# Edit .env with your API keys
```

### Configuration

Create `.env` file:

```env
# Internet Archive
IA_ACCESS_KEY=your_ia_access_key
IA_SECRET_KEY=your_ia_secret_key

# AI Models
ANTHROPIC_API_KEY=your_anthropic_key
OPENAI_API_KEY=your_openai_key  # Optional

# Database
DATABASE_URL=postgresql://user:pass@localhost/prometheus_archive

# Redis
REDIS_URL=redis://localhost:6379

# Stripe
STRIPE_API_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...

# Application
SECRET_KEY=your-secret-key-here
ENVIRONMENT=development
```

### Run the Application

```bash
# Start FastAPI server
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000

# Start Celery worker (separate terminal)
celery -A tasks.celery_app worker --loglevel=info

# Access API documentation
open http://localhost:8000/docs
```

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────┐
│    Master Orchestrator (Natural Language)   │
│         Claude Opus 4.7 + LangGraph          │
└─────────────────────────────────────────────┘
               ▼          ▼          ▼
    ┌──────────────┬──────────────┬──────────────┐
    │ Book         │ Game         │ Software     │
    │ Rebrander    │ Emulator     │ Manager      │
    └──────────────┴──────────────┴──────────────┘
               ▼          ▼          ▼
    ┌──────────────────────────────────────────┐
    │     Internet Archive API Client          │
    │  Search • Download • Upload • Metadata   │
    └──────────────────────────────────────────┘
```

### Key Components

- **Master Orchestrator** - Natural language interface using LangGraph
- **Book Rebrander Agent** - AI-powered book enhancement and rebranding
- **Game Emulator Agent** - Retro game collection and emulator packaging
- **Software Manager Agent** - Software discovery and bundling
- **APK Manager Agent** - Android app management
- **Collection Builder** - Bundle creation and packaging
- **Course Generator** - Educational content creation
- **Monetization Agent** - Stripe integration and automated delivery

---

## 📚 Usage Examples

### 1. Book Rebranding

```python
from agents.book_rebrander import BookRebranderAgent
import internetarchive as ia

agent = BookRebranderAgent(
    ia_client=ia,
    anthropic_api_key="your-key"
)

# Search for books
books = await agent.search_books(
    query="python programming",
    year_range=(1995, 2000),
    max_results=10
)

# Download and enhance
book = await agent.download_book(books[0]['identifier'])
enhanced = await agent.enhance_content(
    book,
    "Update all code examples to Python 3.12 and add type hints"
)

# Rebrand
branded = await agent.rebrand(enhanced, {
    'new_title': f"{book.title} - 2026 Edition",
    'brand_name': "Your Company"
})

# Export
await agent.export_pdf(branded, "output.pdf")
```

### 2. Game Collection

```python
from agents.game_emulator import GameEmulatorAgent

agent = GameEmulatorAgent(ia_client=ia)

# Search NES games
games_meta = await agent.search_games(
    platform='nes',
    genre='action',
    year_range=(1985, 1995),
    max_results=50
)

# Download games
games = [await agent.download_game(g['identifier']) for g in games_meta[:20]]

# Create bundle
bundle = await agent.create_bundle(
    games,
    theme="Ultimate_NES_Collection",
    output_path="/output/nes_bundle.zip"
)
```

### 3. Natural Language Orchestration

```python
from agents.orchestrator import MasterOrchestratorAgent

orchestrator = MasterOrchestratorAgent(
    ia_client=ia,
    anthropic_api_key="your-key"
)

# Just describe what you want!
result = await orchestrator.execute("""
Find 10 cybersecurity books, update them with latest threats 
and tools, create a 12-week course with quizzes, and set up 
Stripe checkout at $299.99
""")

print(result['messages'])  # See what happened
print(result['results'])   # Get the outputs
```

---

## 🚀 Deployment

### Docker

```bash
# Build
docker-compose build

# Run
docker-compose up -d

# View logs
docker-compose logs -f
```

### Production (Kubernetes)

```bash
# Apply manifests
kubectl apply -f k8s/

# Check status
kubectl get pods -n prometheus-archive
```

---

## 💰 Monetization Features

### Stripe Integration

- **Product Catalog** - Automatic Stripe product creation
- **Checkout Sessions** - Secure payment processing
- **Webhooks** - Automated order fulfillment
- **License Keys** - Unique key generation per purchase
- **Customer Portal** - Self-service subscription management

### Pricing Strategies

```python
PRICING_TIERS = {
    'single_book': 9.99,
    'book_bundle_5': 39.99,
    'game_collection': 19.99,
    'premium_course': 99.99,
    'subscription_monthly': 19.99
}
```

### Revenue Dashboard

- Real-time sales tracking
- Conversion rate analytics
- Customer lifetime value
- Product performance metrics

---

## 📖 API Documentation

Full API documentation available at: `http://localhost:8000/docs`

### Key Endpoints

- `POST /api/books/search` - Search books
- `POST /api/books/rebrand` - Rebrand book
- `POST /api/games/search` - Search games
- `POST /api/games/bundle` - Create game bundle
- `POST /api/orchestrate` - Natural language interface
- `POST /api/checkout` - Create Stripe checkout
- `POST /api/webhooks/stripe` - Stripe webhook handler

---

## 🔒 Security

Implements **OWASP Top 10 for Agentic Applications 2026**:

- ✅ Input validation and sanitization
- ✅ Rate limiting (100 req/min per user)
- ✅ Prompt injection prevention
- ✅ Tool execution guardrails
- ✅ Audit logging for all agent actions
- ✅ Secure secrets management
- ✅ HTTPS/TLS encryption
- ✅ SQL injection protection

---

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=backend --cov-report=html

# Run specific test suite
pytest tests/test_agents/test_book_rebrander.py
```

---

## 📊 Performance

- **Book Processing**: ~2-5 min per book (AI enhancement)
- **Game Downloads**: ~10-30 sec per game
- **Bundle Creation**: ~1-3 min for 50 items
- **Concurrent Operations**: Up to 10 parallel agent tasks
- **API Latency**: <200ms for search operations

---

## 🤝 Contributing

Contributions welcome! See [CONTRIBUTING.md](CONTRIBUTING.md)

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

---

## 📄 License

MIT License - see [LICENSE](LICENSE)

---

## 🙏 Acknowledgments

- **Internet Archive** - Amazing content preservation
- **Anthropic** - Claude Opus 4.7 AI model
- **RetroArch** - Emulator infrastructure
- **FastAPI** - Modern Python web framework
- **LangGraph** - Multi-agent orchestration

---

## 📧 Support

- **Email**: support@rickjeffersonsolutions.com
- **GitHub Issues**: [Report Bug](https://github.com/rjbizsolution23-wq/prometheus-archive-engine/issues)
- **Documentation**: [Full Docs](https://docs.rickjeffersonsolutions.com)

---

## 🎯 Roadmap

### v2.1 (Next)
- [ ] Web UI (Next.js 16.2)
- [ ] Video content support
- [ ] Advanced course generator
- [ ] Affiliate program
- [ ] Analytics dashboard

### v2.2
- [ ] AI-generated covers
- [ ] Multi-language support
- [ ] Blockchain NFT integration
- [ ] White-label platform

### v3.0
- [ ] Autonomous content discovery
- [ ] Predictive trending analysis
- [ ] Self-optimizing pricing
- [ ] Full automation mode

---

**Built with ❤️ by RJ Prometheus Apex**

*Transform. Monetize. Scale.*
