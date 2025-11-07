from fastapi import APIRouter
from . import weather, currency, bitcoin

router = APIRouter()

router.include_router(weather.router)
router.include_router(currency.router)
router.include_router(bitcoin.router)