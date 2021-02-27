# Setup
___

## Local Development
For a local development service stores uploaded videos locally at `videos/` directory.
It is automatically created on the app startup.

For developing and testing locally just use docker (you can also just run `main.py`
from PyCharm).

Backend is using FastAPI framework that autogenerates API documentation with Swagger.
It can be accessed by `/docs` handle (e.g. `localhost:8000/docs`).

### Docker
Being in the root repository directory just run:
```shell
docker-compose up --build
```
The service will be run on `0.0.0.0:8000` (i.e. `localhost:8000`). One should not 
reload docker each time some changes were made as it is done automatically with uvicorn.
and docker-compose volume.

### Cloud
To deploy application on cloud run `deploy.sh <token>` in root directory, where <token> is your OAth-token in Yandex Cloud (https://cloud.yandex.ru/docs/iam/concepts/authorization/oauth-token).
