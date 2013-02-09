from sqlalchemy import Table, MetaData

from . import db

meta = db.metadata
meta.reflect(bind=db.engine)

tables = db.metadata.tables

connection = None

HMDA = db.Table('hmda', meta, autoload=True, autoload_with=db.engine)
CBSA = db.Table('cbsa', meta, autoload=True, autoload_with=db.engine)
State = db.Table('state', meta, autoload=True, autoload_with=db.engine)
County = db.Table('county', meta, autoload=True, autoload_with=db.engine)

def conn():
    global connection
    if connection is None:
        connection = db.engine.connect()
    return connection
