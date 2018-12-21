"""Routes module will have all endpoints associated with the flask application"""
from app import app

@app.route('/')
def index():
    """index returns at the index"""
    return "Hello, Backend!"