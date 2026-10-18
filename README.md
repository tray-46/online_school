# Sky.online-school platform

<details>
    <summary>Table of Content</summary>
    <ol>
        <li>
            <a href="#about-the-project">About the project</a>
        </li>
        <li>
          <a href="#getting-started">Getting started</a>
        </li>     
        <li>
          <a href="#ci-cd">CI/CD</a>
        </li> 
    </ol>
</details>

## About the project
A training project - online school platform with DRF

### Build with
* [![Python](https://img.shields.io/badge/Python%20IDLE-3776AB?logo=python&logoColor=fff)](https://python.org/)
* [![PyCharm](https://img.shields.io/badge/PyCharm-000?logo=pycharm&logoColor=fff)](https://www.jetbrains.com/pycharm/)

## Getting started
To clone the repository use the following links:

* with HTTPS:
```
https://github.com/tray-46/online_school.git
```

* with SSH:  
```
git@github.com:tray-46/online_school.git
```

Install dependencies.
From `.env_example` create `.env` file and fill it with your environment settings.

Project uses [stripe.com](https://stripe.com/) for payment processing, so you must provide api keys.  
Project use Celery, so you will need a message broker.

Create database with name specified in settings.  
The project uses a modified AbstractUser model. If you've already applied migrations to the database, 
you may need to roll back the migrations for the "auth" application.

Optionally you can fill database with test data by executing commandL
```
python manage.py fill_db
```
**Warning:**  
command will clear existing payments, lessons and courses data and reset respective id sequences
 
### To run the application:  
#### Locally:
In console open project directory and execute following command:
```
python manage.py runserver
```
Start Celery worker process:
```
celery -A config worker --loglevel=INFO --pool=gevent
```
Start Celery beat process:
```
celery -A config beat --loglevel=INFO
```
#### Containerized:
You can run application in container by executing following command in project root directory
```
# --build - rebuild all images berore starting 
# -d - start app in detached mode
docker compose up --build -d
```
To show containers and they current status
```
docker compose ps 
```
For checking metrics and logs
```
# -f - stream logs in real time
docker compose logs -f 
```
For stoping application
```
docker compose stop
```

### CI/CD
Project support CI/CD implemented via GitHub actions.  
On push and pull request to main branch it will run:
 - testing
 - lint
 - docker image build and upload to Docker Hub
 - pulling new image on server and restarting containers 

Initial set up for workflow:
+ Server set up:
    - Server supporting connections via ssh
    - Install Docker and Docker Compose
    - Create directory for the application and copy your .env production file, [nginx.conf](docker/nginx/nginx.conf) file and [docker-compose.prod.yaml](docker-compose.prod.yaml)
    - Login into Docker Hub
+ GitHub repository set up:
    Add following repository secrets:
    - SERVER_IP - your server public IP or domain name
    - SSH_USER - user for ssh connection to server
    - SSH_PRIVATE_KEY - shh key for connection
    - DEPLOY_DIR - working directory of application
    - DOCKER_HUB_USER
    - DOCKER_HUB_ACCESS_TOKEN - token for Docker Hub connection
