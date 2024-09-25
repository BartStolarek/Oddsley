# Docker Compose Commands

## Build
- Build all services

        `docker-compose build`

- Build specific service(s)

        `docker-compose build frontend`
        
        `docker-compose build backend`

## Start
- Start all services (builds if necessary)

        `docker-compose up`

- Start all services in detached mode (runs in background)

        `docker-compose up -d`

- Start specific service(s)

        `docker-compose up backend`
        `docker-compose up frontend`

- Start services without building

        cker-compose up --no-build`

## Stop
- Stop all running services

        `docker-compose down`

- Stop specific service(s)

        `docker-compose stop backend`
        `docker-compose stop frontend`

- Remove all stopped service containers

        `docker-compose rm`

- Remove a specific stopped service container'

        `docker-compose rm backend`

## Logs
- View logs of all services

        `docker-compose logs`

- View logs of specific service(s)

        `docker-compose logs backend`
        `docker-compose logs -f frontend  # -f to follow log output`

## Other
- List containers

        `docker-compose ps`

- Execute a command in a running container

        `docker-compose exec backend python manage.py shell`
        `docker-compose exec frontend npm run test`

