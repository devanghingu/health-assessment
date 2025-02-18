from fastapi import FastAPI
from core_app.app_routes import api_router

fastapi_app = FastAPI()

fastapi_app.include_router(api_router)