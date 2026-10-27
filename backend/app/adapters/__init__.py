import asyncio

from app.adapters.ashby import AshbySource
from app.adapters.base import JobSource
from app.adapters.comeet import ComeetSource
from app.adapters.greenhouse import GreenhouseSource
from app.adapters.lever import LeverSource
from app.models import Job

SOURCES: list[JobSource] = [
    GreenhouseSource(),
    ComeetSource(),
    AshbySource(),
    LeverSource(),
]


async def fetch_all_jobs() -> list[Job]:
    tasks = []
    for source in SOURCES:
        tasks.append(source.fetch_all_jobs())

    results = await asyncio.gather(*tasks)

    all_jobs: list[Job] = []
    for jobs in results:
        all_jobs.extend(jobs)

    return all_jobs
