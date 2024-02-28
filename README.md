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

## Environment Variables
- `MONGODB_CONNECTION_URI`: Connection URL for mongo db
- `DB_NAME`: Name of database
- `DB_NAME_TEST`: Name of database used to run tests

