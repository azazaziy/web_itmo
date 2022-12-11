from src.postgres.postgres_helper import PostgresHelper
from src.json_helper.serializer import MessageSerializer
import uvicorn
import requests
from typing import Optional, List
from datetime import datetime
import json
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
        login,
        password
):
    response = {
            'headers':
                {
                    'from_dict': True,
                    'table': 'users',
                    'action_type': 'insert',
                },
            'data':
                {
                    'login': f"'{login}'",
                    'password': f"'{password}'",
                }
        }
    s_one = {
        'headers':
            {
                'action_type': 'select_one',
                'table': 'users'
            },
        'data':
            {
                'values': 'login',
                'conditions': {'login':f"'{login}'"}
            }
    }
    article_id = db.execute(**s_one)
    if article_id:
        return {"error": 'existed_login'}
    else:
        resp = db.execute(**response)
        return{'resp': resp}

@app.get('/login')
async def login(
        login,
        password
):
    response = {
            'headers':
                {
                    'from_dict': True,
                    'table': 'users',
                    'action_type': 'insert',
                },
            'data':
                {
                    'login': f"'{login}'",
                    'password': f"'{password}'",
                }
        }
    s_one = {
        'headers':
            {
                'action_type': 'select_one',
                'table': 'users'
            },
        'data':
            {
                'values': 'password',
                'conditions': {'login':f"'{login}'"}
            }
    }
    passw = db.execute(**s_one)
    if password == passw:
        return {"done": 'ok'}
    else:
        return{'failed': 'failed'}

@app.get('/set_data')
async def set_data(
    author,
    title,
    text,
    image,
):

    response = json.dumps(
        {
            'headers':
                {
                    'table': 'articles',
                    'action_type': 'insert',
                    'from_dict': True,
                },
            'data':
                {
                    'author': {'value':author,'type':'str'},
                    'title': {'value':title,'type':'str'},
                    'text': {'value':text,'type':'str'},
                    'image': {'value':image,'type':'str'},
                    'timestamp': {'value':str(datetime.now()),'type':'str'},
                    'tags': {'value':['some tag'],'type':'list'},
                    'article_id': {'value':'article_id','type':'int'},
                    'editors': {'value':None,'type':'list'},
                    'moderators': {'value':None,'type':'list'}
                }
        }
    )
    article = MessageSerializer(response)
    db.execute(**article.as_dict())
    return {"status": 'added successfully'}

@app.get('/get_one')
async def get():
    return {'comments': {'1':1, '2':2}}

@app.get('/get_all')
async def get():
    return {'comments': {'1':1, '2':2}}

@app.get('/update')
async def update():
    return {'comments': {'1':1, '2':2}}

@app.get('/delete')
async def delete():
    return {'comments': {'1':1, '2':2}}

@app.get('/new_id')
async def new_id(
        field,
        table
):
    s_one = {
        'headers':
            {
                'action_type': 'select_one',
                'table':table
            },
        'data':
            {
                'values': 'MAX({field}_id)',
                'table': 'articles'
            }
    }
    s_one['data']['values'] = s_one['data']['values'].format(field = field)
    id = db.execute(**s_one) + 1
    return {'id': id}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)