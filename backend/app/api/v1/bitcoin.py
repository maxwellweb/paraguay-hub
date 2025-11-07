# /app/api/v1/bitcoin.py

from fastapi import APIRouter, HTTPException, Query
from typing import List
from app.models import schemas
from app.services import bitcoin as bitcoin_service # Importamos la lógica

router = APIRouter(
    prefix="/bitcoin",
    tags=["Conversor de Bitcoin"]
)

@router.get(
    "/history",
    response_model=List[schemas.BitcoinHistoryPoint],
    summary="Obtiene el historial de precios de Bitcoin (BTC) en USD"
)
async def get_bitcoin_history(days: int = Query(7, ge=1, le=30, description="Número de días de historial a obtener")):
    """
    Obtiene el historial de precios de Bitcoin (BTC) en USD para los últimos 7 días.
    """
    
    
    return await bitcoin_service.get_bitcoin_history_data(days)

@router.post(
    "/convert", 
    response_model=schemas.BitcoinConversionResponse,
    summary="Convierte Bitcoin (BTC) a Guaraníes Paraguayos (PYG)"
)
async def convert_btc_to_pyg(request: schemas.BitcoinConversionRequest):
    """
    Recibe un monto en BTC y devuelve su valor equivalente en PYG, 
    usando tasas de cambio actuales de BTC/USD y USD/PYG.
    """
    
    conversion_result = await bitcoin_service.convert_bitcoin_to_pyg(
        amount_btc=request.amount
    )
    
    if conversion_result is None:
        raise HTTPException(
            status_code=503,
            detail="Error al obtener las tasas de cambio de BTC o USD. Las APIs externas no respondieron correctamente."
        )
        
    return conversion_result