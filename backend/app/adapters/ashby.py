import httpx

from app.adapters.base import JobSource
from app.adapters.locations import is_israel
from app.models import Job

BOARD_URL = "https://api.ashbyhq.com/posting-api/job-board/{slug}"


def job_is_in_israel(raw_job: dict) -> bool:
    address = raw_job.get("address") or {}
    postal_address = address.get("postalAddress") or {}
    country = postal_address.get("addressCountry")
    if country:
        return country.lower() == "israel"

    return is_israel(raw_job.get("location"))


class AshbySource(JobSource):
    name = "ashby"

    companies = [
        "monday.com",
        "moonactive",
        "wonderful",
        "irregular",
        "echo.ai",
        "zafran-security",
        "pointfive",
        "tavily",
        "nexxen",
        "Viz.ai",
        "brandlight",
        "simply",
        "glow",
        "huskeys",
        "oak",
        "airwallex",
        "shapes",
        "reindeer-ai",
        "finout",
        "act-security",
        "stigg",
        "chainalysis-careers",
        "semperis",
        "crusoe",
        "matia",
        "april",
        "loora",
        "honeybook",
        "lumana",
        "chamelio",
        "mend-io",
        "clickhouse",
        "harmony",
        "snowflake",
        "sisense",
        "enclave",
        "sweep",
        "ledge",
        "candex",
        "lilt-production",
        "HUMAN",
        "unit",
        "zip",
        "singular",
        "Snappy",
        "pi-security",
        "menlosecurity",
        "originhq",
        "trm-labs",
        "wand-ai",
        "Spacial",
        "chalk",
    ]

    async def fetch_company_jobs(self, client: httpx.AsyncClient, slug: str) -> list[Job]:
        resp = await client.get(BOARD_URL.format(slug=slug))
        resp.raise_for_status()
        jobs: list[Job] = []

        for raw_job in resp.json()["jobs"]:
            if not raw_job.get("isListed", True):
                continue

            if not job_is_in_israel(raw_job):
                continue

            job = Job(
                source=self.name,
                external_id=raw_job["id"],
                title=raw_job["title"],
                company=slug,
                location=raw_job.get("location"),
                url=raw_job["jobUrl"],
                updated_at=raw_job.get("publishedAt"),
            )
            jobs.append(job)

        return jobs
