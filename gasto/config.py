import os

from decouple import config

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = config("SECRET_KEY", default=None)
    DEBUG = config("DEBUG", default=None)
