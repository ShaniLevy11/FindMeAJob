import httpx

from app.adapters.base import JobSource
from app.adapters.locations import is_israel
from app.models import Job

BOARD_URL = "https://boards-api.greenhouse.io/v1/boards/{slug}/jobs"


class GreenhouseSource(JobSource):
    name = "greenhouse"

    companies = [
        "similarweb",
        "taboola",
        "payoneer",
        "appsflyer",
        "jfrog",
        "riskified",
        "melio",
        "nice",
        "gongio",
        "unframe",
    ]

    async def fetch_company_jobs(self, client: httpx.AsyncClient, slug: str) -> list[Job]:
        resp = await client.get(BOARD_URL.format(slug=slug))
        resp.raise_for_status()
        jobs: list[Job] = []

        for raw_job in resp.json()["jobs"]:
            location_data = raw_job.get("location")
            if location_data:
                location = location_data.get("name")
            else:
                location = None

            if not is_israel(location):
                continue

            company = raw_job.get("company_name")
            if not company:
                company = slug

            job = Job(
                source=self.name,
                external_id=str(raw_job["id"]),
                title=raw_job["title"],
                company=company,
                location=location,
                url=raw_job["absolute_url"],
                updated_at=raw_job.get("updated_at"),
            )
            jobs.append(job)

        return jobs
