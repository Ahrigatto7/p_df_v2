from fastapi import FastAPI
from .api_router import router

app = FastAPI()
app.include_router(router)
