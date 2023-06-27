"""[General Configuration Params]
"""
from os import environ, path
import os
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))

load_dotenv(path.join(basedir, ".env"))


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = "th15i5th3c0nf19p01nt-s3Cr3t-k3YS"
    SQLALCHEMY_DATABASE_URI = os.environ["DATABASE_URL"]
    SQLALCHEMY_TRACK_MODIFICATIONS = os.environ["SQLALCHEMY_TRACK_MODIFICATIONS"]
    JWT_SECRET_KEY = os.environ["JWT_SECRET_KEY"]
    JWT_ACCESS_TOKEN_EXPIRES = os.environ["JWT_ACCESS_TOKEN_EXPIRES"]
    JSON_SORT_KEYS = False
    # UPLOAD_FOLDER = os.environ["UPLOAD_FOLDER"]
    UPLOAD_FILE = os.environ["UPLOAD_FILE"]
    URL = os.environ["URL"]
    # MAIL_MAILER = os.environ["MAIL_MAILER"]
    # MAIL_SERVER = os.environ["MAIL_SERVER"]
    # MAIL_PORT = os.environ["MAIL_PORT"]
    # MAIL_USERNAME = os.environ["MAIL_USERNAME"]
    # MAIL_PASSWORD = os.environ["MAIL_PASSWORD"]
    # MAIL_DEFAULT_SENDER = os.environ["MAIL_DEFAULT_SENDER"]
    # MAIL_FROM_NAME = os.environ["MAIL_FROM_NAME"]
    # MAIL_ENCRYPTION = os.environ["MAIL_ENCRYPTION"]
    # MAIL_USE_SSL = os.environ["MAIL_USE_SSL"]


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
