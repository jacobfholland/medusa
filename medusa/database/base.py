from .database import Database

db = Database()  # Create an instance of the Database class.

# Get the database engine and base from the Database instance.
# These will be used by the Model class to register the model with the database.
Engine = db.engine
"""Database engine (connection)"""

Base = db.base
"""Database declarative base used in model registration"""
