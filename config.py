import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
   
    ## How this will be deployed after Dev
    ## SECRET_KEY = os.environ.get('PROJECT-GALAXY-BACKEND-SECRET-KEY')
    ## For now we will set the key manually for Development purposes
    
    SECRET_KEY = '\x82\xc5\xac-EC\xf5\x92\x11w\xe2\x18 )k\x82.\xcc\xf8 g7fA\x86~\xa7c\xd6\xfdQ\x7f\xed\xe2e21\xd5\xa5\xf6QzMg?\x85\x1e\xd5'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False