from fastapi import FastAPI
from contextlib import asynccontextmanager
from routes import BaseRoute , DataRoute
from utils import Settings ,get_settings
from motor.motor_asyncio import AsyncIOMotorClient
from models import UserModel

@asynccontextmanager
async def lifespan(app: FastAPI):
    env_var = get_settings()
    app.MongoClient =AsyncIOMotorClient(env_var.MONGO_DB_CLIENT)
    app.Database = app.MongoClient[env_var.MONGO_DB_NAME]
    
    yield
    app.MongoClient.close()

app = FastAPI(lifespan=lifespan)

app.include_router(BaseRoute)
app.include_router(DataRoute)