import json
import csv
import logging

logger = logging.getLogger("Prioritization_Pipeline")


def csv_to_json(csv_file_path):
    assets = []
    try:
        with open(csv_file_path, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    asset = {
                        "id":row["id"],
                        "geometry":{"x": float(row["x"]), "y": float(row["y"])},
                        "parameters": {
                            "damage_grade": int(row["damage_grade"]),
                            "usage_frequency": int(row["usage_frequency"])
                        },
                        "score": None
                    }
                    assets.append(asset)
                except (ValueError, KeyError) as e:
                    logger.warning(f"Failed to process row_ {e}")
        logger.info(f"Successfully loaded {len(assets)} records from {csv_file_path}.")
    except FileNotFoundError:
        logger.error(f"File not found: {csv_file_path}")
    
    return assets

