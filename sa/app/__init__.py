# -*- coding: utf-8 -*-

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_debugtoolbar import DebugToolbarExtension
from config import config


app = Flask(__name__)
config_name = 'default'
app.config.from_object(config[config_name])
config[config_name].init_app(app)
toolbar = DebugToolbarExtension(app)


db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'


# admin site
from admin import views

from auth import auth
app.register_blueprint(auth, url_prefix="/auth")
