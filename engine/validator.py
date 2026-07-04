import logging
from typing import Dict, Optional
from pydantic import BaseModel, Field, ValidationError, model_validator

logger = logging.getLogger("Prioritization_Pipeline")


class Geometry(BaseModel):
    x: float
    y: float


class Asset(BaseModel):
    id: str
    name: Optional[str] = None
    geometry: Geometry
    values: Dict[str, float]
    score: Optional[float] = None

    @model_validator(mode="after")
    def check_values_in_range(self):
        for name, value in self.values.items():
            if value < 0:
                raise ValueError(f"Criterion '{name}' has a negative value: {value}")
        return self


def validate_assets(asset_data_list, criteria):
    valid_assets = []

    if not asset_data_list:
        logger.warning("No asset data to validate.")
        return valid_assets

    expected = {crit["name"] for crit in criteria}

    for data in asset_data_list:
        try:
            asset = Asset(**data)

            missing = expected - set(asset.values.keys())
            if missing:
                raise ValueError(f"Missing criteria: {missing}")
            
            valid_assets.append(asset)
        except (ValidationError, ValueError) as e:
            logger.error(f"Validation failed for asset {data.get('id', 'Unknown')}: {e}")

    if len(valid_assets) == len(asset_data_list):
        logger.info("All assets passed validation.")
    else:
        logger.warning(f"Validation partial: {len(valid_assets)}/{len(asset_data_list)} assets valid")

    return valid_assets
