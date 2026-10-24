from fastapi import APIRouter

from app import adapters
from app.models import Job

router = APIRouter(prefix="/jobs", tags=["jobs"])


@router.get("", response_model=list[Job])
async def list_jobs():
    return await adapters.fetch_all_jobs()
