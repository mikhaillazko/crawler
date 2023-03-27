from datetime import datetime
from typing import Optional

from django.db import models

from .task import Task


class LinkQuerySet(models.query.QuerySet):
    def filter_by_task_id(self, task_id):
        return self.filter(task_id=task_id)

    async def paginate(self, offset, limit):
        paginated_results = self[offset: offset + limit]
        async for obj in paginated_results:
            yield obj


class Link(models.Model):
    objects = LinkQuerySet.as_manager()

    id: int = models.AutoField(primary_key=True)
    created_at: datetime = models.DateTimeField(auto_now_add=True)
    origin: str = models.CharField(max_length=500)
    url: str = models.URLField(max_length=500)
    task: Optional[Task] = models.ForeignKey(Task, on_delete=models.SET_NULL, null=True)
    parent: Optional['Link'] = models.ForeignKey('self', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'Link(id={self.id}, origin="{self.origin}", url="{self.url}")'
