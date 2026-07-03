import logging

logger = logging.getLogger("Priorization_Pipeline")

def calculate_priority(assets, criteria):
    processed_assets = []
    logging.info(F"Starting priority calculation for {len(assets)} assets.")
    
    for asset in assets:
        try:
            cond_score = asset.parameters.damage_grade * criteria["condition"]
            freq_score = asset.parameters.usage_frequency * criteria["criticality"]

            asset.score =cond_score + freq_score
            processed_assets.append(asset)

        except KeyError as e:
            logging.warning(f"Missing parameters in asset {asset.id}: {e}")
        except Exception as e:
            logging.error(f"Unexpected error calculating score for asset {asset.id}: {e}")
    logging.info("Priority calculation completed")
    return processed_assets
