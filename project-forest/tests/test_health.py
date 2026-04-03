"""Tests for the health endpoints."""

import pytest
import pytest_asyncio
import httpx
from httpx import ASGITransport, AsyncClient
import respx
from app.main import app, BINANCE_TESTNET_URL


@pytest_asyncio.fixture
async def client():
    """Create an async test client."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client


@pytest.mark.asyncio
class TestStatusEndpoint:
    """Tests for /private/status endpoint."""

    async def test_status_returns_up(self, client):
        """Happy case: status endpoint returns 'up'."""
        response = await client.get("/private/status")
        
        assert response.status_code == 200
        assert response.json() == {"status": "up"}


@pytest.mark.asyncio
class TestHealthcheckEndpoint:
    """Tests for /private/healthcheck endpoint."""

    @respx.mock
    async def test_healthcheck_all_up(self, client):
        """Happy case: both app and Binance are up."""
        # Mock Binance API returning success
        respx.get(BINANCE_TESTNET_URL).mock(return_value=httpx.Response(200))
        
        response = await client.get("/private/healthcheck")
        
        assert response.status_code == 200
        data = response.json()
        assert data["overall"] == "up"
        assert data["components"]["app"]["status"] == "up"
        assert data["components"]["binance"]["status"] == "up"

    @respx.mock
    async def test_healthcheck_binance_down_http_error(self, client):
        """Unhappy case: Binance returns HTTP error."""
        # Mock Binance API returning 500 error
        respx.get(BINANCE_TESTNET_URL).mock(return_value=httpx.Response(500))
        
        response = await client.get("/private/healthcheck")
        
        assert response.status_code == 200
        data = response.json()
        assert data["overall"] == "degraded"
        assert data["components"]["app"]["status"] == "up"
        assert data["components"]["binance"]["status"] == "down"
        assert "HTTP 500" in data["components"]["binance"]["error"]

    @respx.mock
    async def test_healthcheck_binance_down_connection_error(self, client):
        """Unhappy case: Binance connection fails."""
        # Mock Binance API raising connection error
        respx.get(BINANCE_TESTNET_URL).mock(side_effect=Exception("Connection refused"))
        
        response = await client.get("/private/healthcheck")
        
        assert response.status_code == 200
        data = response.json()
        assert data["overall"] == "degraded"
        assert data["components"]["binance"]["status"] == "down"
        assert "Connection refused" in data["components"]["binance"]["error"]
