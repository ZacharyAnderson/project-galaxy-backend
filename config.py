"""This module creates the config object"""
import os
import datetime

BASEDIR = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    """This class will be used to configure the flask application"""
    # How this will be deployed after Dev
    # SECRET_KEY = os.environ.get('PROJECT-GALAXY-BACKEND-SECRET-KEY')
    # For now we will set the key manually for Development purposes
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    S3_BUCKET = os.environ.get('PROJECT_GALAXY_TEST_BUCKET')
    AWS_KEY = os.environ.get('AWS_ACCESS_KEY')
    AWS_SECRET_KEY = os.environ.get('AWS_SECRET_KEY')
    S3_LOCATION = 'http://{}.s3.amazonaws.com/'.format(S3_BUCKET)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = '\x82\xc5\xac-EC\xf5\x92\x11w\xe2\x18 )k\x82.\xcc\xf8 \
    g7fA\x86~\xa7c\xd6\xfdQ\x7f\xed\xe2e21\xd5\xa5\xf6QzMg?\x85\x1e\xd5'
    JWT_SECRET_KEY = "\x88\x99\xdc\x0e\xb4\x07\x8d\xe3\xe4\x03\x1d\xcd$\
    \x00\n\xf6\x95\x19\x0cI\xf5\xf5'\xda"
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(days=1)
