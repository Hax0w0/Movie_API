import os
import csv
import sqlite3

def initialize_database():

    # Create a local database file and connect to it
    path = os.path.join(os.path.dirname(__file__), "Movies.db")
    database = sqlite3.connect(path)
    cursor = database.cursor()

    # Define the movie table schema
    movie_columns = """
        ID                  INTEGER PRIMARY KEY AUTOINCREMENT,
        Release_Date        TEXT NOT NULL,
        Title               TEXT NOT NULL,
        Overview            TEXT NOT NULL,
        Popularity          FLOAT NOT NULL,
        Vote_Count          INTEGER NOT NULL,
        Vote_Average        FLOAT NOT NULL,
        Original_Language   TEXT NOT NULL,
        Genre               TEXT NOT NULL
        """

    # Create the table
    movie_table_schema = f"CREATE TABLE IF NOT EXISTS movies ({movie_columns})"
    cursor.execute(movie_table_schema)

    # Save changes and close
    database.commit()
    database.close()

    return

def populate_database():

    # Create a local database file and connect to it
    path = os.path.join(os.path.dirname(__file__), "Movies.db")
    database = sqlite3.connect(path)
    cursor = database.cursor()
    
    # Get the path to the movie dasta
    movies_csv = os.path.join(os.path.dirname(__file__),
                              "..", "Data_Files", "Movies.csv")
    
    # Read the CSV file
    with open(movies_csv, newline='', encoding='utf-8') as f:

        # Normalize unusual line separators
        content = f.read()

        # Create the reader and get the column headers
        reader = csv.reader(content.splitlines())

        # Isolate the relevant column headers
        headers = next(reader)
        relevant_headers = headers[:-1]

        # Create the template for inserting
        insert_sql = f"""
            INSERT INTO movies ({", ".join(relevant_headers)})
            VALUES ({", ".join(["?"] * len(relevant_headers))})
            """

        # Go through each row of the dataset
        for row in reader:

            # Keep only relevant columns
            relevant_columns = row[0:8]
            cursor.execute(insert_sql, relevant_columns)

    # Save changes and close
    database.commit()
    database.close()

def setup():

    print("Database Setup:")

    print("\t Creating tables...")
    initialize_database()

    print("\t Populating tables...")
    populate_database()

    print("\t Database setup complete ✔")

if __name__ == "__main__":
    setup()