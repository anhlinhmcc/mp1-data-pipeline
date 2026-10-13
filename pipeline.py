"""
Data Processing Pipeline - CLI
DS 3500 - MP1
"""

import argparse
import logging
import sys
from pathlib import Path

from data_loaders import load_data
from data_processor import process_data, create_cleaning_report

logger = logging.getLogger(__name__)


def setup_logging(verbose=False):
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s %(levelname)-8s %(name)s — %(message)s",
        datefmt="%H:%M:%S",
    )


def parse_arguments():
    parser = argparse.ArgumentParser(description="Data Processing Pipeline")
    parser.add_argument("--input", "-i", required=True, help="Path to input file")
    parser.add_argument("--config", required=True, help="Path to YAML config file")
    parser.add_argument("--output", "-o", required=True, help="Path to output file")
    parser.add_argument("--verbose", "-v", action="store_true",
                        help="Enable verbose logging")
    return parser.parse_args()


def validate_input(filepath):
    if Path(filepath).is_file():
        logger.info("Input file validated: %s", filepath)
        return True
    logger.error("Input file not found: %s", filepath)
    return False


def main():
    args = parse_arguments()
    setup_logging(args.verbose)
    logger.debug("Arguments parsed: input=%s, config=%s, output=%s",
                 args.input, args.config, args.output)

    if not validate_input(args.input):
        sys.exit(1)
    if not validate_input(args.config):
        sys.exit(1)

    try:
        df = load_data(args.input)
        config = load_data(args.config)
    except ValueError:
        sys.exit(1)

    df_original = df.copy()

    try:
        df = process_data(df, config)
    except ValueError:
        sys.exit(1)

    report = create_cleaning_report(df_original, df)
    logger.info("Processing complete: %d → %d rows", len(df_original), len(df))
    print(report)

    df.to_csv(args.output, index=False)
    logger.info("Saved cleaned data to %s", args.output)


if __name__ == "__main__":
    main()