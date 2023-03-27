from datetime import datetime
from http import HTTPStatus
from typing import List

from fastapi import APIRouter
from pydantic import BaseModel

from core.api import PageMeta
from crawler.models import Link

router = APIRouter(prefix="/links", tags=['Link'])


class LinkResponse(BaseModel):
    id: int
    created_at: datetime
    url: str

    @classmethod
    def from_model(cls, result):
        return cls(
            id=result.id,
            created_at=result.created_at,
            url=result.url,
        )


class LinkPageResponse(BaseModel):
    objects: List[LinkResponse]
    meta: PageMeta


@router.get('/', status_code=HTTPStatus.OK, response_model=LinkPageResponse)
async def get_links(task_id: int, offset: int = 0, limit: int = 10) -> LinkPageResponse:
    filtered_query = Link.objects.filter_by_task_id(task_id)
    objects = [
        LinkResponse.from_model(result)
        async for result in filtered_query.paginate(offset, limit)
    ]
    return LinkPageResponse(
        objects=objects,
        meta=PageMeta(
            offset=offset,
            limit=limit,
            total=await filtered_query.acount(),
        )
    )
