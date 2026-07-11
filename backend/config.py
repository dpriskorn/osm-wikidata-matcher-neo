from pathlib import Path
from functools import lru_cache
import yaml
from pydantic import BaseModel
from typing import Optional


class WikidataConfig(BaseModel):
    sparql_query: str
    label_property: str
    update_property: str
    not_found_property: str
    not_found_qualifier: Optional[str] = None
    coord_property: Optional[str] = None


class OverpassQuery(BaseModel):
    query: str
    bbox_from_country: bool = False
    bbox_from_coord: bool = False
    bbox_radius_km: float = 1.0
    country_bbox_map: Optional[dict[str, str]] = None
    fallback_bbox: Optional[str] = None


class MatchingConfig(BaseModel):
    method: str
    similarity_threshold: float
    exclude_words: list[str]


class ObjectTypeConfig(BaseModel):
    object_type: str
    label: str
    wikidata: WikidataConfig
    overpass: OverpassQuery
    matching: MatchingConfig


@lru_cache
def get_configs_dir() -> Path:
    return Path(__file__).parent.parent / "configs"


@lru_cache
def get_all_configs() -> dict[str, ObjectTypeConfig]:
    configs: dict[str, ObjectTypeConfig] = {}
    configs_dir = get_configs_dir()

    for yaml_file in configs_dir.glob("*.yaml"):
        with open(yaml_file, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
            obj_type = data["object_type"]
            configs[obj_type] = ObjectTypeConfig(**data)

    return configs


def get_config(object_type: str) -> ObjectTypeConfig:
    configs = get_all_configs()
    if object_type not in configs:
        raise ValueError(f"Unknown object type: {object_type}")
    return configs[object_type]
