# Backend for IdealAQ sensor data monitoring app
This app was completed as part of [Full-stack open](fullstackopen.com/en/) course. Additionally, the created solution aims to serve as a useful tool for [IdealAQ](https://idealaq.com/) project with a potential to be the base or a case study for future production version of the web app.

## Instructions
> The name of the container (app-backend) might not me the same. Verify using `docker container ls`.

To run the backend locally, run 
```bash
docker-compose -f ./docker-compose.dev.yml up
```
To open Swagger UI (for API documentation), visit http://127.0.0.1:8080/docs

To run tests, run while running backend in container: 
```bash
docker exec -it app-backend /bin/bash pytest
```

To check linting, run while running backend in container:
```bash
docker exec -it app-backend flake8 .
```

## ENV Variables
> **WARNING:** The database used to run tests must be different from database used to run the app. Otherwise, all application data might ger corrupted or lost. 

| variable                      | description                                  | note                     |
|-------------------------------|----------------------------------------------|--------------------------|
| **database**                  |                                              |                          |
| `MONGODB_CONNECTION_URI`      | connection uri for the database              |                          |
| `MONGODB_CONNECTION_URI_TEST` | connection uri for the database to run tests | \*used only to run tests |
| `DB_NAME`                     | name of the database                         |                          |
| `DB_NAME_TEST`                | name of the database used to run tests       | \*used only to run tests |
| **encryption**                |                                              |                          |
| `SECRET_KEY`                  |                                              |                          |
| `ALGORITHM`                   |                                              |                          |
| `ACCESS_TOKEN_EXPIRE_MINUTES` |                                              |                          |
| **AWS SDK**                   |                                              |                          |
| `AWS_ACCESS_KEY_ID`           |                                              |                          |
| `AWS_SECRET_ACCESS_KEY`       |                                              |                          |
| `AWS_REGION_NAME`             |                                              |                          |
|                               |                                              |                          |


