# /app/api/v1/weather.py

from fastapi import APIRouter, HTTPException, Depends
from app.models import schemas
from app.services import weather as weather_service

router = APIRouter(
    prefix="/weather",
    tags=["Clima Paraguay"]
)

@router.get(
    "/{department_name}", 
    response_model=schemas.WeatherResponse,
    summary="Obtiene el clima actual de un departamento de Paraguay"
)
async def get_department_weather(
    department_name: str,
    ):
    """
    Busca el clima para el departamento de Paraguay especificado. 
    Los datos se sirven desde una caché de MongoDB con una duración de 1 hora.
    """
    
    weather_result = await weather_service.get_weather_data(department_name)
    
    if weather_result is None:
        supported_departments = ", ".join(weather_service.DEPARTMENTS.keys())
        
        raise HTTPException(
            status_code=404,
            detail=f"Departamento '{department_name}' no soportado o error al consultar el clima. Departamentos soportados: {supported_departments}"
        )
        
    return weather_result