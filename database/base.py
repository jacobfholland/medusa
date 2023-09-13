from database.database import Database


db_instance = Database()
Base = db_instance.base
