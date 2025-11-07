from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
import asyncio
from app.core.config import settings

client: AsyncIOMotorClient = None
database: AsyncIOMotorDatabase = None

async def connect_to_mongo():
    global client, database

    try:
        client = AsyncIOMotorClient(settings.MONGO_URI,  serverSelectionTimeoutMS=5000)
        database = client[settings.DATABASE_NAME]
        await client.admin.command("ping")
        print("✅ Conexión a MongoDB exitosa.")
    except Exception as e:
        print(f"❌ Error al conectar a MongoDB: {e}")

async def close_mongo_connection():
    global client, database
    if client:
        await client.close()
        print("❌ Conexión a MongoDB cerrada.")

def get_database():
    global database
    if database is None:
        raise Exception("❌ No se ha establecido una conexión a MongoDB.")
    return database