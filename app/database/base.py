from app.database.database import Database


# Creates the SQLAlachemy declarative base while avoiding circular import errors
db_instance = Database()
Base = db_instance.base
