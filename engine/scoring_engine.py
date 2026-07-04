import logging

logger = logging.getLogger("Prioritization_Pipeline")


def calculate_priority(assets, criteria):
    processed_assets = []
    logger.info(f"Starting priority calculation for {len(assets)} assets.")

    for asset in assets:
        try:
            raw_score = 0.0
            max_possible_score= 0.0

            for crit in criteria:
                name = crit["name"]
                weight = crit["weight"]
                max_value = crit["max"]

                raw_score += asset.values[name] * weight
                max_possible_score += max_value * weight


            asset.score = raw_score / max_possible_score
            processed_assets.append(asset)

        except KeyError as e:
            logger.error(f"Missing config key while scoring asset {asset.id}: {e}")
        except ZeroDivisionError as e:
            logger.error(f"Max possible score is zero for asset {asset.id} - check weights/max in config")            
        except Exception as e:
            logger.error(f"Unexpected error calculating score for asset {asset.id}: {e}")

    logger.info("Priority calculation completed")
    return processed_assets
