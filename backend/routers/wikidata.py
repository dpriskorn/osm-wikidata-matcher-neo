import asyncio
import logging
import httpx

from fastapi import APIRouter

log = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["wikidata"])

USER_AGENT = "osm-wikidata-matcher-neo 1.0 (https://github.com/anomalyco/opencode)"

_cache: dict[tuple[str, str], str] = {}
_cache_lock = asyncio.Lock()


async def _fetch_label_cached(qid: str, lang: str) -> str | None:
    cache_key = (qid, lang)
    async with _cache_lock:
        if cache_key in _cache:
            return _cache[cache_key]

    url = f"https://www.wikidata.org/w/rest.php/wikibase/v1/entities/items/{qid}/labels/{lang}"
    headers = {"User-Agent": USER_AGENT}
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=10.0)
            if response.status_code == 200:
                try:
                    data = response.json()
                    if isinstance(data, str):
                        label = data
                    else:
                        label = data.get(qid, {}).get("value")
                except Exception:
                    text = response.text.strip()
                    label = text if text and text != "null" else None

                if label:
                    async with _cache_lock:
                        _cache[cache_key] = label
                return label
        except Exception as e:
            log.warning(f"Failed to fetch label for {qid}: {e}")
    return None


@router.get("/wikidata/{qid}/label")
async def get_wikidata_label(qid: str, lang: str = "en"):
    label = await _fetch_label_cached(qid, lang)
    if label is None and lang != "en":
        label = await _fetch_label_cached(qid, "en")
    return {"qid": qid, "label": label or qid}
