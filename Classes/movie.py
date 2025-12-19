from pydantic import BaseModel

class Movie(BaseModel):
    Release_Date: str
    Title: str
    Overview: str
    Popularity: float
    Vote_Count: int
    Vote_Average: float
    Original_Language: str
    Genre: str