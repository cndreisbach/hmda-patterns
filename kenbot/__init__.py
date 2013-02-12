#!/usr/bin/env python

import os, os.path

from flask import Flask, g
import flask.ext.assets
import sqlsoup


from .views import views
from .assets import raphael, app_js, app_css

def create_app(config=None):
    app = Flask(__name__)
    
    if config:        
        app.config.from_pyfile(os.path.join(os.getcwd(), config))

    app.register_blueprint(views)

    asset_pkg = flask.ext.assets.Environment(app)
    asset_pkg.register('raphael', raphael)
    asset_pkg.register('app_js', app_js)
    asset_pkg.register('app_css', app_css)

    @app.before_request
    def connect_to_db():
        g.db = sqlsoup.SQLSoup(app.config['DATABASE_URI'])

    @app.teardown_request
    def close_db_connection(error=None):
        g.db.session.remove()

    return app
    


