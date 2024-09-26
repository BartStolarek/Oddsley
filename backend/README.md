# Django Management Commands

Django management commands are a powerful feature that allows you to interact with your Django project via the command line. These commands can be used for a variety of tasks, including project management, database management, testing, and more.

## 1. Project Management

- `python manage.py startapp <app_name>`: Creates a new Django app
- `python manage.py check`: Checks your project for common problems
- `python manage.py shell`: Starts an interactive Python shell with Django environment loaded
- `python manage.py createsuperuser`: Creates a superuser account for the Django admin

## 2. Database Management

- `python manage.py migrate`: Applies database migrations
- `python manage.py makemigrations`: Creates new migrations based on changes detected in your models
- `python manage.py showmigrations`: Shows all migrations and their status
- `python manage.py sqlmigrate`: Displays the SQL statements for a migration
- `python manage.py dbshell`: Starts the command-line client for your database
- `python manage.py dumpdata`: Outputs the contents of the database as a fixture
- `python manage.py loaddata`: Loads data from a fixture into the database

## 3. Testing and Coverage

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

## 4. Development Server

- `python manage.py hello_world`: Prints "Hello, World!" to the console
- `python manage.py runserver`: Starts the Django development server


## 5. Tasks

The following commands are available for immediate task execution:

- `python manage.py task_run <task_name> [--args arg1 arg2 ...]`: Runs a specified task immediately

Example:
```
python manage.py task_run hello_world_task
```

This command will execute the specified task immediately and display the result in the console. It's useful for testing tasks or running one-off operations.

## 6. Jobs

Django-Q is used for job queuing in this project. The following commands are available to manage jobs:

- `python manage.py job_task <task_name> [--args arg1 arg2 ...]`: Queues a job with a specified task

    Example:
    ```
    python manage.py job_task hello_world_task --args param1 param2
    ```

- `python manage.py job_list`: Displays a list of all currently queued jobs with their unique IDs

- `python manage.py job_cancel <job_id>`: Cancels a specific queued job using its unique ID

- `python manage.py job_cancel_all`: Cancels all currently queued jobs

Jobs are tasks that are queued for later execution by Django-Q workers. This allows for asynchronous processing and better management of long-running or resource-intensive tasks.


## 7. Scheduling

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


## 8. Static Files

- `python manage.py collectstatic`: Collects static files into STATIC_ROOT


## 9. Code Quality and Formatting

- `python manage.py format`: Runs autoflake, isort, and yapf formatters over the project

## Additional Useful Commands

- `python manage.py clearsessions`: Clears expired sessions from the database
- `python manage.py diffsettings`: Displays differences between the current settings and Django's default settings
- `python manage.py sendtestemail`: Sends a test email to confirm your email settings are correct

Remember to run these commands from your project's root directory. Some commands may require additional packages to be installed, especially for advanced testing and coverage features.

