import logging
from pathlib import Path

logger = logging.getLogger(__name__)

def setup_logging(verbose=False):
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s %(levelname)-8s %(name)s — %(message)s",
        datefmt="%H:%M:%S",
    )

def validate_input(filepath):
    if Path(filepath).is_file():
        logger.info("Input file validated: %s", filepath)
        return True
    logger.error("Input file not found: %s", filepath)
    return False