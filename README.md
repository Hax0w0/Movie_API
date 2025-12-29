# Movie API README
**Project**: Movie API<br>
 **Contributers**: Raymond Gu<br>

## Introduction
This project is a RESTful API for managing and querying a movie dataset, built using FastAPI and SQLite. The goal of the project was to gain hands-on experience with REST API design while also learning how to deploy a Python backend to Microsoft Azure App Service.<br>

The API supports standard CRUD operations, including filtering and querying resources via URL parameters, and follows REST conventions such as resource-based routing and proper HTTP methods. The backend uses SQLite for simplicity and portability, making it easy to initialize and populate the database.

## How To Set Up Project (Local)
There is a `requirements.txt` file that contains all the dependencies needed to run this project. To create a virtual environment for this project, you can run the following code shown below:

```
$ python3 -m venv Virtual_Environment
$ .\Virtual_Environment\Scripts\Activate
$ pip install -r requirements.txt
```

### | Database Setup
The dataset used for this project is `Doula Isham Rashik Hasan`'s 9000+ Movies Dataset. The original CSV file for this dataset can be found in the `Movies.csv` file in the `Data_Files` folder.<br>

The code used to create the SQLite database is in `setup.py` in the `Database` folder. This code can be ran using the following command:

```
$ python .\Database\setup.py
```

### | Running API Locally
To run the API locally on your own computer, you can use the following command:

```
$ uvicorn main:app --reload
```

This should start the API and give you a link that looks like `http://127.0.0.1:8000`.

### | FastAPI Interactive Documentation
FastAPI automatically generates interactive API documentation based on the endpoint definitions and request/response models. Once the application is running, the documentations can be accessed by adding `/docs` as shown below:

```
http://127.0.0.1:8000/docs
```

## How To Set Up Project (Azure)
There is an `Azure_Deployment.zip` file that contains everything needed and can be manually deployed to Microsoft Azure App Service. The ZIP file contains the following folder and files:
- Classes
  - movie.py
  - update.py
- Database
  - Movies.db
  - setup.py
  - utils.py
- main.py
- requirements.txt

**Note**: When creating the `requirements.txt` file, I ran into many issues because I generated it on Windows. To avoid any issues when deploying to Azure, make sure this file uses `UTF-8` text encodings and `LF` line endings.

### | Creating Web App Service
First, we need to create the web app service.
1. Navigate to the search bar and search for "App Services".
2. Click on the "Create" button and select the "Web App" option.
3. Fill in the fields (the relevant ones are shown below):
    - Publish = Code
    - Runtime Stack = Python 3.11
    - Operating System = Linux
4. Review and create the web app.

Once the web app service is successfully deployed, we need to setup a few settings before manually deploying the ZIP file. In the "Environment variables" section, create 2 new environment variables. These variables will ensure that an environment for the web app service is built using Oryx during deployment (this does NOT happen by default).
- `SCM_DO_BUILD_DURING_DEPLOYMENT` = true
- `WEBSITE_RUN_FROM_PACKAGE` = 0

After that, we can manually deploy the ZIP file and run the app.
1. Navigate to the "Deployment" section and go to "Deployment Center".
2. For the "Source", choose "Publish files (new)".
3. Select the `Azure_Deployment.zip` file and click "Save".
4. Navigate to the "Settings" section and go to "Configuration".
5. Select the "Stack settings" tab and enter the "Startup command" shown below:
    - python -m uvicorn main:app --host 0.0.0.0 --port 8000
6. After that, click "Apply" and the API is all set up.

## Movies Dataset
As stated previously, this project uses the Kaggle 9000+ Movies Dataset. The original dataset consists of 9 features, but I only decided to use 8 of the 9 features for this project. Here are the features I chose to use and a description of each one:<br>

<table cellpadding="8" border="1">
  <tr>
    <th>Features</th>
    <th>Description</th>
  </tr>
  <tr>
    <td>Release_Date</td>
    <td>
      The date when the movie was released.
    </td>
  </tr>
  <tr>
    <td>Title</td>
    <td>
      The name of the movie.
    </td>
  </tr>
  <tr>
    <td>Overview</td>
    <td>
      A brief summary of the movie.
    </td>
  </tr>
  <tr>
    <td>Popularity</td>
    <td>
      A metric computed by TMDB developers based on various other important metrics such as number of views per day, number of users marked as "favorite", etc.
    </td>
  </tr>
  <tr>
    <td>Vote_Count</td>
    <td>
      The total aggregation of votes the movie received from users.
    </td>
  </tr>
  <tr>
    <td>Vote_Average</td>
    <td>
      Average rating based on vote count and the number of viewers (this metric is out of 10).
    </td>
  </tr>
  <tr>
    <td>Original_Language</td>
    <td>
      The original language of the movie. Dubbed versions are not considered to be original language.
    </td>
  </tr>
  <tr>
    <td>Genre</td>
    <td>
      Categories the movie can be classified as.
    </td>
  </tr>
</table>

**Note**: When inserting each movie into `Database.db`, each movie is also automatically given it's own unique `ID` that acts as the primary key.

## Movie API
As stated previously, this API is a RESTful interface for interacting with a movie dataset. It supports standard CRUD operations using appropriate HTTP methods and resource-based endpoints.

### | Method: `GET` /movies
**Description** This method returns a list of movies from the database.

**Output** The following features of each movie are returned in a JSON format.
- Title
- ID
- Release_Date
- Popularity
- Genre

**Query Parameters**: This method also supports optional query parameters.
- `genre`: Filter movies by genre (partial match).
- `sort`: Sort results by release date, popularity, or title.
- `order`: Sort results by ascending (ASC) or descending (DESC) order.
- `limit`: The number of movies to show.

Below is an example of a link to test this method when running the API locally.

```
http://127.0.0.1:8000/movies?genre=Action&sort=popularity&order=DESC&limit=10
```

### | Method: `GET` /movies/{movie_id}
**Description** This method returns a single movie by its unique identifier.

**Output**: If the movie exists, the response will contain a 200 status code.  Otherwise it will contain a 404 status code. This method will also return more details about the movie.
- ID
- Release_Date
- Title
- Overview
- Popularity
- Vote_Count
- Vote_Average
- Original_Language
- Genre

**Path Parameters**: To access a specific movie, you can use its unique id.
- `movie_id`: The unique ID of the movie.

Below is an example of a link to test this method when running the API locally.

```
http://127.0.0.1:8000/movies/100
```

### | Method: `POST` /movies
**Description** This method creates a new movie entry in the database.

**Output**: If the movie is succesfully created, the response will contain a 201 status code.
- ID
- Release_Date
- Title
- Overview
- Popularity
- Vote_Count
- Vote_Average
- Original_Language
- Genre

**Request Body**: To create a movie, you can specify each of its features in the request body in a JSON format.
- `Release_Date`: The release date of the movie.
- `Title`: The title of the movie.
- `Overview`: A brief description of the movie.
- `Popularity`: The popularity of the movie (based on other metrics like number of views per day, number of users marked as "favorite", etc).
- `Vote_Count`: The total aggregation of votes the movie received from users.
- `Vote_Average`: Average rating based on vote count and the number of viewers (this metric is out of 10).
- `Original_Language`: The original language of the movie.
- `Genre`: Categories the movie can be classified as.

To test this method, you can use Postman (use the desktop agent if running locally). When testing this method, make sure to add a header for `Content-Type` and set it to `application/JSON`. Below is an example of a valid request body that can be used to create a movie.

```
{
  "Release_Date": "2023-07-21",
  "Title": "Example Movie",
  "Overview": "A sample movie used for testing.",
  "Popularity": 123.45,
  "Vote_Count": 1500,
  "Vote_Average": 7.8,
  "Original_Language": "en",
  "Genre": "Drama"
}
```

### Method: `PUT` /movies/{movie_id}
**Description** This method updates an existing movie's details.

**Output**: If the movie is successfully updated, the response will contain a 200 status code. If the movie doesn't exist, the response will contain a 404 status code.
- ID
- Release_Date
- Title
- Overview
- Popularity
- Vote_Count
- Vote_Average
- Original_Language
- Genre

**Path Parameters**: To access a specific movie, you can use its unique id.
- `movie_id`: The unique ID of the movie.

**Request Body**: To update a movie, you can specify which fields to update in the request body in a JSON format.
- `Release_Date`: The release date of the movie.
- `Title`: The title of the movie.
- `Overview`: A brief description of the movie.
- `Popularity`: The popularity of the movie (based on other metrics like number of views per day, number of users marked as "favorite", etc).
- `Vote_Count`: The total aggregation of votes the movie received from users.
- `Vote_Average`: Average rating based on vote count and the number of viewers (this metric is out of 10).
- `Original_Language`: The original language of the movie.
- `Genre`: Categories the movie can be classified as.

Below is an example of a valid request body that can be used to update a movie.
```
{
  "Title": "Updated Movie",
  "Overview": "This movie's description has been updated."
}
```

### | Method: `DELETE` /movies/{movie_id}
**Description** This method deletes an existing movie from the database.

**Output**: If the movie is successfully deleted, the response will contain a 204 status code. If the movie doesn't exist, the response will contain a 404 status code.

**Path Parameters**: To access a specific movie, you can use its unique id.
- `movie_id`: The unique ID of the movie.

Below is an example of a link to test this method when running the API locally.

```
http://127.0.0.1:8000/movies/9827

```

