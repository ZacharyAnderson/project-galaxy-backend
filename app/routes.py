"""Routes module will have all endpoints associated with the flask application"""
from app import app, db
from app.models import User
from flask import jsonify, request
import json


@app.route('/')
def index():
    """index returns at the index"""
    return "Hello, Backend!"


@app.route('/api/v1.0/registration/username/<username>', methods=['GET'])
def isUsernameUnique(username):
    """isUsernameUnique will return a json object if the username trying to be registered is not used."""
    users = User.query.all()
    for u in users:
        if(u.username == username):
            return jsonify({'isUnique': False})
    return jsonify({'isUnique': True})


@app.route('/api/v1.0/registration/email/<email>', methods=['GET'])
def isEmailUnique(email):
    """isEmailUnique will return a json object if the email trying to be registered is not used."""
    users = User.query.all()
    for u in users:
        if(u.email == email):
            return jsonify({'isUnique': False})
    return jsonify({'isUnique': True})


@app.route('/api/v1.0/registration', methods=['POST'])
def registerUser():
    """registerUser will register the user to project-galaxy"""
    if request.method == "POST":
        json_dict = json.loads(request.data)

        userName = json_dict['userName']
        userEmail = json_dict['userEmail']
        userPassword = json_dict['userPassword']

        print(userName + '\n' + userEmail + '\n' + userPassword)

        return jsonify({'didItWork': True})
