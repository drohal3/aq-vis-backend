# Admin authentication
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