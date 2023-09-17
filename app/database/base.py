from .database import Database


db = Database()  # Create an instance of the Database class.

# Get the database engine and base from the Database instance.
# These will be used by the Model class to register the model with the database.
Engine = db.engine
Base = db.base
