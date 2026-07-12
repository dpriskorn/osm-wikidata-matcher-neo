import logging
import requests
from functools import lru_cache

from fastapi import APIRouter

log = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["wikidata"])

USER_AGENT = "osm-wikidata-matcher-neo 1.0 (https://github.com/anomalyco/opencode)"


@lru_cache(maxsize=1000)
def _fetch_label_cached(qid: str, lang: str) -> str | None:
    url = f"https://www.wikidata.org/w/rest.php/wikibase/v1/entities/items/{qid}/labels/{lang}"
    headers = {"User-Agent": USER_AGENT}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return data.get(qid, {}).get("value")
    except Exception as e:
        log.warning(f"Failed to fetch label for {qid}: {e}")
    return None


@router.get("/wikidata/{qid}/label")
async def get_wikidata_label(qid: str, lang: str = "en"):
    label = _fetch_label_cached(qid, lang)
    return {"qid": qid, "label": label or qid}
