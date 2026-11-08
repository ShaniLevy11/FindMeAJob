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
    company_key: str | None = None
    categories: list[str] = []
    first_seen_at: datetime | None = None
    last_seen_at: datetime | None = None
    closed_at: datetime | None = None
