# Udacity Full-Stack Nanodegree: Capstone Project

## Content

1. [Motivation](#motivation)
2. [Deploy and run the project locally](#start-locally)
3. [API Documentation](#api)
4. [Authentification](#authentification)

<a name="motivation"></a>

## Motivation for the project

This is the last project of the `Udacity-Full-Stack-Nanodegree` Program.
It covers following technical topics in 1 app:

1. Database modeling was done with `PostgreSQL` & `SQLAlchemy` (see the `models.py` file)
2. An API that performs CRUD operations on database with the `Flask` Framework (see the `app.py` file)
3. There are also automated tests provided with `Unittest` (see the `test_app` file)
4. Authorization & Role based Authentification was made with the help of `Auth0` and its services (see the `auth.py` file)
5. Final goal to deploy to `Heroku` platform.

<a name="start-locally"></a>

## Deploy and run the project locally

To get started, make sure you `cd` into the correct directory, where all files of the application are located. Then proceed with the following steps to set it up.
Please take into account that, in order to run successfully the project, you will need the latest version of [Python 3](https://www.python.org/downloads/)
and [PostgreSQL](https://www.postgresql.org/download/) installed on your machine.

To start and run the local development server,

1. Initialize and activate a virtualenv:

```bash
$ pipenv shell
```

2. Install the dependencies:

```bash
$ pipenv run pip install -r requirements.txt
```

Please note that running this project locally means that it can´t access `Herokus` env variables.
To fix this, you need to edit a few informations in `config.py`, so it can
correctly connect to a local database

3. Change database config so it can connect to your local postgres database

- Open `config.py` with your editor of choice.
- Here you can see a global variable with the name `DATABASE_URI`:

```python
DATABASE_URL = "postgres://postgres:george2016@localhost:5432/project"
```

Where the follow syntax is followed:

```python
DATABASE_URL = "postgres://{username}:{password}@{host_and_port}/{database_name}"
```

- Just change `username`, `password` and `host_and_port` to whatever you choose while installing postgres. However, make sure that you already have started the PostgreSQL server in your system and that you have created the corresponding database in your system .
  > _tip_: `username` usually defaults to `postgres` and `port` always defaults to `localhost:5432` while installing PostgreSQL, most of the time you just need to change the `password`.

4. Setup Auth0
   If you only want to test the API (i.e. Project Reviewer), you can
   simply use the existing bearer tokens located in the `config.py` file.

If you already know your way around `Auth0`, just insert your own data
into the `config.py` file.

FYI: Here are the steps I followed to enable [authentification](#authentification).

5. (optional) Turn DEBUG mode on, which is included in the development environment:

```bash
$ export FLASK_ENV=development
```

6. Run the development server on `http://localhost:5000/`:

```bash
$ flask run
```

7. (optional) Execute the tests, to make sure everything works correctly:

```bash
$ python test_app.py
```

**WARNING!**

**Before running tests in, please ensure that you have exported an environment variable `DATABASE_URL` in your Command Prompt (CMD) or in your Terminal, and you have assigned it the value of your database URL just like in the `config.py` file.**

If you choose to run all tests, it should give this response, provided the fact that everything works correctly and as expected:

```bash
$ python test_app.py
.........................

Ran 25 tests in 15.235s

OK
```

## API Documentation

<a name="api"></a>

In this part of the document you can find and explore all existing endpoints, which methods can be used, how to work with them & example responses you will get. Furthermore, you can find about common error status codes, and the message that return.

- **Base URL**: https://udacity-fsnd-capstone-project.herokuapp.com/

- **Authentification**: Please see [API Authentification](#authentification-bearer) section for more information and details.

### **Available Endpoints**

Both `/movies` and `/actors` endpoints come with all the common HTTP methods (`GET`, `POST`, `DELETE`, `PATCH`).

### **How to work with each endpoint**

Click on a link to directly get to the ressource.

1. Actors
   1. [GET /actors](#get-actors)
   2. [POST /actors](#post-actors)
   3. [DELETE /actors](#delete-actors)
   4. [PATCH /actors](#patch-actors)
2. Movies
   1. [GET /movies](#get-movies)
   2. [POST /movies](#post-movies)
   3. [DELETE /movies](#delete-movies)
   4. [PATCH /movies](#patch-movies)

Each ressource documentation is clearly structured:

1. Description in a few words
2. `curl` example that can directly be used in terminal
3. More descriptive explanation of input & outputs.
4. Required permission
5. Example Response.

### Error Handling

Errors are return as JSON format in the following format:

```json
{
  "success": False,
  "error": 404,
  "message": "Not found"
}
```

The API will return six (6) error types when a request fails:

- 400: Bad request
- 401: Permissions not found
- 403: Forbidden
- 404: Not found
- 422: Unprocessable entity
- 500: Internal server error

###

# <a name="get-actors"></a>

### 1. GET /actors

Query paginated actors.

```bash
$ curl -X GET https://udacity-fsnd-capstone-project.herokuapp.com/actors?page1
```

- Fetches a list of dictionaries of examples in which the keys are the ids with all available fields
- Request Arguments:
  - **integer** `page` (10 actors per page)
- Request Headers: **None**
- Requires permission: `read:actors`
- Returns:
  1. List of dict of actors with following attributes:
     - **integer** `id`
     - **string** `name`
     - **string** `gender`
     - **integer** `age`
  2. **boolean** `success`

#### Example response

```json
{
  "actors": [
    {
      "age": 25,
      "gender": "John",
      "id": 1,
      "name": "Matthew"
    }
  ],
  "success": true
}
```

#### Errors

If you try fetch a page which does not have any actors, you will encounter an error which looks like this:

```bash
$ curl https://udacity-fsnd-capstone-project.herokuapp.com/actors?page123124
```

and it will return:

```json
{
  "error": 404,
  "message": "Not found",
  "success": false
}
```

# <a name="post-actors"></a>

### 2. POST /actors

Create a new actor and insert it into the database system.

```bash
$ curl -X POST https://udacity-fsnd-capstone-project.herokuapp.com/actors
```

- Request Arguments: **None**
- Request Headers: (_application/json_) 1. **string** `name` (<span style="color:red">_</span>required) 2. **integer** `age` (<span style="color:red">_</span>required) 3. **string** `gender`
- Requires permission: `create:actors`
- Returns:
  1. **integer** `id from newly created actor`
  2. **boolean** `success`

#### Example response

```json
{
  "created": 5,
  "success": true
}
```

#### Errors

If you try to create a new actor without a requiered field like `name`,
and it will throw a `422` error:

```bash
$ curl https://udacity-fsnd-capstone-project.herokuapp.com/actors?page123124
```

will return

```js
{
  "error": 422,
  "message": "Unprocessable entity",
  "success": false
}
```

# <a name="patch-actors"></a>

### 3. PATCH /actors

Edit an existing Actor

```bash
$ curl -X PATCH https://udacity-fsnd-capstone-project.herokuapp.com/actors/1
```

- Request Arguments: **integer** `id from actor you want to update`
- Request Headers: (_application/json_) 1. **string** `name` 2. **integer** `age` 3. **string** `gender`
- Requires permission: `edit:actors`
- Returns:
  1. **integer** `id from updated actor`
  2. **boolean** `success`
  3. List of dict of actors with following fields:
     - **integer** `id`
     - **string** `name`
     - **string** `gender`
     - **integer** `age`

#### Example response

```json
{
  "actor": [
    {
      "age": 27,
      "gender": "Female",
      "id": 1,
      "name": "Michaella"
    }
  ],
  "success": true,
  "updated": 1
}
```

#### Errors

If you try to update an actor with an invalid id, then it will throw an `404`error:

```bash
$ curl -X PATCH https://udacity-fsnd-capstone-project.herokuapp.com/actors/125
```

will return

```js
{
  "error": 404,
  "message": "Not found",
  "success": false
}
```

Additionally, trying to update an Actor with already existing field values will result in an `422` error:

```js
{
  "error": 422,
  "message": "Unprocessable entity",
  "success": false
}
```

# <a name="delete-actors"></a>

### 4. DELETE /actors

Delete an existing Actor

```bash
$ curl -X DELETE https://udacity-fsnd-capstone-project.herokuapp.com/actors/1
```

- Request Arguments: **integer** `id from actor you want to delete`
- Request Headers: `None`
- Requires permission: `delete:actors`
- Returns:
  1. **integer** `id from deleted actor`
  2. **boolean** `success`

#### Example response

```json
{
  "deleted": 5,
  "success": true
}
```

#### Errors

If you try to delete actor with an invalid id, then it will throw an `404`error:

```bash
$ curl -X DELETE https://udacity-fsnd-capstone-project.herokuapp.com/actors/125
```

It will return

```js
{
  "error": 404,
  "message": "Not found",
  "success": false
}
```

# <a name="get-movies"></a>

### 5. GET /movies

Query paginated all movies in the database system.

```bash
$ curl https://udacity-fsnd-capstone-project.herokuapp.com/movies?page1
```

- Fetches a list of dictionaries of examples in which the keys are the ids with all available fields
- Request Arguments:
  - **integer** `page` (optional, 10 movies per page, defaults to `1` if not given)
- Request Headers: **None**
- Requires permission: `read:movies`
- Returns:
  1. List of dict of movies with following fields:
     - **integer** `id`
     - **string** `name`
     - **date** `release_date`
  2. **boolean** `success`

#### Example response

```json
{
  "movies": [
    {
      "id": 1,
      "release_date": "Sun, 16 Feb 2020 00:00:00 GMT",
      "title": "Matthew first Movie"
    }
  ],
  "success": true
}
```

#### Errors

If you try fetch a page which does not have any movies, you will encounter an error which looks like this:

```bash
$ curl https://udacity-fsnd-capstone-project.herokuapp.com/movies?page123124
```

It will return

```json
{
  "error": 404,
  "message": "Not found",
  "success": false
}
```

# <a name="post-movies"></a>

### 6. POST /movies

Create a new Movie into the database system.

```bash
$ curl https://udacity-fsnd-capstone-project.herokuapp.com/movies
```

- Request Arguments: **None**
- Request Headers: (_application/json_) 1. **string** `title` (<span style="color:red">_</span>required) 2. **date** `release_date` (<span style="color:red">_</span>required)
- Requires permission: `create:movies`
- Returns:
  1. **integer** `id from newly created movie`
  2. **boolean** `success`

#### Example response

```json
{
  "created": 5,
  "success": true
}
```

#### Errors

If you try to create a new movie without a requiered field like `name`, then
it will throw a `422` error:

```bash
$ curl https://udacity-fsnd-capstone-project.herokuapp.com/movies?page123124
```

will return

```js
{
  "error": 422,
  "message": "Unprocessable entity",
  "success": false
}
```

# <a name="patch-movies"></a>

### 7. PATCH /movies

Edit an existing Movie information.

```bash
$ curl -X PATCH https://udacity-fsnd-capstone-project.herokuapp.com/movies/1
```

- Request Arguments: **integer** `id from movie you want to update`
- Request Headers: (_application/json_) 1. **string** `title` 2. **date** `release_date`
- Requires permission: `edit:movies`
- Returns:
  1. **integer** `id from updated movie`
  2. **boolean** `success`
  3. List of dict of movies with following fields:
     - **integer** `id`
     - **string** `title`
     - **date** `release_date`

#### Example response

```json
{
  "created": 1,
  "movie": [
    {
      "id": 1,
      "release_date": "Sun, 16 Feb 2020 00:00:00 GMT",
      "title": "Solarity x500"
    }
  ],
  "success": true
}
```

#### Errors

If you try to update an movie with an invalid id, then it will throw an `404`error:

```bash
$ curl -X PATCH https://udacity-fsnd-capstone-project.herokuapp.com/movies/125
```

It will return

```json
{
  "error": 404,
  "message": "Not found",
  "success": false
}
```

Additionally, trying to update an Movie with already existing field values will result in an `422` error:

```json
{
  "error": 422,
  "message": "Unprocessable entity",
  "success": false
}
```

# <a name="delete-movies"></a>

### 8. DELETE /movies

Delete an existing Movie.

```bash
$ curl -X DELETE https://udacity-fsnd-capstone-project.herokuapp.com/movies/1
```

- Request Arguments: **integer** `id from movie you want to delete`
- Request Headers: `None`
- Requires permission: `delete:movies`
- Returns:
  1. **integer** `id from deleted movie`
  2. **boolean** `success`

#### Example response

```json
{
  "deleted": 5,
  "success": true
}
```

#### Errors

If you try to delete movie with an invalid id, then it will throw an `404`error:

```bash
$ curl -X DELETE https://udacity-fsnd-capstone-project.herokuapp.com/movies/125
```

It will return

```json
{
  "error": 404,
  "message": "Not found",
  "success": false
}
```

# <a name="authentification"></a>

## Authentification

All API Endpoints are decorated with Auth0 permissions. So, to use the project locally, you need to config Auth0 accordingly.

### Auth0 for locally use

#### Create an App & API

1. Login to https://manage.auth0.com/
2. Click on Applications Tab
3. Create Application
4. Give it a name like `Me`, or something else that you would like, and select "Regular Web Application"
5. Go to Settings and find `domain`. Copy & paste it into `config.py` => AUTH0_DOMAIN=['AUTH0_DOMAIN'] (i.e. replace with `"example-me.eu.auth0.com"`)
6. Click on API Tab
7. Create a new API:
   1. Name: `Me`
   2. Identifier `Me`
   3. Keep Algorithm as it is
8. Go to Settings and find `Identifier`. Copy & paste it into config.py => API_AUDIENCE=['API_AUDIENCE'] (i.e. replace with `"Me"`)

#### Create Roles & Permissions

1. Before creating `Roles & Permissions`, you need to `Enable RBAC` in your API. To do that go to the `API` section, click on your `API Name`, go to the `Settings` tab and switch the `Enable RBAC` togle to on and finally `Save` those changes and the end of the page.
2. Also, check the button `Add Permissions in the Access Token`.
3. First, create a new Role under `Users and Roles` => `Roles` => `Create Roles`
4. Give it a descriptive name like `Casting Assistant`.
5. Go back to the API Tab and find your newly created API. Click on Permissions.
6. Create & assign all needed permissions accordingly
7. After you created all permissions this app needs, go back to `Users and Roles` => `Roles` and select the role you recently created.
8. Under `Permissions`, assign all permissions you want this role to have.

# <a name="authentification-bearer"></a>

### Auth0 to use existing API

If you want to access the real, temporary API, bearer tokens for all 3 roles are included in the `config.py` file.

## Existing Roles

They are 3 Roles with distinct permission sets:

1. Casting Assistant:

- view:actors: Can see all actors
- view:movies: Can see all movies

2. Casting Director (everything from Casting Assistant and)

- create:actors: Can create new Actors
- edit:actors: Can edit existing Actors
- delete:actors: Can remove existing Actors from database
- edit:movies: Can edit existing Movies

3. Exectutive Dircector (everything from Casting Director and)

- create:movies: Can create new Movies
- delete:movies: Can remove existing Motives from database

In your API Calls, add them as Header, with `Authorization` as key and the `Bearer token` as value. Don´t forget to also
prepend `Bearer` to the token (seperated by space).

For example: (Bearer token for `Executive Director`)

```json
{
  "Authorization": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InM2WDVjWXBzR3lFODlpdmkxUTk4XyJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtcHJvamVjdC5ldS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWVhMzMxYTIzZTNiYzIwYzA0NTYzNTM0IiwiYXVkIjoiYXV0aCIsImlhdCI6MTU4Nzg0ODU3MSwiZXhwIjoxNTg3ODU1NzcxLCJhenAiOiJRTXo4N2cwQndsQVBFQVVnNXdwWUF0UVdtVHBrWGx4OCIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiY3JlYXRlOmFjdG9ycyIsImNyZWF0ZTptb3ZpZXMiLCJkZWxldGU6YWN0b3JzIiwiZGVsZXRlOm1vdmllcyIsImVkaXQ6YWN0b3JzIiwiZWRpdDptb3ZpZXMiLCJyZWFkOmFjdG9ycyIsInJlYWQ6bW92aWVzIl19.lpYrDvrLemHV34CXxmpezd-K8-lZShcm7p-wwQeeUJ6Rd_TyLB751CYhNWFr6MEuYu6CZncm9F0lqvVU-oHBzsJS4Xo3EXsRSAtZlPEcXexhQgJEDVPxdb7ICFgxkCMMxnZa90KLg4XMHOIHqIQPDO63vP8kwy6g9_RdeMEHB5udzRTDy95Jx7fb55gCIdTrbwfzmTrZvM1nQMV5j74IfrOnohXnu2yHev_Cr-pEaTvBAZ6D1UwfcOX4tmn4ryTWhGOkFdWYC65M-rM4jbwDXBWihim8N3p2PNaLyDTqzFryOD0CXkiJmK4ii3b0rnKbUTSIDzGDUT-jzyxkKNipig"
}
```
