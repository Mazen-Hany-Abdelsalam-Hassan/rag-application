from fastapi import FastAPI
from routes.base_route import base_route

app = FastAPI()
app.include_router(base_route)