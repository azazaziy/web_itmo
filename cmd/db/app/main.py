from .src.postgres.postgres_helper import PostgresHelper
from fastapi import (
    FastAPI,
    Query,
    Request
)

app = FastAPI()
db = PostgresHelper(
    host='db',
    port=5432,
    password='postgres',
    user='postgres',
    database='postgres',
)
@app.get('/')
async def start():
    return {'wow': 'it\'s works'}

@app.get('/register')
async def register():
    return {"page": "register"}

@app.get('/login')
async def login():
    return {"page": "login"}

@app.get('/get_article')
async def get_article():
    return {"article": 'article'}

@app.get('/set_article')
async def set_article():
    return {"page": "login"}

@app.get('/set_comment')
async def set_comment():
    return {"page": "login"}

async def get_comment():
    return {'comments': {'1':1, '2':2}}
