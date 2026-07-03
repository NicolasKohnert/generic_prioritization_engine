import logging

logger = logging.getLogger("Priorization_Pipeline")

def calculate_priority(assets, criteria):
    processed_assets = []
    logging.info(F"Starting priority calculation for {len(assets)} assets.")
    
    for asset in assets:
        try:

            max_dmg = criteria["max_damage"]
            max_freq = criteria["max_usage_frequency"]
            
            cond_score = asset.parameters.damage_grade * criteria["condition"]
            freq_score = asset.parameters.usage_frequency * criteria["criticality"]

            max_possible_score = (max_dmg * criteria["condition"]) + (max_freq * criteria["criticality"])
            raw_score = cond_score + freq_score
            
            asset.score =raw_score/max_possible_score
            processed_assets.append(asset)

        except KeyError as e:
            logging.warning(f"Missing parameters in asset {asset.id}: {e}")
        except Exception as e:
            logging.error(f"Unexpected error calculating score for asset {asset.id}: {e}")
    logging.info("Priority calculation completed")
    return processed_assets
