from datetime import datetime
from http import HTTPStatus

from fastapi import APIRouter
from fastapi import HTTPException
from pydantic import AnyUrl
from pydantic import BaseModel
from starlette.requests import Request

from crawler.models import Task
from crawler.models.task import TaskStatus
from crawler.tasks import parse_links
from optifino.throttling import limiter

router = APIRouter(prefix="/tasks", tags=['Task'])


class TaskRequest(BaseModel):
    site_url: AnyUrl


class TaskResponse(BaseModel):
    id: int
    status: TaskStatus
    site_url: AnyUrl
    created_at: datetime

    @classmethod
    def from_model(cls, task):
        return cls(
            id=task.id,
            created_at=task.created_at,
            status=task.status,
            site_url=task.site_url,
        )


@router.post('/', status_code=HTTPStatus.CREATED)
@limiter.limit("15/minute")
async def add_task(request: Request, task_request: TaskRequest) -> TaskResponse:
    task = await Task.objects.acreate(site_url=task_request.site_url)
    parse_links.delay(task_id=task.id)
    return TaskResponse.from_model(task)


@router.get('/{task_id}', status_code=HTTPStatus.OK)
async def get_task(task_id: int) -> TaskResponse:
    task = await Task.objects.filter(id=task_id).afirst()
    if not task:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Task not found")

    return TaskResponse.from_model(task)
