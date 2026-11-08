import asyncio
import logging
import time
from datetime import datetime, timezone

import httpx
from pymongo import UpdateOne

from app import db
from app.categories import categorize
from app.models import Job

logger = logging.getLogger("findmeajob.sync")


class JobSource:
    name: str = ""

    companies: list = []

    client_options: dict = {"timeout": 20}

    async def fetch_company_jobs(self, client: httpx.AsyncClient, company) -> list[Job]:
        raise NotImplementedError

    def company_key(self, company) -> str:
        return str(company)

    def prepare_jobs(self, company, jobs: list[Job]) -> None:
        key = self.company_key(company)
        for job in jobs:
            job.company_key = key
            job.categories = categorize(job.title)

    async def save_new_jobs(self, company, jobs: list[Job]) -> int:
        if not jobs:
            return 0

        now = datetime.now(timezone.utc)
        operations = []
        for job in jobs:
            fields_on_insert = job.model_dump(exclude={"last_seen_at", "closed_at"})
            fields_on_insert["first_seen_at"] = now
            operations.append(
                UpdateOne(
                    {"source": job.source, "external_id": job.external_id},
                    {
                        "$setOnInsert": fields_on_insert,
                        "$set": {"last_seen_at": now, "closed_at": None},
                    },
                    upsert=True,
                )
            )

        result = await db.get_db().jobs.bulk_write(operations, ordered=False)
        return result.upserted_count

    async def fetch_one(self, client: httpx.AsyncClient, company):
        try:
            jobs = await self.fetch_company_jobs(client, company)
        except Exception as error:
            return company, None, error
        return company, jobs, None

    async def fetch_all_jobs(self) -> list[Job]:
        all_jobs: list[Job] = []
        total = len(self.companies)
        done = 0
        failed = 0
        new_total = 0
        started = time.perf_counter()

        logger.info("%s: fetching %d companies", self.name, total)

        async with httpx.AsyncClient(**self.client_options) as client:
            # each item is a function that fetches jobs for a single company
            tasks = []
            for company in self.companies:
                tasks.append(self.fetch_one(client, company))

            # loop over tasks as they finish, so we can process results as they come in
            for finished in asyncio.as_completed(tasks):
                company, jobs, error = await finished
                done += 1
                key = self.company_key(company)

                if error is not None:
                    failed += 1
                    logger.warning("%s [%d/%d] %s: FAILED %r", self.name, done, total, key, error)
                    continue

                self.prepare_jobs(company, jobs)
                all_jobs.extend(jobs)

                new_count = await self.save_new_jobs(company, jobs)
                new_total += new_count
                logger.info("%s [%d/%d] %s: %d jobs, %d new", self.name, done, total, key, len(jobs), new_count)

        elapsed = time.perf_counter() - started
        logger.info(
            "%s: done in %.1fs - %d jobs, %d new, %d failed",
            self.name, elapsed, len(all_jobs), new_total, failed,
        )

        return all_jobs
