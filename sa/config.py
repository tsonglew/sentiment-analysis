# -*- coding: utf-8 -*-

import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    """common configuration"""
    SECRET_KEY = os.environ.get("SECRET_KEY") or "hard to guess string"
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_RECORD_QUERIES = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    """development configuration"""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('XUEER_COMMENTS') or "sqlite:///" + os.path.join(basedir, "data-dev.sqlite")

config = {
    "develop": DevelopmentConfig,
    "default": DevelopmentConfig
}

