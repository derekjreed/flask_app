## API Reference


### `GET /actors  - Retrieve actors from the database`
### `Parameters: None`

#### `Curl`
```bash
localhost
curl -s -H "Authorization: Bearer ${TOKEN}" -X GET http://127.0.0.1:5000/actors

heroku
curl -s -H "Authorization: Bearer ${TOKEN}" -X GET https://capstone-agency-api33.herokuapp.com/actors
```
Get request response returns a json payload containing
- actors - a list of dictionaries
- each list contains:
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