from datetime import datetime, timezone

import httpx

from app.adapters.base import JobSource
from app.adapters.locations import is_israel
from app.models import Job

BOARD_URL = "https://api.lever.co/v0/postings/{slug}"


def job_is_in_israel(raw_job: dict) -> bool:
    country = raw_job.get("country")
    if country:
        return country.upper() == "IL"

    categories = raw_job.get("categories") or {}
    return is_israel(categories.get("location"))


class LeverSource(JobSource):
    name = "lever"

    companies = [
        "jobgether",
        "parallelwireless",
        "d-fendsolutions",
        "cloudinary",
        "CYE",
        "weloglobal",
        "walkme",
        "houzz",
        "veeva",
        "biocatch",
        "lendbuzz",
        "tonkean",
        "airslate",
        "controlup",
        "Zadara",
        "oktopost",
        "logz",
        "aleph",
        "spinai",
        "idt",
        "z1tech",
        "getwingapp",
        "traildsoftware",
        "Sauce",
        "usasurveyjob",
        "terrific-innovation",
    ]

    async def fetch_company_jobs(self, client: httpx.AsyncClient, slug: str) -> list[Job]:
        resp = await client.get(BOARD_URL.format(slug=slug), params={"mode": "json"})
        resp.raise_for_status()
        jobs: list[Job] = []

        for raw_job in resp.json():
            if not job_is_in_israel(raw_job):
                continue

            categories = raw_job.get("categories") or {}

            created_at = raw_job.get("createdAt")
            if created_at:
                posted_at = datetime.fromtimestamp(created_at / 1000, tz=timezone.utc)
            else:
                posted_at = None

            job = Job(
                source=self.name,
                external_id=raw_job["id"],
                title=raw_job["text"],
                company=slug,
                location=categories.get("location"),
                url=raw_job["hostedUrl"],
                updated_at=posted_at,
            )
            jobs.append(job)

        return jobs
