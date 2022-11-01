"""
    author  : azwar8597@gmail.com
    project : API 
"""


from fastapi import APIRouter #type: ignore
from api_analytic.controllers import api

api_router = APIRouter() 

api_router.include_router(api.router, tags=["api-analytic-data"])


