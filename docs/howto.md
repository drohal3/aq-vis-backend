# HOWTO: Admin authentication
To obtain Bearer token, call `POST` to the  `/admin/token` endpoint with the following form data:
- grant_type: password
- username: `<username>`
- password: `<password>`

example:
```
curl -X 'POST' \
  'http://127.0.0.1:8080/admin/token' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'grant_type=password&username=test&password=test'
```

response:
```json
{
    "access_token": "Abc123",
    "token_type": "Bearer"
}
```

The obtained token is used to authorize the requests requiring admin privileges.

example:
```
curl -X 'GET' \
  'http://domain.com/admin/example\
  -H 'accept: application/json' \
  -H 'Authorization: Bearer abc123'
```
> Notice the `Authorization` header.

> **Note:** the token is valid only for the time specified in the API application configuration. After receiving `401 Unauthorized` response it must be renewed.

# HOWTO: Create user
> **Note:** [Admin authentication](howto) is required!

Send a `POST` HTTP request to `/admin/users` endpoint.

Example request body:
```json
{
  "disabled": false,
  "email": "example@test.com",
  "full_name": "Example User",
  "password": "string123",
  "username": "string"
}
```

Response:
```json
{
    "email": "example@test.com",
    "full_name": "Example User",
    "disabled": false,
    "organisation": null,
    "id": "667c23e9bf24f7e4c474fd1c"
}
```

# HOWTO: Create user
> **Note:** [Admin authentication](howto) is required!

Send a `POST` HTTP request to `/admin/users` endpoint.

Example request body:
```json
{
  "disabled": false,
  "email": "example@test.com",
  "full_name": "Example User",
  "password": "string123",
  "username": "string"
}
```

Response:
```json
{
    "email": "example@test.com",
    "full_name": "Example User",
    "disabled": false,
    "organisation": null,
    "id": "667c23e9bf24f7e4c474fd1c"
}
```


# HOWTO: Create organisation
> **Note:** [Admin authentication](howto) is required!

Send a `POST` HTTP request to `/admin/organisations` endpoint.

Example request body:
```json
{
  "name": "test organisation",
  "devices": [],
  "members": []
}
```

Response:
```json
{
    "name": "test organisation",
    "devices": [],
    "members": [],
    "id": "667c2b655a4c2323be4b21fd"
}
```

# HOWTO: Add user to organisation
Send a `POST` request to the `/admin/organisations/add_user` endpoint.

Example request body:
```json
{
  "user": "667c23e9bf24f7e4c474fd1c",
  "is_admin": false,
  "organisation": "667c2b655a4c2323be4b21fd"
}
```
