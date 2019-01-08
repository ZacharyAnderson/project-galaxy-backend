"""datastore.py will take care of all database manipulation"""
from app import db
from app.models import User
from flask import jsonify


def createUser(json_dict):
    """createUser will only be executed if userName and userEmail are unique and unused."""
    # Sets the userName, userEmail, and userPassword to be used in user creation
    userName = json_dict['username']
    userEmail = json_dict['useremail'].lower()
    userPassword = json_dict['userpassword']
    # creates the user object and adds the user to the database
    try:
        user = User(username=userName, email=userEmail, displayname=userName)
        user.set_password(userPassword)
        db.session.add(user)
        db.session.commit()
        # confirms the user was added successfully then returns a status code
        if User.query.filter_by(username=userName, email=userEmail).first() is not None:
            return jsonify({'message': 'User ' + userName + ' has been registered'}), 200
    except:
        return jsonify({'message': 'User ' + userName + ' has failed to register or is already registered.', 'status': 500, 'error': 'Internal Server Error'}), 500
