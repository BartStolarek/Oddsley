# In backend/core/task_registry.py

from django.utils.module_loading import import_string


class TaskRegistry:
    _tasks = {}

    @classmethod
    def register(cls, name, func):
        cls._tasks[name] = func

    @classmethod
    def get_task(cls, name):
        if name in cls._tasks:
            return cls._tasks[name]
        try:
            return import_string(name)
        except ImportError:
            raise ValueError(
                f"Task {name} not found in registry or as importable string")
