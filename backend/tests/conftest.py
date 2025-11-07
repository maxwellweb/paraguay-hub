# tests/conftest.py

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
import pytest_asyncio
from httpx import Response, Request
from app.main import app
from app.core import database
from unittest.mock import patch, MagicMock

# 📌 Simulación de Datos de Éxito para APIs Externas

# Simulación para OpenWeatherMap (Clima)
MOCK_WEATHER_DATA = {
    "main": {"temp": 28.5, "humidity": 65},
    "weather": [{"description": "cielo claro"}],
    "wind": {"speed": 4.17} # 4.17 m/s -> ~15 km/h
}

# Simulación para ExchangeRate-API (Moneda) - USD a PYG
MOCK_CURRENCY_DATA = {
    "result": "success",
    "conversion_rates": {
        "PYG": 7450.00
    }
}

# Simulación para ExchangeRate-API (Moneda) - BTC a USD
MOCK_BTC_RATE_DATA = {
    "bitcoin": {
        "usd": 65000.00
    }
}

# Simulación para ExchangeRate-API (Moneda) - BTC a PYG
MOCK_USD_TO_PYG_RATE = {
    "result": "success",
    "conversion_rates": {
        "PYG": 7450.00
    }
}


COLLECTION_NAME = "weather_cache"

@pytest_asyncio.fixture(scope="session", autouse=True)
def mock_db_connection():
    """
    Simula la conexión de la base de datos global y la colección 'weather_cache'.
    """
    
    # 1. Creamos un objeto MagicMock para simular la colección
    mock_collection = MagicMock()
    
    # 2. Creamos el objeto DB mock, y usamos la CONSTANTE para mapear la colección
    mock_db = {
        # ✅ La clave 'weather_cache' DEBE existir en mock_db
        COLLECTION_NAME: mock_collection 
    } 
    
    # 3. Parcheamos la variable global
    with patch.object(database, 'database', new=mock_db):
        yield mock_db


# 💡 Fixture para el cliente de prueba de FastAPI
@pytest_asyncio.fixture(scope="module")
async def client():
    # Usamos httpx.AsyncClient para probar la aplicación FastAPI de forma asíncrona
    async with client(app=app, base_url="http://test") as c:
        yield c

# 💡 Fixture para la configuración de pytest-asyncio
@pytest.fixture(scope="session")
def anyio_backend():
    # Necesario para que pytest-asyncio funcione con las funciones de prueba async
    return 'asyncio'

# 💡 Fixture para simular la respuesta HTTP exitosa
@pytest.fixture
def mock_httpx_success():
    """Retorna un objeto Response simulado con status 200 y un objeto Request."""
    def _mock_success(json_data):
        # 💡 Creamos un objeto Request simulado, es la clave para la corrección
        mock_request = Request("GET", "http://mock-url.com")
        
        # 💡 Adjuntamos el mock_request al Response
        return Response(status_code=200, json=json_data, request=mock_request) 
    return _mock_success