from .src.postgres.postgres_helper import PostgresserHelper
from fastapi import (
    FastAPI,
    Query,
    Request
)
app = FastAPI()

@app.get('/')
async def start():
    return {'ОГО': 'ОНО РАБОТАЕТ'}

@app.get('/register')
async def register():
    return {"page": "register"}

@app.get('/login')
async def login():
    return {"page": "login"}

@app.get('/get_article')
async def get_article():
    return {"page": "login"}

@app.get('/set_article')
async def set_article():
    return {"page": "login"}
