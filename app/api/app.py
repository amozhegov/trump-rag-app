# from dir app:
# uvicorn api.app:app --reload --host 0.0.0.0 --port 8000

# from frontend:
# npm run dev

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes import router

from logging_config import setup_logging

from db.session import init_db

setup_logging()
init_db()

app = FastAPI(
    title='Trump API',
    description='What does the greatest US president thinks of things?',
    version='0.0.1',
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(router)

app.get('/')
def root():
    return{
        'message':'Trump API',
        'docs':'/docs',
        'analyze': 'POST /analyze'
    }