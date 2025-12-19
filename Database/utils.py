import os
import sqlite3

def connect_to_database():

    # Create a local database file and connect to it
    path = os.path.join(os.path.dirname(__file__), "Movies.db")
    database = sqlite3.connect(path)

    # Make SQLite return rows as dictionary-like objects
    database.row_factory = sqlite3.Row

    return database