import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app import db
from app.routers import jobs

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    datefmt="%H:%M:%S",
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    db.connect()
    await db.create_indexes()
    yield
    await db.disconnect()


app = FastAPI(title="FindMeAJob", lifespan=lifespan)
app.include_router(jobs.router)


@app.get("/health")
async def health():
    await db.get_db().command("ping")
    return {"status": "ok", "mongo": "connected"}

@app.get("/")
async def root():
    return {"status": "ok"}