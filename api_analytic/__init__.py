"""
    author  : azwar8597@gmail.com
    project : API 
"""

from fastapi import FastAPI #type: ignore
from api_analytic.controllers import api_router

def create_app():

    app = FastAPI()

    app.include_router(api_router)

    return app

