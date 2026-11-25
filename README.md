# Module 12: FastAPI Application, Authentication, Database Integration, Testing and CI/CD

## Project Overview

Module 12 builds on the previous application work by implementing a FastAPI application with user authentication, JWT-based security, database integration, calculation functionality, automated testing, containerization, security scanning, and continuous deployment.

The application uses PostgreSQL for persistent data storage and Redis for JWT token blacklist functionality.

## Repository

- **GitHub:** https://github.com/quameboakye/module12_is601
- **Docker Hub:** https://hub.docker.com/r/slasha1982/module12_is601

## Technology Stack

- Python 3.11
- FastAPI
- SQLAlchemy 2
- Pydantic
- PostgreSQL 16
- Redis 7
- JWT authentication
- Passlib and bcrypt
- Pytest and pytest-cov
- Playwright
- Docker and Docker Buildx
- GitHub Actions
- Trivy vulnerability scanning
- Docker Hub

## Application Features

The application includes:

- FastAPI application and REST API endpoints.
- SQLAlchemy user and calculation models.
- Pydantic schemas for request validation and response serialization.
- User authentication and JWT token functionality.
- JWT refresh-token support.
- Redis-backed token blacklist functionality.
- PostgreSQL database integration.
- Calculation functionality.
- Unit, integration, and end-to-end tests.
- Docker containerization.
- Automated CI/CD through GitHub Actions.
- Container vulnerability scanning using Trivy.
- Automated Docker Hub image publishing.

## Project Structure

```text
module12_is601/
├── .github/
│   └── workflows/
│       └── test.yml
├── app/
│   ├── auth/
│   │   ├── dependencies.py
│   │   ├── jwt.py
│   │   └── redis.py
│   ├── core/
│   │   └── config.py
│   ├── models/
│   │   ├── calculation.py
│   │   └── user.py
│   ├── operations/
│   ├── schemas/
│   │   ├── auth.py
│   │   ├── base.py
│   │   ├── calculation.py
│   │   ├── token.py
│   │   └── user.py
│   ├── config.py
│   ├── database.py
│   ├── database_init.py
│   └── main.py
├── tests/
│   ├── unit/
│   ├── integration/
│   └── e2e/
├── Dockerfile
├── .dockerignore
├── requirements.txt
├── pytest.ini
├── README.md
└── REFLECTION.md
```

## Prerequisites

Install:

- Python 3.11 or later
- Git
- Docker Engine
- Docker Compose (if using a separately configured Compose environment)

Verify the installations:

```bash
python3 --version
git --version
docker --version
docker compose version
```

## Clone the Repository

```bash
git clone https://github.com/quameboakye/module12_is601.git
cd module12_is601
```

## Python Environment Setup

Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Environment Configuration

The application uses environment-based configuration.

The main environment variables include:

| Variable | Purpose |
|---|---|
| DATABASE_URL | PostgreSQL connection URL |
| REDIS_URL | Redis connection URL |
| JWT_SECRET_KEY | JWT signing secret |
| JWT_REFRESH_SECRET_KEY | JWT refresh-token signing secret |

Configure these values in your local environment before starting the application.

Do not commit `.env` files, database passwords, JWT secrets, or Docker Hub access tokens.

## Running the Tests

Run the complete test suite:

```bash
pytest -vv --run-slow
```

Run the tests with coverage:

```bash
pytest -vv --run-slow \
  --cov=app \
  --cov-report=term-missing
```

The latest verified local test run produced:

- **103 tests passed**
- **68.21% code coverage**
- No failing tests.

The GitHub Actions test job currently enforces a minimum coverage threshold of 68%.

The test suite includes unit, integration, and end-to-end tests.

## Docker Configuration

The root Dockerfile builds the Module 12 FastAPI application using Python 3.11 slim.

The image includes:

- Application dependency installation.
- Application source code.
- A non-root application user.
- A container health check.
- Uvicorn as the application server.

The application starts using:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 1
```

Build the local Docker image:

```bash
docker build -t module12_is601:test .
```

Run the locally built image after configuring the required environment variables and ensuring PostgreSQL and Redis are reachable from the container.

Example:

```bash
docker run -d \
  --name module12-app-example \
  --add-host=host.docker.internal:host-gateway \
  -p 8003:8000 \
  -e DATABASE_URL="postgresql+psycopg://DB_USER:DB_PASSWORD@host.docker.internal:5434/DB_NAME" \
  -e REDIS_URL="redis://host.docker.internal:6379/0" \
  -e JWT_SECRET_KEY="replace-with-a-secure-secret" \
  -e JWT_REFRESH_SECRET_KEY="replace-with-a-secure-refresh-secret" \
  module12_is601:test
```

Check the running container:

```bash
docker ps
docker logs --tail 50 module12-app
```

## Application Verification

The following endpoints were verified against the locally running Module 12 container:

| Endpoint | Result |
|---|---|
| `/health` | HTTP 200 |
| `/docs` | HTTP 200 |
| `/openapi.json` | HTTP 200 |

The health endpoint returned:

```json
{"status":"ok"}
```

### Manual API checks in Swagger

Open `http://localhost:8002/docs` in your browser.

1. Register a user using `POST /users/register`. Supply all required fields, including `confirm_password`.
2. Log in using `POST /users/login` with the registered username and password.
3. Select **Authorize** and authenticate using the `/auth/token` OAuth2 form.
4. Test the protected calculation endpoints: create, list, retrieve, update, and delete calculations.
5. Verify that invalid calculation input, such as division by zero, is rejected.

PostgreSQL connectivity was verified from inside the application container using:

```sql
SELECT 1;
```

The query returned `1`.

Redis connectivity was also verified from inside the application container using `PING`, which returned `True`.

The local application container reported a healthy status.

## GitHub Actions CI/CD

The workflow is located at:

`.github/workflows/test.yml`

It runs automatically when changes are pushed to the `main` branch or when a pull request targets `main`.

The workflow contains three jobs:

### 1. Test

- Sets up Python 3.11.
- Starts PostgreSQL 16 and Redis 7 services.
- Installs project dependencies.
- Installs Playwright and Chromium.
- Runs the test suite.
- Generates a coverage report.
- Enforces the configured coverage threshold.

### 2. Security

- Builds the Module 12 Docker image.
- Runs Trivy vulnerability scanning.
- Checks for CRITICAL and HIGH vulnerabilities.
- Fails the job when qualifying vulnerabilities are detected.

### 3. Deploy

- Runs after the security job succeeds.
- Executes for pushes to the `main` branch.
- Authenticates with Docker Hub using GitHub Actions secrets.
- Builds and publishes the Module 12 Docker image.

The workflow publishes two tags:

```text
DOCKERHUB_USERNAME/module12_is601:latest
DOCKERHUB_USERNAME/module12_is601:<commit-sha>
```

Configure these GitHub Actions secrets:

- `DOCKERHUB_USERNAME`
- `DOCKERHUB_TOKEN`

Never put Docker Hub credentials directly in the workflow or application source code.

## Deployment Verification

The latest verified GitHub Actions run completed successfully:

- Test job: passed.
- Security job: passed.
- Deploy job: passed.

The local Docker container was also verified independently.

The following checks succeeded:

- Container health status: healthy.
- FastAPI health endpoint: HTTP 200.
- FastAPI documentation endpoint: HTTP 200.
- OpenAPI JSON endpoint: HTTP 200.
- PostgreSQL connection: successful.
- Redis connection: successful.

The local container test used the locally built image. The published Docker Hub image was subsequently pulled and run independently using a separate container.

The independently running Docker Hub container passed the following checks:

- Container status: running and healthy.
- `/health`: HTTP 200.
- `/docs`: HTTP 200.
- `/openapi.json`: HTTP 200.
- PostgreSQL connectivity: `SELECT 1` returned `1`.
- Redis connectivity: `PING` returned `True`.

The published image was tested on host port 8003, separately from the original local application container on port 8002.

## Security Considerations

Before production use:

- Use strong, independently generated JWT secrets.
- Use secure database credentials.
- Store sensitive configuration in a secrets manager or protected environment variables.
- Use HTTPS for external application traffic.
- Restrict database and Redis network access.
- Continue monitoring dependencies and container vulnerabilities.
- Review authentication, authorization, and token expiration settings.

Development credentials must not be used in production.

## Submission Checklist

- [x] FastAPI application implemented.
- [x] SQLAlchemy models and database integration.
- [x] Pydantic schemas and validation.
- [x] JWT authentication functionality.
- [x] Redis-backed token blacklist functionality.
- [x] Unit, integration, and end-to-end tests executed.
- [x] Local Docker image built successfully.
- [x] Local application container reported healthy.
- [x] Health endpoint returned HTTP 200.
- [x] API documentation returned HTTP 200.
- [x] OpenAPI JSON endpoint returned HTTP 200.
- [x] PostgreSQL connectivity verified.
- [x] Redis connectivity verified.
- [x] GitHub Actions test job passed.
- [x] GitHub Actions security job passed.
- [x] GitHub Actions deployment job passed.
- [x] Verify the published Docker Hub image by pulling and running it independently.
- [ ] Capture screenshots of successful GitHub Actions and Docker Hub publication.
- [ ] Confirm all documentation matches the final assignment rubric.

## Author

GitHub repository owner: `quameboakye`
