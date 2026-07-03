import yaml
import logging
from pathlib import Path

from engine.logger import setup_logger
from engine.adapter import csv_to_json
from engine.validator import validate_assets
from engine.scoring_engine import calculate_priority
from engine.database import save_to_sql
from engine.gis_export import export_to_geojson

BASE_PATH = Path(__file__).resolve().parent

logger = setup_logger()

def main():
    logger.info("Starting processing pipeline.")

    config_path = BASE_PATH / "config" / "settings.ymal"
    
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)

    criteria = config["weights"]
    bounds = config["bounds"]
    
    paths = {key: BASE_PATH / value for key, value in config["paths"].items()}
    
    raw_data = csv_to_json(paths["input_csv"])
    assets = validate_assets(raw_data)

    if not assets:
        logger.error("No valid assets found. Stopping pipeline.")
        return

    processed_assets = calculate_priority(assets, criteria, bounds)

    for asset in processed_assets:
        logger.info(f"Asset ID: {asset.id} - Final Score: {asset.score:.2f}")
        

    save_to_sql([a.model_dump() for a in processed_assets], paths["output_db"])
    export_to_geojson(processed_assets, paths["output_geojson"])
    
if __name__ == "__main__":
    main()
                    
    
