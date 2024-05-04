from pathlib import Path

from tinydb import TinyDB

db_path = Path('./assets/oj_db.json')

if not db_path.exists():
    db_path.parent.mkdir(parents=True, exist_ok=True)

    db_path.touch(exist_ok=True)
    db_path.write_text('{}', 'utf-8')

db = TinyDB('./assets/oj_db.json', indent=4,
            ensure_ascii=False, sort_keys=True)
usercol = db.table('users')
contestscol = db.table('contests')
