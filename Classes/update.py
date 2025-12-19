from pydantic import BaseModel
from typing import Optional

class Update(BaseModel):
    Release_Date: Optional[str] = None
    Title: Optional[str] = None
    Overview: Optional[str] = None
    Popularity: Optional[float] = None
    Vote_Count: Optional[int] = None
    Vote_Average: Optional[float] = None
    Original_Language: Optional[str] = None
    Genre: Optional[str] = None