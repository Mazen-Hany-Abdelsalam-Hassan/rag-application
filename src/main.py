from fastapi import FastAPI
from contextlib import asynccontextmanager
from routes import BaseRoute , DataRoute,UserOverviewRoute ,NLP_Route
from utils import Settings ,get_settings
from motor.motor_asyncio import AsyncIOMotorClient
from inference_service import Factory
from vector_database import VectorDatabaseFactory
@asynccontextmanager
async def lifespan(app: FastAPI):
    env_var = get_settings()
    app.MongoClient =AsyncIOMotorClient(env_var.MONGO_DB_CLIENT)
    app.Database = app.MongoClient[env_var.MONGO_DB_NAME]

    
    app.embedding_model = Factory(env_var).create(env_var.EMBEDDING_MODEL_BACKEND)
    app.embedding_model.set_embedding_model(embedding_dim=env_var.EMBEDDING_MODEL_DIM,
                                            embedding_model_id=env_var.EMBEDDING_MODEL_NAME)
    app.llm_model = Factory(env_var).create(env_var.LLM_BACKEND)
    app.llm_model.set_generation_model(env_var.LLM_MODEL)
    app.vector_DB_client = VectorDatabaseFactory(config=env_var).set_provider(env_var.VECTOR_DATABASE_NAME)
    app.vector_DB_client.connect()
    #print(app.vector_DB_client.get_all_collection())
    #print(app.embedding_model.embed_text("MAZEN"))

    yield
    app.MongoClient.close()
    app.vector_DB_client.disconnect()

app = FastAPI(lifespan=lifespan)

app.include_router(BaseRoute)
app.include_router(DataRoute)
app.include_router(UserOverviewRoute)
app.include_router(NLP_Route)