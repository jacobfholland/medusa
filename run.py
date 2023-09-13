# run.py
from app.database.database import Database
from app.database.import_models import import_models

db = Database()
import_models(db)
db.init_db()
