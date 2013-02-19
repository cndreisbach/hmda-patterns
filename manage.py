#!/usr/bin/env python

from flask.ext.script import Manager, Server
from flask.ext.assets import ManageAssets
from kenbot import create_app

manager = Manager(create_app)
manager.add_option('-c', '--config',
                   dest='config',
                   required=False,
                   help='Path to configuration file.',
                   default='sample_config.py')
manager.add_command("runserver", Server())
manager.add_command("assets", ManageAssets())

if __name__ == "__main__":
    manager.run()
