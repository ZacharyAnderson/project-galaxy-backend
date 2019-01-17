"""This module will contain all database models"""
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from hashlib import md5


class User(db.Model):
    """User class will contain id, username, email,\
     and password for individual users"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    displayname = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(
            password, method='pbkdf2:sha256', salt_length=8)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'\
            .format(digest, size)
