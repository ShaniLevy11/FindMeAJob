import asyncio

from fastapi import APIRouter, HTTPException

from app import adapters, db
from app.models import Job

router = APIRouter(prefix="/jobs", tags=["jobs"])

sync_lock = asyncio.Lock()


# GET /api/jobs
@router.get("", response_model=list[Job])
async def list_jobs():
    cursor = db.get_db().jobs.find({"closed_at": None}, {"_id": 0}).sort("updated_at", -1)
    return await cursor.to_list()


@router.post("/sync")
async def sync_jobs():
    if sync_lock.locked():
        raise HTTPException(status_code=409, detail="A sync is already running")

    async with sync_lock:
        jobs_collection = db.get_db().jobs
        count_before = await jobs_collection.count_documents({})

        fetched = await adapters.fetch_all_jobs()

        count_after = await jobs_collection.count_documents({})
        open_jobs = await jobs_collection.count_documents({"closed_at": None})

    return {"fetched": len(fetched), "new_jobs": count_after - count_before, "open_jobs_in_db": open_jobs}
