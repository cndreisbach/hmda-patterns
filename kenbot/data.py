from sqlalchemy import Table, MetaData

from . import db

meta = db.MetaData()

CBSA = db.Table('cbsa', db.metadata, autoload=True, autoload_with=db.engine)
HMDA = db.Table('hmda', db.metadata, autoload=True, autoload_with=db.engine)
State = db.Table('state', db.metadata, autoload=True, autoload_with=db.engine)
County = db.Table('county', db.metadata, autoload=True, autoload_with=db.engine)

