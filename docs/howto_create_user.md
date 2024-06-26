# HOWTO: Create user
> **Note:** [Admin authentication](howto_admin_authentication.md) is required!

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