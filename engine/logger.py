import logging
from pathlib import PATH

BASE_PATH = Path(__file__).resolve().parent.parent

def setup_logger():
    log_dir = Base_PATH / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)

    log_file = os.path.join(log_dir, "app.log")

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger("Prioritization_Pipeline")
