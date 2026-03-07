# Project Forest - Automated Trading App

A Python-based automated trading bot with health monitoring.

## Quick Start

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or: venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Run the app
uvicorn app.main:app --reload
```

## API Endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /private/status` | Returns app status (liveness) |
| `GET /private/healthcheck` | Returns overall health (includes dependencies) |
| `GET /docs` | Auto-generated API documentation (Swagger UI) |

## Project Structure

```
project-forest/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application entry
│   ├── config.py            # Configuration management
│   ├── api/
│   │   ├── __init__.py
│   │   └── health.py        # Health check endpoints
│   └── services/
│       ├── __init__.py
│       └── binance_client.py # Exchange client (placeholder)
├── tests/
│   └── __init__.py
├── requirements.txt
└── README.md
```

## Configuration

Set environment variables or create a `.env` file:

```bash
APP_NAME=project-forest
APP_VERSION=0.1.0
DEBUG=true
BINANCE_TESTNET_API_KEY=your_key_here
BINANCE_TESTNET_SECRET=your_secret_here
```
