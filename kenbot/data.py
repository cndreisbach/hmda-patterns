from . import db

def msas():
    res = db.execute("SELECT cbsa_code, name FROM cbsa WHERE parent_code IS NULL")
    return res.fetchall()
