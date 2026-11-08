import asyncio
import logging
import time

from app.adapters.ashby import AshbySource
from app.adapters.base import JobSource
from app.adapters.comeet import ComeetSource
from app.adapters.greenhouse import GreenhouseSource
from app.adapters.lever import LeverSource
from app.models import Job

logger = logging.getLogger("findmeajob.sync")

SOURCES: list[JobSource] = [
    GreenhouseSource(),
    ComeetSource(),
    AshbySource(),
    LeverSource(),
]


async def fetch_all_jobs() -> list[Job]:
    started = time.perf_counter()
    logger.info("sync started: %d sources", len(SOURCES))

    tasks = []
    for source in SOURCES:
        tasks.append(source.fetch_all_jobs())

    results = await asyncio.gather(*tasks)

    all_jobs: list[Job] = []
    for jobs in results:
        all_jobs.extend(jobs)

    elapsed = time.perf_counter() - started
    logger.info("sync finished in %.1fs - %d jobs fetched", elapsed, len(all_jobs))

    return all_jobs
