import logging
import httpx

from fastapi import APIRouter

from db import get_cached_label, set_cached_label

log = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["wikidata"])

USER_AGENT = "osm-wikidata-matcher-neo 1.0 (https://github.com/anomalyco/opencode)"


async def _fetch_label(qid: str, lang: str) -> str | None:
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
                return label
        except Exception as e:
            log.warning(f"Failed to fetch label for {qid}: {e}")
    return None


@router.get("/wikidata/{qid}/label")
async def get_wikidata_label(qid: str, lang: str = "en") -> dict[str, str]:
    cached = await get_cached_label(qid, lang)
    if cached:
        return {"qid": qid, "label": cached}

    label = await _fetch_label(qid, lang)
    if label is None and lang != "en":
        label = await _fetch_label(qid, "en")

    if label:
        await set_cached_label(qid, lang, label)

    return {"qid": qid, "label": label or qid}
