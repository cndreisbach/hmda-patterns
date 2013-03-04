#!/usr/bin/env python

from flask.ext.script import Manager, Server, Command
from flask.ext.assets import ManageAssets
from hmda_tools import data
from hmda_tools.data import geo, cbsa
from kenbot import create_app


class SyncDB(Command):
    """Create the database schema and load join tables."""
    def run(self):
        from flask import current_app
        db_uri = current_app.config['SQLALCHEMY_DATABASE_URI']
        print "Creating schemas..."
        data.create_schemas(db_uri)
        print "Loading code sheet..."
        data.load_code_sheet(db_uri)
        print "Downloading & loading MSA data..."
        cbsa.load_cbsa(db_uri)
        print "Downloading & loading geographic data..."
        geo.load_all(db_uri)


manager = Manager(create_app)
manager.add_option('-c', '--config',
                   dest='config',
                   required=False,
                   help='Path to configuration file.',
                   default='sample_config.py')
manager.add_command("runserver", Server())
manager.add_command("assets", ManageAssets())
manager.add_command("syncdb", SyncDB())


if __name__ == "__main__":
    manager.run()
