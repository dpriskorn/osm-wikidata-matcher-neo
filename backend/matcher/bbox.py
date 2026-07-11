import logging
import math
from typing import Any
from clients.wikidata import WikidataItem, WikidataClient
from clients.overpass import OverpassClient
from matcher.base import Matcher, MatchCandidate
from config import ObjectTypeConfig


log = logging.getLogger(__name__)


class BBoxMatcher(Matcher[WikidataItem]):
    def __init__(
        self,
        config: ObjectTypeConfig,
        wikidata_client: WikidataClient,
        overpass_client: OverpassClient,
    ):
        super().__init__(
            exclude_words=config.matching.exclude_words,
            threshold=config.matching.similarity_threshold,
        )
        self.config = config
        self.wikidata = wikidata_client
        self.overpass = overpass_client
        self.radius_km = config.overpass.bbox_radius_km

    async def find_matches(self, wikidata_item: WikidataItem) -> tuple[list[MatchCandidate[WikidataItem]], str | None]:
        if not wikidata_item.coord:
            log.warning(f"BBoxMatcher: no coordinates for {wikidata_item.label}")
            return [], None

        bbox = self._coord_to_bbox(wikidata_item.coord.lat, wikidata_item.coord.lon)
        log.debug(f"BBoxMatcher: bbox={bbox} for {wikidata_item.label} at {wikidata_item.coord.lat},{wikidata_item.coord.lon}")
        query = self.config.overpass.query.replace("{{bbox}}", bbox)

        raw_results = await self.overpass.query(query)
        osm_items = self.overpass.parse_results(raw_results)
        osm_timestamp = raw_results.get("osm3s", {}).get("timestamp_osm_base")

        candidates = []
        for osm in osm_items:
            sim = self.similarity(wikidata_item.label, osm.name)
            if sim >= self.threshold:
                candidates.append(MatchCandidate(
                    item=wikidata_item,
                    similarity=sim,
                    osm_id=osm.osm_id,
                    osm_type=osm.osm_type,
                    osm_name=osm.name,
                ))

        candidates.sort(key=lambda c: c.similarity, reverse=True)
        log.info(f"BBoxMatcher: found {len(candidates)} matches for {wikidata_item.label}")
        for c in candidates:
            log.debug(f"  - {c.osm_type}/{c.osm_id} '{c.osm_name}' similarity={c.similarity:.2f}")
        return candidates, osm_timestamp

    def _coord_to_bbox(self, lat: float, lon: float) -> str:
        km_per_deg_lat = 111.32
        km_per_deg_lon = 111.32 * math.cos(math.radians(lat))
        delta_lat = self.radius_km / km_per_deg_lat
        delta_lon = self.radius_km / km_per_deg_lon
        south = lat - delta_lat
        north = lat + delta_lat
        west = lon - delta_lon
        east = lon + delta_lon
        return f"{south},{west},{north},{east}"
