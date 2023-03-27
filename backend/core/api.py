from pydantic import BaseModel


class PageMeta(BaseModel):
    offset: int
    limit: int
    total: int
