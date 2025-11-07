from pydantic_settings import BaseSettings
from dotenv import load_dotenv
from pydantic import ConfigDict

load_dotenv()

class Settings(BaseSettings):
    
# --- Configuración del Servidor ---
    PROJECT_NAME: str = "ClimaPYG"
    API_V1_STR: str = "/api/v1"

    # --- Configuración de MongoDB ---
    MONGO_URI: str
    DATABASE_NAME: str = "climapyg"
    
    # --- Claves de APIs Externas ---
    EXCHANGE_RATE_API_KEY: str
    OPENWEATHERMAP_API_KEY: str
    COINGECKO_API_KEY: str
    
    # --- Configuración del Caché de Clima ---
    # Tiempo en segundos que los datos del clima serán considerados válidos en la caché
    WEATHER_CACHE_TTL_SECONDS: int = 3600 # 1 hora
    
    model_config = ConfigDict(env_file=".env", extra="ignore")
# Instancia global de configuración
settings = Settings()