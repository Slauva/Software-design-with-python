# Плагин для вывода сообщений при добавлении/завершении задач
class NotificationPlugin:
    """Плагин для отправки уведомлений о задачах."""
    
    def update(self, action, task):
        if action == 'add':
            print(f'Добавлена новая задача: {task.title}')
        elif action == 'complete':
            print(f'Задача завершена: {task.title}')