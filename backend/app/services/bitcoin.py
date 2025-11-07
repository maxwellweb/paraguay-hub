import httpx
from datetime import datetime, timedelta
from typing import Optional, List
from pydantic import BaseModel
import asyncio
from app.core.config import settings
from app.models.schemas import BitcoinConversionResponse
import random


BITCOIN_API_URL = "https://api.coingecko.com/api/v3"

EXCHANGE_API_URL = "https://v6.exchangerate-api.com/v6/"
EXCHANGE_API_KEY = settings.EXCHANGE_RATE_API_KEY
TARGET_CURRENCY = "PYG"
BASE_CURRENCY = "USD"
API_KEY = settings.COINGECKO_API_KEY

headers = {"x-cg-demo-api-key": API_KEY}

async def get_btc_to_usd_rate() -> Optional[float]: 
    
    params = {
        "ids": "bitcoin",
        "vs_currencies": "usd"
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(BITCOIN_API_URL+"/simple/price", params=params, timeout=10, headers=headers)
            response.raise_for_status()
            data = response.json()
            return data.get("bitcoin", {}).get("usd")
        except httpx.RequestError as e:
            print(f"Error al obtener la tasa de cambio de BTC a USD: {e}")
            return None

async def get_btc_high_low_24h() -> Optional[tuple[float, float]]: 
    
    params = {
        "vs_currency": "usd",
        "ids": "bitcoin",
        "names": "Bitcoin",
        "symbols": "btc",
        "category": "layer-1",
        "price_change_percentage": "7d",
        "per_page": 1,
        "page": 1,
        "sparkline": False,
        "locale": "en"
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(BITCOIN_API_URL+"/coins/markets", params=params, timeout=10, headers=headers)
            response.raise_for_status()
            data = response.json()
            return data[0].get("high_24h"), data[0].get("low_24h"), data[0].get("price_change_percentage_24h")
        except httpx.RequestError as e:
            print(f"Error al obtener la tasa de cambio de BTC a USD: {e}")
            return None

async def get_usd_to_pyg_rate() -> Optional[float]: 
    
    url = f"{EXCHANGE_API_URL}{EXCHANGE_API_KEY}/latest/{BASE_CURRENCY}"
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if data.get("result") == "success":
                rate = data["conversion_rates"][TARGET_CURRENCY]
                return rate
            
        except httpx.HTTPStatusError as e:
            print(f"Error HTTP al obtener la tasa de cambio de USD a PYG: {e}")
            return None
            
        except httpx.RequestError as e:
            print(f"Error al obtener la tasa de cambio de USD a PYG: {e}")
            return None
    
async def get_btc_to_pyg_rate() -> Optional[float]: 
    
    url = f"{EXCHANGE_API_URL}{EXCHANGE_API_KEY}/latest/{BASE_CURRENCY}"

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()

            if data.get("result") == "success":
                return data["conversion_rates"][TARGET_CURRENCY]
            return None

        except httpx.HTTPStatusError as e:
            print(f"Error HTTP al obtener la tasa de cambio de BTC a PYG: {e}")
            return None
            
        except httpx.RequestError as e:
            print(f"Error al obtener la tasa de cambio de BTC a PYG: {e}")
            return None
            
async def convert_bitcoin_to_pyg(amount_btc: float) -> Optional[BitcoinConversionResponse]:

    btc_usd_rate, btc_pyg_rate, usd_pyg_rate, low_high_btc_to_usd = await asyncio.gather(
        get_btc_to_usd_rate(),
        get_btc_to_pyg_rate(),
        get_usd_to_pyg_rate(),
        get_btc_high_low_24h()
    )
    
    if btc_usd_rate is None or btc_pyg_rate is None or usd_pyg_rate is None or low_high_btc_to_usd is None:
        return None
    
    converted_amount = (amount_btc * btc_usd_rate ) * usd_pyg_rate 
    converted_usd_to_pyg = btc_usd_rate * usd_pyg_rate
    converted_high_24h = low_high_btc_to_usd[0] * usd_pyg_rate
    converted_low_24h = low_high_btc_to_usd[1] * usd_pyg_rate
    
    return BitcoinConversionResponse(
        source_currency="BTC",
        target_currency=TARGET_CURRENCY,
        amount=amount_btc,
        converted_amount=round(converted_amount, 2),
        btc_rate_usd=round(btc_usd_rate, 2),
        btc_rate_pyg=round(converted_usd_to_pyg, 2),
        usd_rate_pyg=round(usd_pyg_rate, 2),
        btc_high_24h=round(converted_high_24h, 2),
        btc_low_24h=round(converted_low_24h, 2),
        btc_change_24h=round(low_high_btc_to_usd[2], 2),
        timestamp=datetime.now()
    )


class BitcoinHistoryPoint(BaseModel):
    date: str
    price_usd: float
    
async def get_bitcoin_history_data(days: int = 7) -> list[BitcoinHistoryPoint]:
    """
    Simula la obtención de datos históricos de Bitcoin.
    """
    history = []
    current_price = 65000.00 
    
    # Recorrer los días de forma descendente
    for i in range(days, 0, -1):
        date_obj = datetime.now() - timedelta(days=i)
        
        # Simular una variación aleatoria del precio
        variance = 1 + (random.uniform(-0.02, 0.02) * i/days)
        price = current_price * variance
        
        history.append(BitcoinHistoryPoint(
            # ✅ ESTA ES LA LÍNEA CRÍTICA: La fecha debe ser una cadena.
            date=date_obj.strftime("%Y-%m-%d"), 
            price_usd=round(price, 2)
        ))
        
    return history
