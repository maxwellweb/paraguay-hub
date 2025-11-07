# /app/api/v1/currency.py

from fastapi import APIRouter, HTTPException
from app.models.schemas import CurrencyConversionRequest, CurrencyConversionResponse
from app.services import currency as currency_service 
router = APIRouter(
    prefix="/currency",
    tags=["Conversor de Moneda"]
)

@router.post(
    "/convert", 
    response_model=CurrencyConversionResponse,
    summary="Convierte una moneda a Guaraníes Paraguayos (PYG)"
)
async def convert_to_pyg(request: CurrencyConversionRequest):
    """
    Recibe el código de una moneda y un monto, y devuelve el equivalente en PYG.
    
    - **from_currency**: Código ISO 4217 (ej: USD, EUR, BRL).
    - **amount**: Cantidad a convertir.
    """
    
    conversion_result = await currency_service.convert_currency(
        from_currency=request.from_currency,
        amount=request.amount
    )
    
    if conversion_result is None:
        raise HTTPException(
            status_code=400,
            detail=f"No se pudo obtener la tasa para la moneda '{request.from_currency}'. Asegúrese de usar un código ISO 4217 válido (ej: USD)."
        )
        
    return conversion_result
