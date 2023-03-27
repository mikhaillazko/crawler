import os

from kombu import Exchange
from kombu import Queue

from core import env_var_enabled

# Rabbit MQ settings
broker_url = os.environ['BROKER_URL']
broker_use_ssl = env_var_enabled('CELERY_BROKER_USE_SSL', default=True)
worker_prefetch_multiplier = 6

# celery queues setup
celery_exchange = Exchange('default')
task_queues = (
    Queue('normal', celery_exchange, routing_key='normal'),
)

task_default_exchange = 'default'
task_default_queue = 'normal'
task_default_routing_key = 'normal'

task_routes = {
    'crawler.*': {'queue': 'normal'},
}

task_soft_time_limit = int(os.environ.get('CELERY_TASK_SOFT_TIME_LIMIT'))
task_time_limit = int(os.environ.get('CELERY_TASK_TIME_LIMIT'))
task_always_eager = env_var_enabled('CELERY_TASK_ALWAYS_EAGER', default=False)
