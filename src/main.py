import os
import importlib.util
import functools

class Task:
    """Класс для представления задачи."""
    
    def __init__(self, title, description):
        self.title = title
        self.description = description
        self.completed = False
    
    def complete(self):
        """Отметить задачу как завершенную."""
        self.completed = True

    def __str__(self):
        return f'Task: {self.title}, Description: {self.description}, Completed: {self.completed}'


def log_task_operation(operation):
    """Декоратор для логирования операций с задачами."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            result = func(self, *args, **kwargs)
            print(f"{operation.capitalize()} Task: {args[0] if args else 'N/A'}")
            return result
        return wrapper
    return decorator

class TaskManager:
    """Класс для управления задачами."""
    
    def __init__(self):
        self.tasks = []
        self.plugins = []

    @log_task_operation('added')
    def add_task(self, title, description):
        """Добавить задачу."""
        task = Task(title, description)
        self.tasks.append(task)
        self.notify_plugins('add', task)

    @log_task_operation('completed')
    def complete_task(self, title):
        """Завершить задачу по заголовку."""
        for task in self.tasks:
            if task.title == title:
                task.complete()
                self.notify_plugins('complete', task)
                break

    def list_tasks(self):
        """Вывести список задач."""
        return [str(task) for task in sorted(self.tasks, key=lambda x: x.completed)]

    def register_plugin(self, plugin):
        """Добавить плагин."""
        self.plugins.append(plugin)

    def notify_plugins(self, action, task):
        """Уведомление плагинов об изменениях."""
        for plugin in self.plugins:
            plugin.update(action, task)

def load_plugins(manager: TaskManager, plagin_folder: str):
    """Загрузить плагины из текущего каталога."""
    
    for filename in os.listdir(f"./{plagin_folder}"):
        if filename.endswith('.py') and filename != '__init__.py':
            plugin_path = os.path.join(os.path.dirname(__file__), '..', plagin_folder, filename)
            spec = importlib.util.spec_from_file_location(filename[:-3], plugin_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            for item in dir(module):
                item_class = getattr(module, item)
                if isinstance(item_class, type):
                    manager.register_plugin(item_class())
            
if __name__ == "__main__":
    task_manager = TaskManager()
    
    # Регистрация плагина
    load_plugins(task_manager, "plugins")

    # Примеры задач
    task_manager.add_task('Изучить Python', 'Пройти курс на Codecademy')
    task_manager.add_task('Написать отчет', 'Подготовить отчет по проекту')
    
    # Завершение задачи
    task_manager.complete_task('Изучить Python')
    
    # Вывод всех задач
    for task in task_manager.list_tasks():
        print(task)
