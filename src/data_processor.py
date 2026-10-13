import logging
import pandas as pd

logger = logging.getLogger(__name__)


def remove_duplicates(df):
    before = len(df)
    df = df.drop_duplicates()
    logger.debug("remove_duplicates: %d → %d rows", before, len(df))
    return df


def handle_missing(df, axis="rows"):
    if axis == "rows":
        before = len(df)
        df = df.dropna(axis=0)
        logger.debug("handle_missing: %d → %d rows", before, len(df))
    elif axis == "columns":
        before = df.shape[1]
        df = df.dropna(axis=1)
        logger.debug("handle_missing: %d → %d columns", before, df.shape[1])
    else:
        logger.error("Unsupported axis: %s", axis)
        raise ValueError(f"Unsupported axis: {axis}")
    return df


def remove_outliers(df, columns, method, threshold):
    if method not in ("iqr", "zscore"):
        logger.error("Unsupported outlier method: %s", method)
        raise ValueError(f"Unsupported outlier method: {method}")

    for col in columns:
        if col not in df.columns:
            logger.warning("Column not found: %s", col)
            continue
        if not pd.api.types.is_numeric_dtype(df[col]):
            logger.warning("Column is not numeric: %s", col)
            continue

        series = df[col]
        if method == "iqr":
            q1, q3 = series.quantile(0.25), series.quantile(0.75)
            iqr = q3 - q1
            lower, upper = q1 - threshold * iqr, q3 + threshold * iqr
        else:  # zscore
            mean, std = series.mean(), series.std()
            lower, upper = mean - threshold * std, mean + threshold * std

        keep = series.isna() | ((series >= lower) & (series <= upper))
        removed = int((~keep).sum())
        df = df[keep]
        logger.debug("%s: method=%s, threshold=%s, lower=%s, upper=%s, removed=%d",
                     col, method, threshold, lower, upper, removed)
    return df


def process_data(df, config):
    settings = config["processing"]

    if settings.get("remove_duplicates"):
        df = remove_duplicates(df)

    missing = settings.get("missing", {})
    if missing.get("enabled"):
        df = handle_missing(df, missing.get("axis", "rows"))

    outliers = settings.get("outliers", {})
    if outliers.get("enabled"):
        df = remove_outliers(df, outliers["columns"], outliers["method"],
                             outliers["threshold"])
    return df


def create_cleaning_report(df_before, df_after):
    return {
        "rows_before": len(df_before),
        "rows_after": len(df_after),
        "rows_removed": len(df_before) - len(df_after),
        "columns_before": df_before.shape[1],
        "columns_after": df_after.shape[1],
        "columns_removed": df_before.shape[1] - df_after.shape[1],
    }   