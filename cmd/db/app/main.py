from .src.postgres.postgres_helper import PostgresHelper
from typing import Optional, List
from datetime import datetime
import json
from .pages.article import SetArticle
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
async def start(

):
    return {'wow': 'it\'s works'}

@app.get('/register')
async def register(
        request: Request = None
):
    return {"page": request}

@app.get('/login')
async def login():
    return {"page": "login"}

@app.get('/get_article')
async def get_article():
    return {"article": 'article'}

@app.get('/set_article')
async def set_article(
    author,
    title,
    text,
    image,
):
    response = json.dumps(
        {
            'author': author,
            'title': title,
            'text': text,
            'image': image,
            'timestamp': str(datetime.now()),
            'tags': None,
            'article_id': None,
            'editors': None,
            'moderators': None
        }
    )

    article = SetArticle(response)
    article_id = db.execute(
        action_type='select_one',
        values='MAX(article_id)',
        table='articles'
    )
    article_id = str(article_id[0] + 1)
    article.set_article_id(article_id)
    article_dict = article.to_dict()
    fields = []
    values = []
    print(article_dict)
    for key, value in article_dict.items():
        if value is not None:
            fields.append(key)
            values.append(value)

    db.execute(
        action_type='alter',
        table='articles',
        fields=fields,
        values=values
    )
    return {"page": article.article_id}

@app.get('/set_comment')
async def set_comment():
    return {"page": "login"}

@app.get('/get_comment')
async def get_comment():
    return {'comments': {'1':1, '2':2}}

@app.get('/update_comment')
async def update_comment():
    return {'comments': {'1':1, '2':2}}

@app.get('/update_post')
async def update_post():
    return {'comments': {'1':1, '2':2}}

@app.get('/delete_post')
async def delete_post():
    return {'comments': {'1':1, '2':2}}

@app.get('/delete_comment')
async def delete_comment():
    return {'comments': {'1':1, '2':2}}