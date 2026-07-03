import os
import yaml
import logging

from engine.logger import setup_logger
from engine.adapter import csv_to_json
from engine.validator import validate_assets
from engine.scoring_engine import calculate_priority
from engine.database import save_to_sql
from engine.gis_export import export_to_geojson

logger = setup_logger()

def main():
    logging.info("Starting processing pipeline.")

    base_path = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(base_path, "config", "settings.yaml")
    
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)

    criteria = config["weights"]
    paths = config["paths"]
    
    raw_data = csv_to_json(paths["input_csv"])
    assets = validate_assets(raw_data)

    if not assets:
        logging.error("No valid assets found. Stopping pipeline.")
        return

    processed_assets = calculate_priority(assets, criteria)

    for asset in processed_assets:
        logging.info(f"Asset ID: {asset.id} - Final Score: {asset.score:.2f}")
        

    save_to_sql([a.model_dump() for a in processed_assets], paths["output_db"])
    export_to_geojson(processed_assets, paths["output_geojson"])
    
if __name__ == "__main__":
    main()
                    
    
