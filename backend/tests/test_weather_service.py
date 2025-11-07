# tests/test_weather_service.py

import pytest
from unittest.mock import patch, AsyncMock
from datetime import datetime, timedelta, timezone

from app.services.weather import get_weather_data
from app.core import database # Importamos el módulo para acceder al 'database'
from app.core.config import settings
from tests.conftest import MOCK_WEATHER_DATA


COLLECTION_NAME = "weather_cache"



@pytest.mark.asyncio
async def test_weather_cache_miss_and_fetch(mock_httpx_success):
    """
    Prueba el escenario Cache Miss: 
    1. No hay datos en MongoDB.
    2. Consulta la API externa.
    3. Guarda los datos en MongoDB.
    """
    department = "ASUNCION"

    # 📌 1. Configurar Mocks

# 1. Simular la colección y sus métodos asíncronos
    mock_collection = AsyncMock() 
    mock_collection.find_one.return_value = None # Cache Miss
    # Simular que update_one no falla y es asíncrono
    mock_collection.update_one.return_value = None 

    # 2. Simular la base de datos (un diccionario que contiene la colección)
    mock_db_object = {COLLECTION_NAME: mock_collection}

    # 3. Parchear la función que obtiene la base de datos para devolver nuestro mock
    # ESTO SUSTITUYE A TODO EL PATCH.OBJECT ANTERIOR DE CONTEST.PY
    with patch('app.core.database.get_database') as mock_get_db:
        mock_get_db.return_value = mock_db_object
        
        # 2. Ejecutar la función a probar (sin argumento de DB, ya que se inyecta por get_database)
        result = await get_weather_data(department) # tests/test_weather_service.py

import pytest
from unittest.mock import patch, AsyncMock
from datetime import datetime, timedelta, timezone

from app.services.weather import get_weather_data
from app.core import database # Importamos el módulo para acceder al 'database'
from app.core.config import settings
from tests.conftest import MOCK_WEATHER_DATA # Asegúrate de que este MOCK_WEATHER_DATA esté disponible


# 💡 La constante COLLECTION_NAME está bien definida aquí
COLLECTION_NAME = "weather_cache"


# ⚠️ IMPORTANTE: EL FIXTURE setup_and_teardown_db FUE ELIMINADO PARA EVITAR CONFLICTOS.
# NO DEBE ESTAR PRESENTE EN ESTE ARCHIVO.


@pytest.mark.asyncio
async def test_weather_cache_miss_and_fetch(mock_httpx_success):
    """
    Prueba el escenario Cache Miss: 
    1. No hay datos en MongoDB.
    2. Consulta la API externa.
    3. Guarda los datos en MongoDB.
    """
    department = "ASUNCION"

    # 📌 1. Configurar Mocks
    
    # a) Simular la colección y sus métodos asíncronos
    mock_collection = AsyncMock() 
    # Simula Cache Miss: find_one retorna None
    mock_collection.find_one.return_value = None 
    # Simular que update_one no falla
    mock_collection.update_one.return_value = None 

    # b) Simular la base de datos (inyección directa)
    mock_db_object = {COLLECTION_NAME: mock_collection}

    # c) Simular la respuesta HTTP externa de éxito
    with patch("httpx.AsyncClient.get") as mock_get:
        mock_get.return_value = mock_httpx_success(MOCK_WEATHER_DATA)
        
        # 2. Ejecutar la función a probar
        # ✅ CORRECCIÓN FINAL: Pasar el mock_db_object como el argumento 'db'
        result = await get_weather_data(department, mock_db_object) 

        # 3. Assertions (Verificaciones)
        
        # a) Debe haber llamado a la API externa
        mock_get.assert_called_once()
        # b) Debe haber llamado a find_one (para verificar la caché)
        mock_collection.find_one.assert_called_once()
        # c) Debe haber llamado a update_one (para guardar el resultado)
        mock_collection.update_one.assert_called_once() 
        # d) Verificar el resultado
        assert result.department == department
        assert result.temp_celsius == 28.5


@pytest.mark.asyncio
async def test_weather_cache_hit(mock_httpx_success):
    """
    Prueba el escenario Cache Hit: 
    1. Encuentra datos frescos en MongoDB.
    2. NO consulta la API externa.
    """
    department = "ITAPUA"
    
    # 📌 1. Datos simulados en caché (frescos)
    fresh_time = datetime.now(timezone.utc) - timedelta(minutes=1)
    
    MOCK_CACHED_DOC = {
        "department": department,
        "temp_celsius": 32.0,
        "description": "Soleado",
        "humidity": 45,
        "wind_speed_kmh": 10.0,
        "last_updated": fresh_time # Clave para que sea un Cache Hit
    }

    # 📌 2. Configurar Mocks
    
    # a) Simular la colección (AsyncMock)
    mock_collection = AsyncMock()
    # Simula Cache Hit: find_one retorna el documento
    mock_collection.find_one.return_value = MOCK_CACHED_DOC
    
    # b) Simular la base de datos (inyección directa)
    mock_db_object = {COLLECTION_NAME: mock_collection}
    
    # c) Simular la consulta a la API externa para verificar que NO sea llamada
    with patch("httpx.AsyncClient.get") as mock_get:
        # Aseguramos un return_value para evitar fallos si se llama inesperadamente
        mock_get.return_value = mock_httpx_success(MOCK_WEATHER_DATA) 
        
        # 3. Ejecutar la función a probar
        # ✅ CORRECCIÓN FINAL: Pasar el mock_db_object como el argumento 'db'
        result = await get_weather_data(department, mock_db_object)

        # 4. Assertions (Verificaciones)
        
        # a) La API externa NO debe ser llamada
        mock_get.assert_not_called()
        # b) MongoDB (find_one) SÍ debe ser llamado
        mock_collection.find_one.assert_called_once()
        # c) Verificar que update_one NO fue llamado
        mock_collection.update_one.assert_not_called()
        # d) Verificar el resultado debe ser de la caché
        assert result.department == department
        assert result.temp_celsius == 32.0

        # 3. Assertions (Verificaciones)
        
        # a) Debe haber llamado a la API externa
        mock_get.assert_called_once()
        # b) Debe haber guardado los datos en MongoDB (usando la colección simulada)
        mock_collection.update_one.assert_called_once() # 💡 Aserción contra el mock
        # c) Verificar el resultado
        assert result.department == department
        assert result.temp_celsius == 28.5
        
        # b) Simular que MongoDB no encuentra nada (find_one retorna None)
        # with patch.object(mock_db_object[COLLECTION_NAME], 'find_one', new_callable=AsyncMock) as mock_find:
        #     mock_find.return_value = None
            
        #     # c) Simular que MongoDB guarda los datos
        #     with patch.object(mock_db_object[COLLECTION_NAME], 'update_one', new_callable=AsyncMock) as mock_update:
                
        #         mock_update.return_value = mock_db_object
        #         # 2. Ejecutar la función a probar
        #         result = await get_weather_data(department, mock_update)

        #         # 3. Assertions (Verificaciones)
                
        #         # a) Debe haber llamado a la API externa
        #         mock_get_db.assert_called_once()
        #         # b) Debe haber guardado los datos en MongoDB
        #         mock_update.assert_called_once()
        #         # c) Verificar el resultado
        #         assert result.department == department
        #         assert result.temp_celsius == 28.5


@pytest.mark.asyncio
async def test_weather_cache_hit():
    """
    Prueba el escenario Cache Hit: 
    1. Encuentra datos frescos en MongoDB.
    2. NO consulta la API externa.
    """
    department = "ITAPUA"
    
    # 📌 1. Datos simulados en caché (frescos)
    
    # Creamos un documento que es más reciente que el TTL (ej: 1 minuto atrás)
    fresh_time = datetime.now(timezone.utc) - timedelta(minutes=1)
    
    MOCK_CACHED_DOC = {
        "department": department,
        "temp_celsius": 32.0,
        "description": "Soleado",
        "humidity": 45,
        "wind_speed_kmh": 10.0,
        "last_updated": fresh_time # Clave para que sea un Cache Hit
    }

    # 📌 2. Configurar Mocks

    mock_collection = AsyncMock()
    mock_collection.find_one.return_value = MOCK_CACHED_DOC
    
    mock_db_object = {COLLECTION_NAME: mock_collection}

    mock_update = AsyncMock()
    mock_db_object[COLLECTION_NAME].update_one = mock_update
    

    
    # a) Simular la consulta a la API externa para verificar que NO sea llamada
    with patch("app.core.database.get_database", new_callable=AsyncMock) as mock_get_db:

        mock_get_db.return_value = mock_db_object
        
        # b) Simular que MongoDB SÍ encuentra datos frescos
        with patch.object(mock_db_object[COLLECTION_NAME], 'find_one', new_callable=AsyncMock) as mock_find:
            mock_find.return_value = MOCK_CACHED_DOC
            
            # 3. Ejecutar la función a probar
            result = await get_weather_data(department, mock_db_object)

            # 4. Assertions (Verificaciones)
            
            # a) La API externa NO debe ser llamada
            mock_get_db.assert_not_called()
            # b) Verificar el resultado debe ser de la caché
            assert result.department == department
            assert result.temp_celsius == 32.0
