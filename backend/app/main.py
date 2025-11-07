import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.database import connect_to_mongo, close_mongo_connection
from app.api.v1 import routers as api_router

# Configuración de Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Conectando a MongoDB...")
    await connect_to_mongo()
    yield
    logger.info("Cerrando la conexión a MongoDB...")
    await close_mongo_connection()


# --- Creación de la aplicación ---
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="API para obtener el clima y la conversión de monedas.",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    version="1.0.0",
    lifespan=lifespan,
)

# -- Rutas de la API --


# Configuración CORS
origins = [
    "*"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluimos las rutas de la API 
app.include_router(
    api_router.router,
    prefix=settings.API_V1_STR,
)

@app.get("/", tags=["Health Check"], description="Endpoint de Health Check", summary="Endpoint de Health Check")
async def root():
    return {"message": "API de Clima y Conversión de Monedas funcionando. Visita /api/v1/docs para la documentación."}