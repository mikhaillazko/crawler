from datetime import datetime

from django.db import models


class TaskStatus(models.TextChoices):
    PENDING = 'pending'
    STARTED = 'started'
    COMPLETED = 'completed'
    FAILED = 'failed'


class Task(models.Model):
    id: int = models.AutoField(primary_key=True)
    created_at: datetime = models.DateTimeField(auto_now_add=True)
    updated_at: datetime = models.DateTimeField(auto_now=True)
    site_url: str = models.URLField(max_length=200, null=False, blank=False)
    status: TaskStatus = models.CharField(max_length=15, choices=TaskStatus.choices, default=TaskStatus.PENDING)

    def __str__(self):
        return f'Task(id={self.id}, url="{self.site_url}", status="{self.status}")'
