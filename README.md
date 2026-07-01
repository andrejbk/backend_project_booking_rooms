## BookingPro
RESTful API for an online hotel booking system

## Live API

- 🌐 Landing Page: https://booking-project.de
- 📖 Swagger UI: https://booking-project.de/docs
- 📚 ReDoc: https://booking-project.de/redoc

### Overview
BookingPro is my personal backend portfolio project created to demonstrate practical backend development skills using Python.

I developed the application entirely from scratch, implementing a RESTful API for an online hotel booking platform and deploying it to a real server with a public domain.

The project follows modern development practices, including asynchronous programming, automated testing, static analysis, Docker-based deployment, and GitLab CI/CD automation.

### Technology Stack

   - Python 3.12
   - FastAPI + Pydantic
   - PostgreSQL 18
   - SQLAlchemy + asyncpg
   - Redis + Celery
   - Pytest + Ruff
   - Docker + Docker Compose
   - Nginx
   - Gitlab CI/CD

### Key Features

  - JWT-based authentication and authorization
  - Asynchronous processing for booking operations, database interactions, and background tasks
  - Interactive OpenAPI (Swagger) documentation
  - Comprehensive unit and integration tests
  - Automated code quality checks with Ruff (linting and formatting)
  - Docker-based deployment
  - Automated GitLab CI/CD pipeline

### Installation
   - Clone the repository.
   - Create a .env file from .env-test and configure it with the required values. 
   1. Local setup
   - Create a Python virtual environment and activate it.

         python -m venv venv
         source venv/bin/activate  (macOS / Linux)
         venv\Scripts\activate.bat (Windows (CMD))
         venv\Scripts\Activate.ps1 (Windows (PowerShell))

   - Install the dependencies from requirements.txt.

         pip install -r requirements.txt
   2. Server setup using Docker, Docker Compose, and GitLab CI/CD
   - Create a Docker network.
         
         docker network create my-network

   - Start the PostgreSQL database.

         docker run --name booking_db -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=your_password -e POSTGRES_DB=booking --network=my-network -v pg-booking-data:/var/lib/postgresql/18/docker -d postgres:18

   - Start the Redis container.

         docker run --name booking_cache --network=my-network -d redis:8.8

   - Start the application, Celery worker, and Celery Beat services.

         docker compose -f docker-compose.yml up -d

   - Create an nginx.conf configuration file and start the Nginx container.

         nginx.conf (example):
         # start of file
         events {}

         http {
             server {
                 location / {
                     proxy_pass http://booking_back:8000/;
                 }
             }
         }
         # end of file

         docker run --name booking_nginx -v ./nginx.conf:/etc/nginx/nginx.conf:ro -v /etc/letsencrypt:/etc/letsencrypt:ro -v /var/lib/letsencrypt:/var/lib/letsencrypt:ro --network=my-network --rm -p 80:80 -d nginx

   - Set up the GitLab Runner.
         
         docker run -d --name gitlab-runner --restart always -v /srv/gitlab-runner/config:/etc/gitlab-runner -v /var/run/docker.sock:/var/run/docker.sock gitlab/gitlab-runner:alpine

   - Register the GitLab Runner. When prompted, provide the GitLab Runner authentication token and set the default Docker image to `docker:dind`.

         docker run --rm -it -v /srv/gitlab-runner/config:/etc/gitlab-runner gitlab/gitlab-runner:alpine register

   - Create two GitLab CI/CD variables, `ENV` and `TEST_ENV`, containing the contents of the `.env` and `.env-test` files.

### Deployment
The project uses a GitLab CI/CD pipeline to automate the integration and deployment process. After changes are pushed to the GitLab repository, the pipeline is triggered automatically and executed by a pre-configured GitLab Runner.

> **Important!**
> Before pushing your changes, ensure that all tests pass and the code successfully passes linting and formatting checks. See the **Testing & Code Quality** section for details.
    
### Testing & Code Quality
Run the following commands in order and make sure each one completes successfully without errors.

         pytest
         ruff check
         ruff format

### My Experience
Working on BookingPro significantly improved my understanding of backend development.

Since I developed the project independently, I was responsible for every aspect of the software development process—from architecture and implementation to testing, deployment, and maintenance.

This experience gave me practical insight into how modern backend applications are designed, tested, deployed, and maintained in real-world development environments.