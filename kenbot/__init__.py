#!/usr/bin/env python

import os
import os.path

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
import flask.ext.assets

__all__ = ['create_app', 'db']


def create_app(config=None):
    app = Flask(__name__)

    if config:
        app.config.from_pyfile(os.path.join(os.getcwd(), config))

    app.register_blueprint(views)

    asset_pkg = flask.ext.assets.Environment(app)
    asset_pkg.register('raphael', raphael)
    asset_pkg.register('app_js', app_js)
    asset_pkg.register('app_css', app_css)

    app.config['SQLALCHEMY_DATABASE_URI'] = app.config['DATABASE_URI']
    db.init_app(app)

    return app

db = SQLAlchemy()

from .views import views
from .assets import raphael, app_js, app_css
