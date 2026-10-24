from datetime import datetime

from pydantic import BaseModel


class Job(BaseModel):
    source: str
    external_id: str
    title: str
    company: str
    location: str | None = None
    url: str
    updated_at: datetime | None = None
