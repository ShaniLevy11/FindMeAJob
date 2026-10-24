import re

import httpx

from app.adapters.base import JobSource
from app.models import Job

CAREERS_PAGE_URL = "https://www.comeet.com/jobs/{slug}/{uid}"
POSITIONS_URL = "https://www.comeet.co/careers-api/2.0/company/{uid}/positions"


class ComeetSource(JobSource):
    name = "comeet"

    companies = [
        ("abra_rnd", "15.007"),
        ("comm-it", "76.008"),
        ("kelatechnologies", "2A.007"),
        ("crossriver", "C7.00F"),
        ("cyera", "17.008"),
        ("SolarEdge", "71.00A"),
        ("guardio", "57.000"),
        ("biocatch", "03.00E"),
        ("enlightenergy", "99.006"),
        ("cardosystems", "F2.003"),
        ("deltagalil", "78.000"),
        ("vastdata", "43.001"),
        ("infinidat", "D6.003"),
        ("paragon", "76.006"),
        ("quantummachines", "D6.000"),
        ("Cellebrite", "C3.00F"),
        ("inmanage", "B7.006"),
        ("maytronics", "E3.008"),
        ("team8", "61.003"),
        ("arpeely", "57.001"),
    ]

    client_options = {
        "timeout": 20,
        "follow_redirects": True,
        "headers": {"User-Agent": "Mozilla/5.0"},
    }

    async def get_token(self, client: httpx.AsyncClient, slug: str, uid: str) -> str:
        resp = await client.get(CAREERS_PAGE_URL.format(slug=slug, uid=uid))
        resp.raise_for_status()
        match = re.search(r'"token":\s*"([0-9A-Fa-f]+)"', resp.text)
        if not match:
            raise ValueError("token not found in careers page")
        return match.group(1)

    async def fetch_company_jobs(self, client: httpx.AsyncClient, company: tuple[str, str]) -> list[Job]:
        slug, uid = company
        token = await self.get_token(client, slug, uid)

        resp = await client.get(POSITIONS_URL.format(uid=uid), params={"token": token})
        resp.raise_for_status()
        jobs: list[Job] = []

        for raw_job in resp.json():
            location_data = raw_job.get("location") or {}

            if location_data.get("country") != "IL":
                continue

            job = Job(
                source=self.name,
                external_id=raw_job["uid"],
                title=raw_job["name"],
                company=raw_job.get("company_name") or slug,
                location=location_data.get("name"),
                url=raw_job["url_comeet_hosted_page"],
                updated_at=raw_job.get("time_updated"),
            )
            jobs.append(job)

        return jobs
