import tinydb
from tinydb import TinyDB

db = TinyDB('./assets/oj_db.json', indent=4,
            ensure_ascii=False, sort_keys=True)
usercol = db.table('users')
