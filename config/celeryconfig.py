broker_url = 'redis://localhost:6379/'
result_backend = 'django-db'

task_serializer = 'json'
result_serializer = 'json'
accept_content = ['json']
timezone = 'Asia/Bishkek'
enable_utc = False
broker_connection_retry_on_startup = True

task_routes = {
    'tasks.add': 'low-priority',
}

task_annotations = {
    'tasks.add': {'rate_limit': '10/m'}
}
