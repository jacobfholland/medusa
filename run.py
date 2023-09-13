# run.py
from database.database import Database
from database.import_models import import_models

db = Database()
import_models(db)
db.init_db()
