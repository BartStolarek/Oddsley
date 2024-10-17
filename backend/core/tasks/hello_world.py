from loguru import logger

def hello_world_task(*args, _task_name=None, _job_id=None, **kwargs):
    print("Hello, World!")
    logger.info(f"Task: {_task_name}, Job ID: {_job_id}")
    