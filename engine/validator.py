import logging
from typing import List, Optional
from pydantic import BaseModel, Field, ValidationError

logger = logging.getLogger("Priorization_Pipeline")


class Geometry(BaseModel):
    x: float
    y: float

class Parameters(BaseModel):
    damage_grade: int = Field(..., ge=0, le=10)
    usage_frequency: int

class Asset(BaseModel):
    id: str
    geometry: Geometry
    parameters: Parameters
    score: Optional[float] = None

def validate_assets(asset_data_list: List[dict]) -> List[Asset]:
    valid_assets = []

    for data in asset_data_list:
        try:
            asset = Asset(**data)
            valid_assets.append(asset)
        except ValidationError as e:
            logging.error(f"Validation failed for asset {data.get("id", Unknown)}: {e.json()}")

    if len(valid_assets)== len(asset_data_list):
        logging.info("All assets passed validation.")
    else:
        logging.warning(f"Validation partial: {len(valid_assets)}/{len(asset_data_list)} assets valid")

    return valid_assets
