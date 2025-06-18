import os

from decouple import config

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = config("SECRET_KEY", default=None)
    DEBUG = config("DEBUG", default=None)
    SQLALCHEMY_DATABASE_URI = config(
        "SQLALCHEMY_DATABASE_URI",
        default=f"sqlite:///{os.path.join(basedir, 'database.sqlite')}",
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = config(
        "SQLALCHEMY_TRACK_MODIFICATIONS", default=False
    )
