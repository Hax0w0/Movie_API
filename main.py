from fastapi import FastAPI, status, HTTPException
from typing import Optional
from Database.utils import *
from Classes.movie import *
from Classes.update import *

app = FastAPI()

@app.get("/movies")
def get_movies(genre: Optional[str] = None,
               sort: Optional[str] = None,
               order: Optional[str] = "ASC",
               limit: Optional[int] = None):

    # Connect to the database
    database = connect_to_database()
    cursor = database.cursor()

    # Define variables to help set up query
    relevant_columns = "Title, ID, Release_Date, Popularity, Genre"
    base_query = f"SELECT {relevant_columns} FROM movies"
    params = []

    # If a genre is provided, add it as a condition
    if genre:
        base_query += " WHERE LOWER(Genre) LIKE LOWER(?)"
        params.append(f"%{genre}%")

    # If the user wants to sort, add it to the query
    if (sort) and (order.upper() in ["DESC", "ASC"]):
        sort = sort.upper()
        order = order.upper()

        if sort == "RELEASE_DATE":
            base_query += f" ORDER BY date(Release_Date) {order}"

        elif sort == "POPULARITY":
            base_query += f" ORDER BY CAST(Popularity AS REAL) {order}"

        elif sort == "TITLE":
            base_query += f" ORDER BY Title {order}"

    # If a limit is provided, add it to the query
    if limit is not None and limit > 0:
        base_query += " LIMIT ?"
        params.append(limit)

    # Execute the query and parse the response
    cursor.execute(base_query, params)
    rows = cursor.fetchall()
    movies = [dict(row) for row in rows]

    # Close the connection to the database
    database.close()

    return movies

@app.get("/movies/{movie_id}")
def get_movie(movie_id: int):

    # Connect to the database
    database = connect_to_database()
    cursor = database.cursor()

    # Execute the query and parse the response
    cursor.execute("SELECT * FROM movies WHERE id = ?", (movie_id,))
    movie = cursor.fetchone()

    # Close the database connection
    database.close()

    # Raise an exception if the movie ID is invalid
    if movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")

    return dict(movie)
    
@app.post("/movies", status_code=status.HTTP_201_CREATED)
def create_movie(movie: Movie):

    # Connect to the database
    database = connect_to_database()
    cursor = database.cursor()

    # Specify the columns and their values
    columns = """
        Release_Date,
        Title,
        Overview,
        Popularity,
        Vote_Count,
        Vote_Average,
        Original_Language,
        Genre
        """
    
    values = (movie.Release_Date,
              movie.Title,
              movie.Overview,
              movie.Popularity,
              movie.Vote_Count,
              movie.Vote_Average,
              movie.Original_Language,
              movie.Genre)

    # Create the query and execute
    query = f"""INSERT INTO movies ({columns})
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)"""
    cursor.execute(query, values)

    # Commit changes, get movie ID, and close connection
    database.commit()
    movie_id = cursor.lastrowid
    database.close()

    return {"id": movie_id, **movie.model_dump()}

@app.put("/movies/{movie_id}", status_code=status.HTTP_200_OK)
def update_movie(movie_id: int, update: Update):

    # Connect to the database
    database = connect_to_database()
    cursor = database.cursor()

    # Check if the movie exists
    cursor.execute("SELECT * FROM movies WHERE ID = ?", (movie_id,))
    existing_movie = cursor.fetchone()
    if not existing_movie:
        database.close()
        raise HTTPException(status_code=404, detail="Movie not found")

    # Build query dynamically for fields that are provided
    fields = []
    values = []
    for key, value in update.model_dump(exclude_unset=True).items():
        fields.append(f"{key} = ?")
        values.append(value)
    values.append(movie_id)

    # Create the query and execute
    if fields:
        query = f"UPDATE movies SET {', '.join(fields)} WHERE id = ?"
        cursor.execute(query, values)
        database.commit()

    # Fetch updated movie
    cursor.execute("SELECT * FROM movies WHERE id = ?", (movie_id,))
    updated_movie = dict(cursor.fetchone())
    database.close()

    return updated_movie

@app.delete("/movies/{movie_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_movie(movie_id: int):

    # Connect to the database
    database = connect_to_database()
    cursor = database.cursor()

    # Check if the movie exists
    cursor.execute("SELECT * FROM movies WHERE ID = ?", (movie_id,))
    existing_movie = cursor.fetchone()
    if not existing_movie:
        database.close()
        raise HTTPException(status_code=404, detail="Movie not found")

    # Delete the movie
    cursor.execute("DELETE FROM movies WHERE id = ?", (movie_id,))
    database.commit()
    database.close()

    return
