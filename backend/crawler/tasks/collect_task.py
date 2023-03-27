import logging

from django.db import transaction

from crawler.models import Task
from crawler.models.task import TaskStatus
from crawler.services import collect_links
from optifino.celery import app

log = logging.getLogger(__name__)


@app.task
def parse_links(task_id: int):
    task = Task.objects.get(id=task_id)
    task.status = TaskStatus.STARTED
    task.save()
    try:
        with transaction.atomic():
            collect_links(task)
            task.status = TaskStatus.COMPLETED
            task.save()
    except Exception as e:
        log.exception(f'Failed to parse site {task.site_url} for task {task_id}')
        task.status = TaskStatus.FAILED
        task.save()
