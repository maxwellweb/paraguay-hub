import pytest
import pytest_asyncio
from unittest.mock import patch, AsyncMock

from app.services.currency import convert_currency
from tests.conftest import MOCK_CURRENCY_DATA
from app.core import database

@pytest_asyncio.fixture(scope="session", autouse=True)
def mock_db_connection():
    """
    Simula la conexión de la base de datos global para evitar el TypeError
    en las pruebas unitarias que dependen de database.database.
    """
    # Creamos un objeto mock que representa una conexión activa
    mock_db = {} # Un diccionario simple para simular un objeto con subscripción
    
    # Parcheamos la variable global 'database.database' con nuestro mock
    with patch.object(database, 'database', new=mock_db):
        yield mock_db

@pytest.mark.asyncio
async def test_convert_currency_success(mock_httpx_success):
    with patch("httpx.AsyncClient.get", new_callable=AsyncMock) as mock_get:
        # Configuramos el mock para que devuelva una respuesta exitosa
        mock_get.return_value = mock_httpx_success(MOCK_CURRENCY_DATA)
        
        # Ejecutamos la función
        amount = 100.0
        result = await convert_currency(amount=amount, from_currency="USD")
        
        # Verificamos el resultado
        mock_get.assert_called_once()

        assert result is not None
        assert result.source_currency == "USD"
        assert result.target_currency == "PYG"
        assert result.amount == amount
        assert result.converted_amount == MOCK_CURRENCY_DATA["conversion_rates"]["PYG"] * amount
        assert result.rate == MOCK_CURRENCY_DATA["conversion_rates"]["PYG"]
        assert result.converted_amount == round(MOCK_CURRENCY_DATA["conversion_rates"]["PYG"] * amount, 2)

@pytest.mark.asyncio
async def test_convert_currency_api_failure(mock_httpx_success):
    
    MOCK_FAILURE_DATA = {"result": "error", "error-type": "unsupported-code"}

    with patch("httpx.AsyncClient.get", new_callable=AsyncMock) as mock_get:
        mock_get.return_value = mock_httpx_success(MOCK_FAILURE_DATA)
        
        result = await convert_currency(amount=100.0, from_currency="XXX")
        
        assert result is None
        
        