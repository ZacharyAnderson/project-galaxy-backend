"""Routes module will have all endpoints associated with \
the flask application"""
from app import app, db
from app.models import User
from app.datastore import createUser, changeUserPassword
from flask import jsonify, request
from flask_jwt_extended import jwt_required, \
    create_access_token, get_jwt_identity
from werkzeug.utils import secure_filename
from .recipes_bucket import upload_file_to_s3, allowed_file, list_users_files
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


@app.route('/api/v1.0/user/resetpassword', methods=['POST'])
@jwt_required
def reset_password_request():
    """Change password will change the users password"""
    current_user = get_jwt_identity()
    if (request.data):
        json_dict = json.loads(request.data)
        return changeUserPassword(json_dict)
    return jsonify({'msg': 'missing json body.'}), 401


@app.route('/api/v1.0/user', methods=["GET"])
@jwt_required
def user_settings():
    """Route will show user settings"""
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user).first()
    return jsonify(current_user=current_user, email=user.email), 200


@app.route('/api/v1.0/user/recipe', methods=["POST"])
@jwt_required
def upload_file():
    """POST Route will allow uploading of recipe files"""
    if "user_file" not in request.files:
        return "No user_file key in request.files"
    file = request.files["user_file"]

    if file.filename == "":
        return "Please selet a file"

    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user).first()

    if file and allowed_file(file.filename):
        file.filename = secure_filename(file.filename)
        output = upload_file_to_s3(
            file, app.config["S3_BUCKET"], user.username)
        return jsonify(file_location=str(output)), 200
    else:
        return jsonify({'msg': "File does not exist or the file type\
                        is not allowed."}), 401


@app.route('/api/v1.0/<username>/recipes', methods=["GET"])
def list_files(username):
    """GET Route lists all users uploaded files.
       Returns a list of tuples with(key, datetime, file_size)
    """
    file_list = list_users_files(app.config["S3_BUCKET"], username)
    return str(file_list)
