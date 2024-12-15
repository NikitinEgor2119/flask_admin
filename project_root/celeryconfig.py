from datetime import timedelta

# Адрес брокера сообщений (Redis)
broker_url = 'redis://localhost:6379/0'

# Хранилище результатов задач (опционально)
result_backend = 'redis://localhost:6379/0'

# Задачи, которые истекают через 1 час
task_serializer = 'json'
result_serializer = 'json'
accept_content = ['json']
timezone = 'UTC'
enable_utc = True

# Автоматический запуск задач по расписанию (например, каждые 10 минут)
beat_schedule = {
    'expire_transactions': {
        'task': 'tasks.expire_transactions',
        'schedule': timedelta(minutes=10),
    },
}