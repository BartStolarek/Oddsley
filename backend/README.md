# Django Backend Server

This backend directory contains the Django project for the backend server of the application. The backend server provides the API endpoints and business logic for the application.

## Installation

To install the backend server, follow these steps:

1. Create a `.env` file in the `backend` directory (`root/backend/.env`) and add the following environment variables:

```
DJANGO_ENVIRONMENT=development  # development, production
DJANGO_LOGGING=DEBUG   # DEBUG, INFO, WARNING, ERROR, CRITICAL
DJANGO_SECRET_KEY=your__secret_key
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1

CORS_ALLOWED_ORIGINS=http://localhost:3000

# Production database settings (not used in development)
DB_NAME=your_production_db_name
DB_USER=your_production_db_user
DB_PASSWORD=your_production_db_password
DB_HOST=your_production_db_host
DB_PORT=5432

# Django Q Cluster settings for development
Q_CLUSTER_NAME=oddsley_backend
Q_CLUSTER_WORKERS=4
Q_CLUSTER_RECYCLE=500
Q_CLUSTER_TIMEOUT=60
Q_CLUSTER_COMPRESS=True
Q_CLUSTER_SAVE_LIMIT=250
Q_CLUSTER_QUEUE_LIMIT=500
Q_CLUSTER_CPU_AFFINITY=1
Q_CLUSTER_LABEL=Django Q2
Q_CLUSTER_REDIS_HOST=127.0.0.1
Q_CLUSTER_REDIS_PORT=6379
Q_CLUSTER_REDIS_DB=0
```

2. Follow docker instructions from the root README to start the docker backend server.

3. Create a super user for the backend Django admin by running the following command:

```
docker-compose exec backend python manage.py createsuperuser
```

## Admin Panel

To access the admin panel, navigate to `http://localhost:5000/admin` in your browser and log in with the superuser credentials you created.

## Environments

The backend server supports multiple environments, each with its own settings and configurations. The following environments are available:
- `Development`: The default development environment that uses SQLite as the database locally
- `Production`: The production environment that uses PostgreSQL as the database (needs to be configured in the `.env` file)

To set your environment update the `DJANGO_ENVIRONMENT` variable in the `.env` file.

## Databases

The backend server supports multiple databases, including SQLite and PostgreSQL. By default, the development environment uses SQLite, while the production environment uses PostgreSQL.

Currently as of 29th September 2024, the relationship diagram for the database is as follows:

### In-built in to Django Users, Permissions, Groups, Sessions, etc

![alt text](static/Django_model_UML_diagram.png)

## Django Management Commands

Django management commands are a powerful feature that allows you to interact with your Django project via the command line. These commands can be used for a variety of tasks, including project management, database management, testing, and more.

You can either run the commands directly from the terminal in the `root/backend` directory or you can run them from the Django shell. For shell instructions, see the `root/README.md` file.

The most common commands to use are as follows:
- `python manage.py makemigrations` (make database adjustments when changes were made to models)
- `python manage.py migrate` (apply database changes)
- `python manage.py runserver` (start the development server)
- `python manage.py test` (run unit tests)
- `python manage.py format` (format the code using autoflake, isort, and yapf)
- `python manage.py qcluster` (start the Django-Q cluster which is a redis queue to asynchronously run tasks by adding them to the queue with job or schedule commands)
- The Task, Job and Schedule commands are also useful for managing background tasks and scheduling.

The following is a list of useful Django management commands that you can use to manage Django project:

### 1. Project Management

- `python manage.py startapp <app_name>`: Creates a new Django app
- `python manage.py check`: Checks your project for common problems
- `python manage.py shell`: Starts an interactive Python shell with Django environment loaded
- `python manage.py createsuperuser`: Creates a superuser account for the Django admin

### 2. Database Management

- `python manage.py makemigrations`: Creates new migrations based on changes detected in your models
- `python manage.py migrate`: Applies database migrations
- `python manage.py showmigrations`: Shows all migrations and their status
- `python manage.py sqlmigrate`: Displays the SQL statements for a migration
- `python manage.py dbshell`: Starts the command-line client for your database
- `python manage.py dumpdata`: Outputs the contents of the database as a fixture
- `python manage.py loaddata`: Loads data from a fixture into the database

### 3. Testing and Coverage

- `python manage.py test`: Runs all tests in your Django project
- `python manage.py test <app_name>`: Runs tests for a specific app
- `python manage.py test <app_name>.tests.<test_file>`: Runs tests in a specific test file
- `python manage.py test <app_name>.tests.<test_file>.<TestClass>`: Runs tests in a specific test class
- `python manage.py test <app_name>.tests.<test_file>.<TestClass>.<test_method>`: Runs a specific test method
- `python manage.py test --verbosity=2`: Runs tests with increased verbosity for more detailed output
- `python manage.py test --keepdb`: Preserves the test database between test runs for faster testing
- `coverage run --source='.' manage.py test`: Runs tests and collects coverage data
- `coverage report`: Displays a coverage report in the terminal
- `coverage html`: Generates an HTML coverage report

### 4. Development Server

- `python manage.py hello_world`: Prints "Hello, World!" to the console
- `python manage.py runserver`: Starts the Django development server

### 5. Tasks

The following commands are available for immediate task execution:

- `python manage.py task_run <task_name> [--args arg1 arg2 ...]`: Runs a specified task immediately

Example:
```
python manage.py task_run hello_world_task
```

This command will execute the specified task immediately and display the result in the console. It's useful for testing tasks or running one-off operations.

### 6. Jobs

Django-Q is used for job queuing in this project, where a task is taken applied to a job and queued. The following commands are available to manage jobs:

- `python manage.py job_task <task_name> [--args arg1 arg2 ...]`: Queues a job with a specified task

    Example:
    ```
    python manage.py job_task hello_world_task --args param1 param2
    ```

- `python manage.py job_list`: Displays a list of all currently queued jobs with their unique IDs

- `python manage.py job_cancel <job_id>`: Cancels a specific queued job using its unique ID

- `python manage.py job_cancel_all`: Cancels all currently queued jobs

Jobs are tasks that are queued for later execution by Django-Q workers. This allows for asynchronous processing and better management of long-running or resource-intensive tasks.


### 7. Scheduling

Django-Q is used for task scheduling in this project. The following commands are available to manage scheduled tasks:

- `python manage.py schedule_task <task_name> [options]`: Schedules a task with various timing options

    Options:
    - `--schedule_type`: Type of schedule (MINUTES, HOURLY, DAILY, WEEKLY, MONTHLY, QUARTERLY, YEARLY)
    - `--interval`: Interval for MINUTES schedule type
    - `--hour`: Hour for DAILY, WEEKLY, MONTHLY schedules (0-23)
    - `--minute`: Minute for schedules with specific times (0-59)
    - `--day_of_week`: Day of week for WEEKLY schedule (0-6, where 0 is Monday)
    - `--day_of_month`: Day of month for MONTHLY schedule (1-31)
    - `--params`: Parameters to pass to the task

    Example:
    ```
    python manage.py schedule_schedule_task hello_world_task --schedule_type MINUTES --interval 5
    ```

- `python manage.py schedule_list`: Displays a list of all currently scheduled tasks with their unique IDs

- `python manage.py schedule_cancel <task_id>`: Cancels a specific scheduled task using its unique ID

- `python manage.py schedule_cancel_all`: Cancels all currently scheduled tasks


### 8. Static Files

- `python manage.py collectstatic`: Collects static files into STATIC_ROOT


### 9. Code Quality and Formatting

- `python manage.py format`: Runs autoflake, isort, and yapf formatters over the project

### Additional Useful Commands

- `python manage.py clearsessions`: Clears expired sessions from the database
- `python manage.py diffsettings`: Displays differences between the current settings and Django's default settings
- `python manage.py sendtestemail`: Sends a test email to confirm your email settings are correct

Remember to run these commands from your project's root directory. Some commands may require additional packages to be installed, especially for advanced testing and coverage features.

