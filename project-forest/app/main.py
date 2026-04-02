from fastapi import FastAPI
import httpx

app = FastAPI(title="project-forest")

BINANCE_TESTNET_URL = "https://testnet.binance.vision/api/v3/ping"


@app.get("/private/status")
def status():
    """Liveness probe - returns basic app status."""
    return {"status": "up"}


@app.get("/private/healthcheck")
async def healthcheck():
    """Readiness probe - returns overall health including dependencies."""
    components = {
        "app": {"status": "up"},
        "binance": await check_binance()
    }
    
    overall = "up" if all(c["status"] == "up" for c in components.values()) else "degraded"
    
    return {
        "overall": overall,
        "components": components
    }


async def check_binance():
    """Check Binance Testnet connectivity."""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(BINANCE_TESTNET_URL, timeout=5.0)
            if response.status_code == 200:
                return {"status": "up"}
            return {"status": "down", "error": f"HTTP {response.status_code}"}
        except Exception as e:
            return {"status": "down", "error": str(e)}
