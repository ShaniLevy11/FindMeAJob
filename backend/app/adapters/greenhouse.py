import httpx

from app.adapters.base import JobSource
from app.adapters.locations import is_israel
from app.models import Job

BOARD_URL = "https://boards-api.greenhouse.io/v1/boards/{slug}/jobs"


class GreenhouseSource(JobSource):
    name = "greenhouse"

    companies = [
        "nebius",
        "scaleops",
        "similarweb",
        "asteralabs",
        "payoneer",
        "taboola",
        "aidocmedical",
        "nice",
        "appsflyer",
        "connecteam",
        "jfrog",
        "unframe",
        "riskified",
        "gongio",
        "nextinsurance66",
        "melio",
        "pagayais",
        "via",
        "wekatest",
        "doitintl",
        "gitlab",
        "eleoshealth",
        "daylightsecurity",
        "tenableinc",
        "autods",
        "atbayjobs",
        "helloheart",
        "yotpo",
        "guidde",
        "tavily",
        "axonius",
        "forter",
        "datarails",
        "cymulate",
        "drweng",
        "pendo",
        "neosecurityinc",
        "tripledotstudios",
        "apiiro",
        "surfai",
        "cyluscybersecurity",
        "torq",
        "mediaforceltd",
        "safebreach",
        "obligo",
        "nift",
        "wedev",
        "tokensecurity",
        "canopycare",
        "venncity",
        "bluevineisrael",
        "teads1",
        "quanthealth",
        "partnerize",
        "guardz",
        "descope",
        "beyondtrust",
        "figma",
        "optimove",
        "honeycombinsurance",
        "khealthcareers",
        "tomorrow",
        "orioncscybersecurityltd",
        "firstconnectinsurance",
        "zscaler",
        "sweetsecurity",
        "triplewhale",
        "scopely",
        "beamup",
        "eonio",
        "grafanalabs",
        "accessibe",
        "conifersaicareers",
        "brainpop",
        "lightrun",
        "pontera",
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
