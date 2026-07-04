import json
import logging

logger = logging.getLogger("Prioritization_Pipeline")

def export_to_geojson(assets, output_path):
    try:
        features = []
        for asset in assets:
            data = asset.model_dump() if hasattr(asset, "model_dump") else asset
            
            features.append({
                "type": "Feature",
                "properties": {
                    "id": data["id"],
                    "name": data.get("name") or data["id"],
                    "score": data.get("score", 0),
                    "condition": data["values"]["condition"],
                    "criticality": data["values"]["criticality"]
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [data["geometry"]["x"], data["geometry"]["y"]]
                }
            })

        with open(output_path, "w") as f:
            json.dump({"type": "FeatureCollection", "features": features},f)

        logger.info(f"Successfully exported {len(features)} features to {output_path}.")

    except Exception as e:
        logger.error(f"Error during export: {e}")

