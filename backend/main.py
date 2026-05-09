from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database.init_db import init_db
from routes import detect, chatbot, history

from fastapi.staticfiles import StaticFiles

app = FastAPI(title='NightVision Guardian AI', description='AI-Powered Night Surveillance API')

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:5173', 'http://127.0.0.1:5173'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

import os
os.makedirs('uploads', exist_ok=True)
os.makedirs('enhanced', exist_ok=True)
os.makedirs('results', exist_ok=True)

app.mount("/static/uploads", StaticFiles(directory="uploads"), name="static_uploads")
app.mount("/static/enhanced", StaticFiles(directory="enhanced"), name="static_enhanced")
app.mount("/static/results", StaticFiles(directory="results"), name="static_results")

@app.on_event('startup')
def on_startup():
    init_db()

@app.get('/')
def read_root():
    return {'message': 'Welcome to NightVision Guardian AI API'}

app.include_router(detect.router)
app.include_router(chatbot.router)
app.include_router(history.router)