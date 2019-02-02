"""datastore.py will take care of all database manipulation"""
from app import db
from app.models import User
from flask import jsonify


def createUser(json_dict):
    """createUser will only be executed if userName\
     and userEmail are unique and unused."""
    # Sets the userName, userEmail,
    # and userPassword to be used in user creation
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
        if User.query.filter_by(username=userName, email=userEmail)\
                .first() is not None:
            return jsonify({'msg': 'User ' + userName +
                            ' has been registered'}), 200
    except:
        return jsonify({'msg': 'User ' + userName +
                        ' has failed to register or is already registered.',
                        'status': 500, 'error': 'Internal Server Error'}), 500


def changeUserPassword(json_dict):
    """changeUserPassword will recieve a json object that will\
     confirm the old password and then set the new password."""
    userName = json_dict['username']
    oldPassword = json_dict['oldPassword']
    newPassword = json_dict['newPassword']

    user = User.query.filter_by(username=userName).first()
    if (user.check_password(oldPassword)):
        user.set_password(newPassword)
        db.session.commit()
        return jsonify({'msg': 'User ' + userName +
                        ' has successfully updated their password.'}), 200
    return jsonify({'msg': 'User ' + userName +
                    ' has failed to update their password.'}), 401
