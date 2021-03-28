# Setup

---
**IMPORTANT NOTE**

Do not forget to copy environment variables using `cp .env.example .env`
for any type of setup.
___

## Local Development

For developing and testing locally just use docker (you can also just
run `main.py` from PyCharm).

Backend is using FastAPI framework that autogenerates API documentation with
Swagger. It can be accessed by `/docs` handle (e.g. `localhost:8000/docs`).

If you don't have Cloudflare TOKEN and ACCOUNT_ID you should set environment
variable CLOUDFLARE_DEBUG = 1. To save mock video with exists 
cloudflare_video_id:
```shell
echo 'cloudflare_video_id > filename
```

and use `/video/upload` with file=filename

## Docker

Being in the root repository directory just run:

```shell
docker-compose up --build
```

The service will be run on `0.0.0.0:8000` (i.e. `localhost:8000`). One should
not reload docker each time some changes were made as it is done automatically
with uvicorn. and docker-compose volume.

## Cloud

### Environment Variables
1. Copy environment variables to `.env` file: `cp .env.example .env`

2. Fill it with your credentials.

 - `OATH_TOKEN` is your OAth-token in Yandex Cloud.
   More [here](https://cloud.yandex.ru/docs/iam/concepts/authorization/oauth-token).
 - `CLOUD_ID` is the identificator of you yandex cloud account. Can be found
   [here](https://console.cloud.yandex.ru/cloud).
 - `CLOUD_FOLDER_ID` is the id of folder in your yandex cloud account.
   More [here](https://cloud.yandex.ru/docs/resource-manager/operations/folder/get-id).
 - `CLOUD_ZONE` is the zone, where you want your application to be run, for
   example "ru-central1-a".
 - `CLOUDFLARE_TOKEN` is the Cloudflare API token.
   More [here](https://support.cloudflare.com/hc/en-us/articles/200167836-Managing-API-Tokens-and-Keys).
 - `CLOUDFLARE_ACCOUNT_ID` is your account ID. Can be retrieved from 
   the dashboard or by API.
   
### Container Registry
3. Create Yandex Container Registry. More 
[here](https://cloud.yandex.com/en/docs/container-registry/quickstart/).
                               
4. Build, tag and push nginx and postgres images.

#### nginx
```shell
cd nginx
docker build . -t <your-nginx-tag>
docker tag <your-nginx-tag> cr.yandex/<your-registry-id>/<your-nginx-tag>
docker push cr.yandex/<your-registry-id>/<your-nginx-tag>
```

#### postgres
```shell
cd postgres
docker build . -t <your-postgres-tag>
docker tag <your-postgres-tag> cr.yandex/<your-registry-id>/<your-postgres-tag>
docker push cr.yandex/<your-registry-id>/<your-postgres-tag>
```

### Terraform
5. Go to terraform directory, copy env file and fill it with your credentials.
```shell
cd terraform
cp terraform.tfvars.example terraform.tfvars
```

6. Init terraform and apply provisioning
```shell
terraform init
terraform apply
```

### Service deployment
7. Go to [Yandex Console](https://console.cloud.yandex.ru/) and wait until 
   all VMs are provisioned and started.
   
8. Update IPs in `deploy.py` file, activate pipenv environment and run deploy
   file and wait until complete.
   
```shell
pipenv install
pipenv shell
python deploy.py
```

9. Take nginx public IP and go and check that everything is deployed!
