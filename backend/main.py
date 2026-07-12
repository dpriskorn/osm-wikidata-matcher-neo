import logging
import os
import sys
from contextlib import asynccontextmanager

from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, HTTPException  # noqa: E402
from fastapi.middleware.cors import CORSMiddleware  # noqa: E402

from db import init_db, cleanup_expired_cache  # noqa: E402

logging.basicConfig(
    level=os.environ.get("LOG_LEVEL", "INFO").upper(),
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    stream=sys.stdout,
    force=True,
)

logging.getLogger("httpcore").setLevel(logging.WARNING)
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("aiosqlite").setLevel(logging.WARNING)

log = logging.getLogger(__name__)

from routers import matcher  # noqa: E402
from routers.auth import router as auth_router  # noqa: E402
from routers.wikidata import router as wikidata_router  # noqa: E402


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    deleted = await cleanup_expired_cache()
    if deleted > 0:
        log.info(f"Cleaned up {deleted} expired label cache entries")
    yield


app = FastAPI(title="Wikidata-OSM Matcher", version="0.1.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(matcher.router)
app.include_router(auth_router)
app.include_router(wikidata_router)


@app.exception_handler(ValueError)
async def value_error_handler(request, exc):
    raise HTTPException(status_code=500, detail=str(exc))


@app.get("/health")
async def health():
    return {"status": "ok"}


log.info("Wikidata-OSM Matcher started")
