import httpx
from datetime import datetime, timedelta, timezone
from typing import Optional
from fastapi import HTTPException

from app.core.config import settings
from app.core.database import database
from app.models import schemas
from motor.motor_asyncio import AsyncIOMotorDatabase

WEATHER_API_KEY = settings.OPENWEATHERMAP_API_KEY

DEPARTMENTS = {
    "ASUNCION": {"lat": -25.2637, "lon": -57.5759, "name": "Asunción"},
    "ALTO_PARANA": {"lat": -25.5000, "lon": -54.6167, "name": "Ciudad del Este (Alto Parana)"},
    "CENTRAL": {"lat": -25.3333, "lon": -57.5000, "name": "San Lorenzo (Central)"},
    "ITAPUA": {"lat": -27.3333, "lon": -56.0000, "name": "Encarnación (Itapúa)"},
}

COLLECTION_NAME = "weather_cache"
CACHE_TTL_HOURS = 1

# --- Funciones de MongoDB (Cache) ---
async def get_cached_weather(department: str, db: AsyncIOMotorDatabase) -> Optional[schemas.WeatherResponse]:

    cache_doc = await db[COLLECTION_NAME].find_one({"department": department})
    
    if cache_doc:
        last_updated = cache_doc.get("last_updated")

        if last_updated.tzinfo is None or last_updated.tzinfo.utcoffset(last_updated) is None:
            last_updated = last_updated.replace(tzinfo=timezone.utc)

        expiration_time = last_updated + timedelta(hours=CACHE_TTL_HOURS)

        if datetime.now(timezone.utc) < expiration_time:
            print("✅ Usando datos de la caché para el departamento:", department)
            return schemas.WeatherResponse(**cache_doc)
        else:
            print("❌ Datos de la caché para el departamento:", department, "han expirado.")
            return None    
    
    return None

async def update_weather_cache(weather_data: schemas.WeatherResponse, db: AsyncIOMotorDatabase):


    department = weather_data.department

    filter_query = {"department": department}

    update_operation = {
        "$set": {
            **weather_data.model_dump(),
            "last_updated": datetime.now(timezone.utc)
        }
    }
    
    

    await db[COLLECTION_NAME].update_one(
        filter_query,
        update_operation,
        upsert=True
    )
    print(f"✅ Datos de clima actualizados en la caché para el departamento: {weather_data.department}")


async def fetch_weather_from_api(department: str, lat: float, lon: float) -> Optional[schemas.WeatherResponse]:

    params = {
        "lat": lat,
        "lon": lon,
        "appid": WEATHER_API_KEY,
        "units": "metric",
        "lang": "es",
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get("https://api.openweathermap.org/data/2.5/weather", params=params, timeout=10)
            response.raise_for_status()
            

            data = response.json()

            weater_response = schemas.WeatherResponse(
                department=department,
                temp_celsius=data["main"]["temp"],
                description=data["weather"][0]["description"],
                humidity=data["main"]["humidity"],
                wind_speed_kmh=data["wind"]["speed"] * 3.6,
                timestamp=datetime.now(),
            )

            return weater_response
        
        except (httpx.HTTPStatusError, httpx.RequestError) as e:
            print(f"❌ Error al consultar la API de clima: {e}")
            return None
        
async def get_weather_data(department: str) -> Optional[schemas.WeatherResponse]:
    """
    Obtiene los datos del clima para un departamento específico usando la API externa.
    """
    
    # 1. Validar y obtener coordenadas
    department_key = department.upper()
    if department_key not in DEPARTMENTS:
        raise HTTPException(
            status_code=404,
            detail=f"Departamento '{department}' no encontrado o no soportado."
        )
        
    coords = DEPARTMENTS[department_key]
    
    params = {
        "lat": coords["lat"],
        "lon": coords["lon"],
        "appid": WEATHER_API_KEY,
        "units": "metric", # Para obtener la temperatura en Celsius
        "lang": "es"       # Para obtener la descripción en español
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get("https://api.openweathermap.org/data/2.5/weather", params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            # 2. Extracción y Formateo
            temp = data["main"]["temp"]
            humidity = data["main"]["humidity"]
            description = data["weather"][0]["description"]
            wind_speed = data["wind"]["speed"] # Velocidad en m/s
            
            # Conversión de m/s a km/h (multiplicar por 3.6)
            wind_speed_kmh = wind_speed * 3.6
            
            # 3. Devolver el esquema de respuesta
            return schemas.WeatherResponse(
                department=coords["name"],
                temp_celsius=round(temp, 1),
                description=description,
                humidity=humidity,
                wind_speed_kmh=round(wind_speed_kmh, 1)
            )

        except httpx.HTTPStatusError as e:
            print(f"Error HTTP al obtener el clima: {e}")
            raise HTTPException(
                status_code=e.response.status_code,
                detail="Error de la API externa de clima."
            )
        except httpx.RequestError as e:
            print(f"Error de conexión al obtener el clima: {e}")
            raise HTTPException(
                status_code=503,
                detail="No se pudo conectar con el servicio de clima."
            )
        except (KeyError, IndexError) as e:
            print(f"Error de formato inesperado de la API: {e}")
            raise HTTPException(
                status_code=500,
                detail="Error al procesar la respuesta del clima."
            )
    

        