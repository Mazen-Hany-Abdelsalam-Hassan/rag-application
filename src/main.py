from fastapi import FastAPI
from routes import BaseRoute , DataRoute
from utils import Settings ,get_settings

app= FastAPI()

app.include_router(BaseRoute)
app.include_router(DataRoute)