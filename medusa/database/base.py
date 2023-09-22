from .database import Database

db = Database()
Engine = db.engine
Base = db.base
