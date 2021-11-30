## API Reference


### `GET /actors  - Retrieve actors from the database`
### `Parameters: None`

#### `Curl`
```bash
localhost
curl -s -H "Authorization: ${TOKEN}" -X GET http://127.0.0.1:5000/actors

heroku
curl -s -H "Authorization: ${TOKEN}" -X GET https://capstone-agency-api33.herokuapp.com/actors
```
Get request response returns a json payload containing
- actors - a list of dictionaries
- each dictionary contains:
    - age - an integer
    - gender - a string
    - id - an integer
    - name - a string

- success - a boolean
- total_actors - an integer


#### `Response Header`
```json
{
  "actors": [
    {
      "age": 52,
      "gender": "Male",
      "id": 1,
      "name": "Derek Rink"
    },
    {
      "age": 32,
      "gender": "Male",
      "id": 2,
      "name": "Jake Pound"
    }
  ],
  "success": true,
  "total_actors": 2
}

```
__Note:__ The output for GET with multiple records is paginated (5 records per page). To GET each page use the query URL parameter to view pages (e.g. ?page=integer)
#### `Page query`
```bash
curl -s -H "Authorization: ${EXECUTIVE_PRODUCE}" -X GET https://capstone-agency-api33.herokuapp.com/actors?page=2
{
  "actors": [
    {
      "age": 40,
      "gender": "Male",
      "id": 8,
      "name": "Joe Bloggs"
    },
    {
      "age": 40,
      "gender": "Male",
      "id": 9,
      "name": "Joe Bloggs"
    }
  ],
  "success": true,
  "total_actors": 7
}


```



### `GET /actors/<int:actor_id>  - Retrieve actor_id from the database`
### `Parameters: actor_id`

#### `Curl`
```bash
localhost
curl -s -H "Authorization: ${TOKEN}" -X GET http://127.0.0.1:5000/actors/1

heroku
curl -s -H "Authorization: ${TOKEN}" -X GET https://capstone-agency-api33.herokuapp.com/actors/1
```
Get request response returns a json payload containing
- a single dictionary instance
- the dictionary contains:
    - age - an integer
    - gender - a string
    - id - an integer
    - name - a string
- success - a boolean
- total_actors - an integer


#### `Response Header`
```json
{
  "actor": {
    "age": 39,
    "gender": "Male",
    "id": 1,
    "name": "Joe James Bloggs"
  },
  "success": true
}


```

### `DELETE /actors/<int:actor_id>  - Delete actor_id from the database`
### `Parameters: actor_id`

#### `Curl`
```bash
localhost
curl -s -H "Authorization: ${TOKEN}" -X DELETE http://127.0.0.1:5000/actors/5

heroku
curl -s -H "Authorization: ${TOKEN}" -X DELETE https://capstone-agency-api33.herokuapp.com/actors/5
```
Delete request response returns a json payload containing
- a single dictionary instance
- the dictionary contains:
    - deleted - an integer
    - success - a boolean


#### `Response Header`
```json
{
  "deleted": 5,
  "success": true
}


```

### `POST /actors  - Creates a new actor in the database`
### `Parameters: None`

#### `Curl`
```bash
localhost
curl -s -H "Authorization: ${TOKEN}" -H "Content-Type: application/json" -d '{"name": "Joe Bloggs", "age": 40, "gender": "Male"}' -X POST http://127.0.0.1:5000/actors

heroku
curl -s -H "Authorization: ${TOKEN}" -H "Content-Type: application/json" -d '{"name": "Joe Bloggs", "age": 40, "gender": "Male"}' -X POST https://capstone-agency-api33.herokuapp.com/actors
```
Post request response returns a json payload containing
- actors - a list of dictionaries
- each dictionary contains:
    - age - an integer
    - gender - a string
    - id - an integer
    - name - a string
- created - an integer
- success - a boolean
- total_actors - an integer


#### `Response Header`
```json
{
  "actors": [
    {
      "age": 39,
      "gender": "Male",
      "id": 1,
      "name": "Joe James Bloggs"
    },
    {
      "age": 32,
      "gender": "Male",
      "id": 2,
      "name": "Jake Pound"
    },
    {
      "age": 38,
      "gender": "Female",
      "id": 3,
      "name": "Clarissa Hunt"
    },
    {
      "age": 38,
      "gender": "Female",
      "id": 6,
      "name": "Clarissa Pint"
    },
    {
      "age": 40,
      "gender": "Male",
      "id": 7,
      "name": "Joe Bloggs"
    }
  ],
  "created": 9,
  "success": true,
  "total_actors": 7
}


```

#### `Created actor`
```bash
curl -s -H "Authorization: ${TOKEN}" -X GET https://capstone-agency-api33.herokuapp.com/actors/9
{
  "actor": {
    "age": 40,
    "gender": "Male",
    "id": 9,
    "name": "Joe Bloggs"
  },
  "success": true
}


```

### `PATCH /actors/<int:actor_id>  - Update an actor in the database`
### `Parameters: actor_id`

#### `Curl`
```bash
localhost
curl -s -H "Authorization: ${TOKEN}" -H "Content-Type: application/json" -d '{"name": "James Dean"}' -X PATCH http://127.0.0.1:5000/actors/1

heroku
curl -s -H "Authorization: ${TOKEN}" -H "Content-Type: application/json" -d '{"name": "James Dean"}' -X PATCH https://capstone-agency-api33.herokuapp.com/actors/1
```
Patch request response returns a json payload containing
- actors - a list of dictionaries
- each dictionary contains:
    - age - an integer
    - gender - a string
    - id - an integer
    - name - a string
- success - a boolean
- total_actors - an integer


#### `Response Header`
```json
{
  "actors": [
    {
      "age": 39,
      "gender": "Male",
      "id": 1,
      "name": "James Dean"
    },
    {
      "age": 32,
      "gender": "Male",
      "id": 2,
      "name": "Jake Pound"
    },
    {
      "age": 38,
      "gender": "Female",
      "id": 3,
      "name": "Clarissa Hunt"
    },
    {
      "age": 38,
      "gender": "Female",
      "id": 6,
      "name": "Clarissa Pint"
    },
    {
      "age": 40,
      "gender": "Male",
      "id": 7,
      "name": "Joe Bloggs"
    }
  ],
  "success": true,
  "total_actors": 7
}


```


### `GET /movies  - Retrieve movies from the database`
### `Parameters: None`

#### `Curl`
```bash
localhost
curl -s -H "Authorization: ${TOKEN}" -X GET http://127.0.0.1:5000/movies

heroku
curl -s -H "Authorization: ${TOKEN}" -X GET https://capstone-agency-api33.herokuapp.com/movies
```
Get request response returns a json payload containing
- movies - a list of dictionaries
- each dictionary contains:   
    - id - an integer
    - release_date - a datetime obj
    - title - a string
- success - a boolean
- total_movies - an integer


#### `Response Header`
```json
{
  "movies": [
    {
      "id": 1,
      "release_date": "Sat, 01 Jan 2022 00:00:00 GMT",
      "title": "Gums"
    },
    {
      "id": 2,
      "release_date": "Sat, 01 Apr 2023 00:00:00 GMT",
      "title": "Time to come"
    },
    {
      "id": 3,
      "release_date": "Sun, 01 May 2022 00:00:00 GMT",
      "title": "Time to stay"
    },
    {
      "id": 5,
      "release_date": "Sat, 01 Apr 2023 00:00:00 GMT",
      "title": "Time to come"
    },
    {
      "id": 6,
      "release_date": "Sun, 01 May 2022 00:00:00 GMT",
      "title": "Time to stay"
    }
  ],
  "success": true,
  "total_movies": 6
}


```

__Note:__ The output for GET with multiple records is paginated (5 records per page). To GET each page use the query URL parameter to view pages (e.g. ?page=integer)
#### `Page query`
```bash
curl -s -H "Authorization: ${EXECUTIVE_PRODUCE}" -X GET https://capstone-agency-api33.herokuapp.com/movies?page=2
{
  "movies": [
    {
      "id": 7,
      "release_date": "Sun, 01 May 2022 00:00:00 GMT",
      "title": "To be a genius"
    },
    {
      "id": 8,
      "release_date": "Thu, 03 Mar 2022 00:00:00 GMT",
      "title": "This will work"
    }
  ],
  "success": true,
  "total_movies": 7
}

```

### `GET /movies/<int:movie_id>  - Retrieve movie_id from the database`
### `Parameters: movie_id`

#### `Curl`
```bash
localhost
curl -s -H "Authorization: ${TOKEN}" -X GET http://127.0.0.1:5000/movies/1

heroku
curl -s -H "Authorization: ${TOKEN}" -X GET https://capstone-agency-api33.herokuapp.com/movies/1
```
Get request response returns a json payload containing
- a single dictionary instance
- the dictionary contains:
    - id - an integer
    - release_date - a datetime obj
    - title - a string
- success - a boolean
- total_movies - an integer


#### `Response Header`
```json
{
  "actor": {
    "age": 39,
    "gender": "Male",
    "id": 1,
    "name": "Joe James Bloggs"
  },
  "success": true
}


```

### `DELETE /movies/<int:movie_id>  - Delete movie_id from the database`
### `Parameters: movie_id`

#### `Curl`
```bash
localhost
curl -s -H "Authorization: ${TOKEN}" -X DELETE http://127.0.0.1:5000/movies/5

heroku
curl -s -H "Authorization: ${TOKEN}" -X DELETE https://capstone-agency-api33.herokuapp.com/movies/5
```
Delete request response returns a json payload containing
- a single dictionary instance
- the dictionary contains:
    - deleted - an integer
    - success - a boolean


#### `Response Header`
```json
{
  "deleted": 5,
  "success": true
}


```

### `POST /movies  - Creates a new movie in the database`
### `Parameters: None`

#### `Curl`
```bash
localhost
curl -s -H "Authorization: ${TOKEN}" -H "Content-Type: application/json" -d '{"title": "This will work", "release_date": "2022-03-03"}' -X POST http://127.0.0.1:5000/movies

heroku
curl -s -H "Authorization: ${TOKEN}" -H "Content-Type: application/json" -d '{"title": "This will work", "release_date": "2022-03-03"}' -X POST https://capstone-agency-api33.herokuapp.com/movies
```
Post request response returns a json payload containing
- movies - a list of dictionaries
- each dictionary contains:   
    - id - an integer
    - release_date - a datetime obj
    - title - a string
- created - an integer
- success - a boolean
- total_movies - an integer


#### `Response Header`
```json
{
  "movies": [
    {
      "id": 1,
      "release_date": "Sat, 01 Jan 2022 00:00:00 GMT",
      "title": "Gums"
    },
    {
      "id": 2,
      "release_date": "Sat, 01 Apr 2023 00:00:00 GMT",
      "title": "Time to come"
    },
    {
      "id": 3,
      "release_date": "Sun, 01 May 2022 00:00:00 GMT",
      "title": "Time to stay"
    },
    {
      "id": 5,
      "release_date": "Sat, 01 Apr 2023 00:00:00 GMT",
      "title": "Time to come"
    },
    {
      "id": 6,
      "release_date": "Sun, 01 May 2022 00:00:00 GMT",
      "title": "Time to stay"
    }
  ],
  "created": 8,
  "success": true,
  "total_movies": 7
}



```

#### `Created movie`
```bash
curl -s -H "Authorization: ${EXECUTIVE_PRODUCE}" -X GET https://capstone-agency-api33.herokuapp.com/movies/8
{
  "movie": {
    "id": 8,
    "release_date": "Thu, 03 Mar 2022 00:00:00 GMT",
    "title": "This will work"
  },
  "success": true
}


```



### `POST /movies  - Creates a new movie in the database`
### `Parameters: None`

#### `Curl`
```bash
localhost
curl -s -H "Authorization: ${TOKEN}" -H "Content-Type: application/json" -d '{"title": "This will work better"}' -X PATCH http://127.0.0.1:5000/movies/1

heroku
curl -s -H "Authorization: ${TOKEN}" -H "Content-Type: application/json" -d '{"title": "This will work better"}' -X PATCH https://capstone-agency-api33.herokuapp.com/movies/1
```
Post request response returns a json payload containing
- movies - a list of dictionaries
- each dictionary contains:   
    - id - an integer
    - release_date - a datetime obj
    - title - a string
- created - an integer
- success - a boolean
- total_movies - an integer


#### `Response Header`
```json
{
  "movies": [
    {
      "id": 1,
      "release_date": "Sat, 01 Jan 2022 00:00:00 GMT",
      "title": "This will work better"
    },
    {
      "id": 2,
      "release_date": "Sat, 01 Apr 2023 00:00:00 GMT",
      "title": "Time to come"
    },
    {
      "id": 3,
      "release_date": "Sun, 01 May 2022 00:00:00 GMT",
      "title": "Time to stay"
    },
    {
      "id": 5,
      "release_date": "Sat, 01 Apr 2023 00:00:00 GMT",
      "title": "Time to come"
    },
    {
      "id": 6,
      "release_date": "Sun, 01 May 2022 00:00:00 GMT",
      "title": "Time to stay"
    }
  ],
  "success": true,
  "total_movies": 7
}


```