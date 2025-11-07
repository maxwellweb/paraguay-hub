from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional


# --- Modelos para Conversión de Moneda ---

class CurrencyConversionRequest(BaseModel):
    """Esquema para la solicitud de conversión de moneda."""
    from_currency: str = Field(..., description="Código de la moneda de origen (ej: USD, EUR)", min_length=3, max_length=3)
    amount: float = Field(..., description="Monto a convertir", gt=0)

class CurrencyConversionResponse(BaseModel):
    """Esquema para la respuesta de la conversión de moneda."""
    source_currency: str = Field(..., description="Moneda de origen.")
    target_currency: str = Field(..., description="Moneda de destino (PYG).")
    amount: float = Field(..., description="Monto original.")
    converted_amount: float = Field(..., description="Monto convertido a Guaraníes.")
    rate: float = Field(..., description="Tasa de cambio aplicada.")
    timestamp: datetime = Field(..., description="Momento de la consulta.")

# --- Modelos para el Clima ---

class WeatherResponse(BaseModel):
    """Esquema base para la respuesta del clima."""
    department: str = Field(..., description="Departamento de Paraguay consultado.")
    temp_celsius: float = Field(..., description="Temperatura en grados Celsius.")
    description: str = Field(..., description="Descripción del clima (ej: Lluvias ligeras).")
    humidity: int = Field(..., description="Porcentaje de humedad.")
    wind_speed_kmh: float = Field(..., description="Velocidad del viento en km/h.")
    
class CachedWeather(WeatherResponse):
    """Esquema para el documento de caché en MongoDB."""
    last_updated: datetime = Field(..., description="Momento en que se guardó la caché.")
    # ID de MongoDB es opcional ya que es generado por la DB
    id: Optional[str] = Field(alias="_id", default=None) 
    
    model_config = ConfigDict(populate_by_name=True)

# -- Modelo para conversión a bitcoin --

class BitcoinConversionRequest(BaseModel):
    amount: float = Field(..., description="Monto de BTC a convertir", gt=0)

class BitcoinConversionResponse(BaseModel):
    source_currency: str = Field(..., description="Moneda de origen.")
    target_currency: str = Field(..., description="Moneda de destino (PYG).")
    amount: float = Field(..., description="Monto original.")
    converted_amount: float = Field(..., description="Monto convertido a Guaraníes.")
    btc_rate_usd: float = Field(..., description="Tasa de cambio de BTC a USD.")
    btc_rate_pyg: float = Field(..., description="Tasa de cambio de BTC a PYG.")
    usd_rate_pyg: float = Field(..., description="Tasa de cambio de USD a PYG.")
    btc_high_24h: float = Field(..., description="Precio máximo de BTC en las últimas 24 horas.")
    btc_low_24h: float = Field(..., description="Precio mínimo de BTC en las últimas 24 horas.")
    btc_change_24h: float = Field(..., description="Variación del precio de BTC en las últimas 24 horas.")
    timestamp: datetime = Field(..., description="Momento de la consulta.")


class BitcoinHistoryPoint(BaseModel):
    date: str
    price_usd: float