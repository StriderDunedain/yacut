import os
import re

BASE_ROUTE = 'http://localhost/'
CUSTOM_LENGTH_REGEX = re.compile(r'^[a-zA-Z0-9]{1,16}$')
DEFAULT_LENGTH = 6


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', default='sqlite:///db.sqlite3')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY', default='SECRET_KEY')
