# tests/test_bitcoin_service.py

import pytest
from unittest.mock import patch
import asyncio # Necesario para usar patch.object con asyncio.gather
from httpx import Response
from app.services.bitcoin import convert_bitcoin_to_pyg
from tests.conftest import (
    MOCK_BTC_RATE_DATA, 
    MOCK_USD_TO_PYG_RATE 
)

# Nota: Asumimos que mock_httpx_success es inyectado como fixture.

@pytest.mark.asyncio
async def test_convert_bitcoin_success(mock_httpx_success):
    """
    Prueba que la conversión de BTC a PYG sea exitosa, mockeando 
    las dos llamadas a APIs externas.
    """
    
    amount_btc = 0.5
    
    # 📌 1. Mockear la función interna httpx.AsyncClient.get
    # Como el servicio de bitcoin hace dos llamadas GET, debemos mockear la 
    # función get para que devuelva respuestas diferentes en orden.
    
    with patch("httpx.AsyncClient.get") as mock_get:
        
        # Configuramos los valores de retorno secuenciales:
        # 1. Tasa de BTC a USD (CoinGecko)
        # 2. Tasa de USD a PYG (ExchangeRate-API)
        mock_get.side_effect = [
            mock_httpx_success(MOCK_BTC_RATE_DATA),
            mock_httpx_success(MOCK_USD_TO_PYG_RATE)
        ]
        
        # 2. Ejecutar la función a probar
        result = await convert_bitcoin_to_pyg(amount_btc=amount_btc)
        
        # 3. Assertions (Verificaciones)
        
        # Fórmulas y valores esperados basados en los Mocks:
        BTC_Rate_USD_MOCK = 65000.00
        PYG_Rate_USD = 7450.00

        amount_btc = 0.5
        # Resultado Esperado: 0.5 * 65000.00 * 7450.00 = 242,125,000.00
        expected_conversion = 3725.00
        
        assert result is not None
        assert result.source_currency == "BTC"
        assert result.target_currency == "PYG"
        assert result.amount == amount_btc
        assert result.btc_rate_usd == BTC_Rate_USD_MOCK
        assert result.btc_rate_pyg == PYG_Rate_USD
        assert result.converted_amount == expected_conversion


@pytest.mark.asyncio
async def test_convert_bitcoin_api_failure(mock_httpx_success):
    """Prueba que la conversión falle si una de las APIs no responde."""
    
    amount_btc = 1.0
    
    with patch("httpx.AsyncClient.get") as mock_get:
        
        # Configuramos side_effect para que la primera llamada (BTC/USD) falle
        mock_get.side_effect = [
            # Simular un fallo de red o un JSON vacío (lo que resulte en None)
            mock_httpx_success({}), 
            # La segunda llamada no importa, porque el proceso fallará con la primera
            mock_httpx_success(MOCK_USD_TO_PYG_RATE) 
        ]
        
        # 2. Ejecutar la función a probar
        result = await convert_bitcoin_to_pyg(amount_btc=amount_btc)
        
        # 3. Assertion: Esperamos que retorne None
        assert result is None