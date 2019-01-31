"""Routes module will have all endpoints associated with \
the flask application"""
from app import app, db
from app.models import User
from app.datastore import createUser
from flask import jsonify, request
from flask_jwt_extended import jwt_required, \
    create_access_token, get_jwt_identity
import json


@app.route('/')
def index():
    """index returns at the index"""
    return "Hello, Backend!"


@app.route('/api/v1.0/registration/username/<username>', methods=['GET'])
def isUsernameUnique(username):
    """isUsernameUnique will return a json object if the username\
     trying to be registered is not used."""
    user = User.query.filter_by(username=username).first()
    if user is not None:
        return jsonify({'isUnique': False})
    return jsonify({'isUnique': True})


@app.route('/api/v1.0/registration/email/<email>', methods=['GET'])
def isEmailUnique(email):
    """isEmailUnique will return a json object if the email\
     trying to be registered is not used."""
    user = User.query.filter_by(email=email.lower()).first()
    if user is not None:
        return jsonify({'isUnique': False})
    return jsonify({'isUnique': True})


@app.route('/api/v1.0/registration', methods=['POST'])
def registerUser():
    """registerUser will register the user to project-galaxy"""
    if request.method == "POST":
        json_dict = json.loads(request.data)
        return createUser(json_dict)


@app.route('/api/v1.0/login', methods=['GET'])
def login():
    """login will handle the authentication tokens for the user"""
    username = request.headers.get('username', None)
    password = request.headers.get('password', None)
    if not username:
        return jsonify({"msg": "Missing username parameter"}), 400
    if not password:
        return jsonify({"msg": "Missing password parameter"}), 400
    # First test to see if the username is correct
    user = User.query.filter_by(username=username).first()
    if user is not None:
        if user.check_password(password):
            access_token = create_access_token(identity=username)
            return jsonify(access_token=access_token,
                           current_user=user.displayname,
                           email=user.email,
                           avatar=user.avatar(80)), 200
    # If the username is not correct test if the email is being used
    user = User.query.filter_by(email=username.lower()).first()
    if user is not None:
        if user.check_password(password):
            access_token = create_access_token(identity=username)
            return jsonify(access_token=access_token,
                           current_user=user.displayname,
                           email=user.email,
                           avatar=user.avatar(80)), 200
    return jsonify({"msg": "Bad username or password"}), 401


@app.route('/api/v1.0/user', methods=["GET"])
@jwt_required
def user_settings():
    """Route will show user settings"""
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user).first()
    return jsonify(current_user=current_user, email=user.email), 200
