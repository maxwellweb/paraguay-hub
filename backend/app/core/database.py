from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from typing import Optional
from app.core.config import settings

client: Optional[AsyncIOMotorClient] = None
database: Optional[AsyncIOMotorDatabase] = None

async def connect_to_mongo():
    global client, database

    # Creamos un cliente localmente para probar la conexión
    test_client: Optional[AsyncIOMotorClient] = None 
    
    try:
        # 1. Crear el cliente de prueba
        test_client = AsyncIOMotorClient(settings.MONGO_URI,  serverSelectionTimeoutMS=5000)
        
        # 2. Ping para verificar la conexión
        await test_client.admin.command("ping")
        
        # 3. Solo si es exitoso, asignamos a las variables globales
        client = test_client
        database = client[settings.DATABASE_NAME]
        
        print("✅ Conexión a MongoDB exitosa.")
    except Exception as e:
        print(f"❌ Error al conectar a MongoDB: {e}")
        # 4. Si falló después de crear el objeto cliente, lo cerramos
        if test_client:
            await test_client.close()
        
        # Aquí, client y database permanecen como None, lo cual es correcto.

async def close_mongo_connection():
    global client, database
    
    # 💡 La verificación que ya tienes es correcta.
    if client:
        await client.close()
        print("❌ Conexión a MongoDB cerrada.")
    else:
        # Añadir un mensaje para saber si la conexión nunca se abrió
        print("No hay cliente de MongoDB activo para cerrar.")

def get_database():
    global database
    if database is None:
        raise Exception("❌ No se ha establecido una conexión a MongoDB.")
    return database