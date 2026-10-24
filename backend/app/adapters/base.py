import asyncio

import httpx

from app.models import Job


class JobSource:
    name: str = ""

    companies: list = []

    client_options: dict = {"timeout": 20}

    async def fetch_company_jobs(self, client: httpx.AsyncClient, company) -> list[Job]:
        raise NotImplementedError

    async def fetch_all_jobs(self) -> list[Job]:
        all_jobs: list[Job] = []

        async with httpx.AsyncClient(**self.client_options) as client:
            tasks = []
            for company in self.companies:
                task = self.fetch_company_jobs(client, company)
                tasks.append(task)

            results = await asyncio.gather(*tasks, return_exceptions=True)

        for company, result in zip(self.companies, results):
            if isinstance(result, Exception):
                print(f"{self.name}: failed to fetch {company}: {result!r}")
            else:
                all_jobs.extend(result)

        return all_jobs
