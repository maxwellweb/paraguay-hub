import httpx
from datetime import datetime
from app.core.config import settings
from app.models.schemas import CurrencyConversionResponse
from typing import Optional

BASE_URL = "https://v6.exchangerate-api.com/v6"
TARGET_CURRENCY = "PYG"

async def get_conversion_rate(from_currency: str) -> Optional[float]:
    
    url = f"{BASE_URL}/{settings.EXCHANGE_RATE_API_KEY}/latest/{from_currency.upper()}"

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if data.get("result") == "success":
                rate = data["conversion_rates"].get(TARGET_CURRENCY)
                return rate

        except httpx.HTTPStatusError as e:
            print(f"Error HTTP al obtener la tasa de cambio: {e}")
            return None
                
        except httpx.RequestError as e:
            print(f"Error de red al obtener la tasa de cambio: {e}")
            return None


async def convert_currency(amount: float, from_currency: str) -> Optional[CurrencyConversionResponse]:
    rate = await get_conversion_rate(from_currency)
    if rate is None:
        return None

    converted_amount = amount * rate
    
    return CurrencyConversionResponse(
            source_currency=from_currency,
            target_currency=TARGET_CURRENCY,
            amount=amount,
            converted_amount=round(converted_amount, 2),
            rate=rate,
            timestamp=datetime.now()
        )