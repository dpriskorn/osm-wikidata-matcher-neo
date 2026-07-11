import httpx
from typing import Any, Self
from pydantic import BaseModel


OVERPASS_API_URL = "https://overpass-api.de/api/interpreter"


class OverpassResult(BaseModel):
    osm_id: str
    osm_type: str
    name: str
    lat: float | None = None
    lon: float | None = None


class OverpassClient:
    def __init__(self) -> None:
        self._client = httpx.AsyncClient(timeout=60.0)

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(self, *args: Any) -> None:
        await self._client.aclose()

    async def query(self, overpass_query: str) -> dict[str, Any]:
        response = await self._client.post(
            OVERPASS_API_URL,
            data={"data": overpass_query},
        )
        response.raise_for_status()
        return response.json()

    def parse_results(self, data: dict[str, Any]) -> list[OverpassResult]:
        elements = data.get("elements", [])
        results = []
        for el in elements:
            osm_type = el.get("type")
            osm_id = str(el.get("id"))
            tags = el.get("tags", {})

            lat = el.get("lat") or el.get("center", {}).get("lat")
            lon = el.get("lon") or el.get("center", {}).get("lon")

            name = tags.get("name", "") or tags.get("name:sv", "") or ""

            if osm_type in ("node", "way", "relation"):
                results.append(OverpassResult(
                    osm_id=osm_id,
                    osm_type=osm_type,
                    name=name,
                    lat=lat,
                    lon=lon,
                ))
        return results
