from django.core.management import call_command
from django.db import connections
from django.db.migrations.executor import MigrationExecutor
from loguru import logger

class BaseTask:
    @classmethod
    def run(cls, *args, **kwargs):
        cls.apply_migrations()
        return cls.execute(*args, **kwargs)

    @staticmethod
    def apply_migrations():
        connection = connections['default']
        executor = MigrationExecutor(connection)
        if executor.migration_plan(executor.loader.graph.leaf_nodes()):
            logger.info('Applying database migrations...')
            call_command('migrate', no_input=True)
        else:
            logger.info('Database up to date, no migrations needed')

    @classmethod
    def execute(cls, *args, **kwargs):
        raise NotImplementedError("Subclasses must implement execute method")