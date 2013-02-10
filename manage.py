#!/usr/bin/env python

from flask.ext.script import Manager, Server, Option

from kenbot import create_app

manager = Manager(create_app)
manager.add_option('-D', '--db-uri', 
    dest='db_uri', 
    required=False,
    default='sqlite:///test.db',
    help="Connection URI for the database (like sqlite:///test.db)")
manager.add_command("runserver", Server())

if __name__ == "__main__":
    manager.run()
