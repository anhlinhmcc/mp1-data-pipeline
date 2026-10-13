from pathlib import Path
import logging
import pandas as pd
import json
import yaml

logger = logging.getLogger(__name__)


def load_csv(filepath):
    df = pd.read_csv(filepath)
    logger.info("Loaded CSV file: %s (%d rows)", filepath, len(df))
    return df


def load_json(filepath):
    with open(filepath) as f:
        data = json.load(f)
    logger.info("Loaded JSON file: %s", filepath)
    return data


def load_yaml(filepath):
    with open(filepath) as f:
        data = yaml.safe_load(f)
    logger.info("Loaded YAML file: %s", filepath)
    return data


def load_data(filepath):
    path = Path(filepath)
    ext = path.suffix.lower()
    if ext == ".csv":
        return load_csv(path)
    if ext == ".json":
        return load_json(path)
    if ext in (".yaml", ".yml"):
        return load_yaml(path)
    logger.error("Unsupported file format: %s", ext)
    raise ValueError(f"Unsupported file format: {ext}")