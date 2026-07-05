import csv
import logging

logger = logging.getLogger("Prioritization_Pipeline")


def csv_to_json(csv_file_path, criteria):
    assets = []
    try:
        with open(csv_file_path, mode="r", encoding="utf-8-sig") as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    values = {}
                    for crit in criteria:
                        column = crit["column_name"]
                        raw = row[column]
                        if "mapping" in crit:
                            try:
                                key = int(raw)
                            except ValueError:
                                key = raw
                            values[crit["name"]] = crit["mapping"][key]
                        else:
                            values[crit["name"]] = float(raw)

                    asset = {
                        "id":row["id"],
                        "name": (row.get("name") or "").strip() or row["id"],
                        "geometry":{"x": float(row["x"]), "y": float(row["y"])},
                        "values": values,
                        "score": None
                    }
                    assets.append(asset)
                except (ValueError, KeyError) as e:
                    logger.warning(f"Failed to process row: (id={row.get("id", "?")}): {e}")
                    
        logger.info(f"Successfully loaded {len(assets)} records from {csv_file_path}.")
    except FileNotFoundError:
        logger.error(f"File not found: {csv_file_path}")
    except UnicodeDecodeError:
        logger.error(f"Encoding error: {csv_file_path} is not utf-8. Please re-save the file as UTF-8.")
    
    return assets

