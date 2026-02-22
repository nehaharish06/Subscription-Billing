import pandas as pd
import logging

TARGET_MONTH = 3
TARGET_YEAR = 2024

def aggregate_usage(usage_df):
    if usage_df.empty:
        return {}

    usage_df["usage_date"] = pd.to_datetime(
        usage_df["usage_date"], errors="coerce"
    )

    invalid_dates = usage_df["usage_date"].isna().sum()
    if invalid_dates > 0:
        logging.warning(f"{invalid_dates} invalid date records skipped")

    usage_df = usage_df.dropna(subset=["usage_date"])

    usage_df = usage_df[
        (usage_df["usage_date"].dt.month == TARGET_MONTH) &
        (usage_df["usage_date"].dt.year == TARGET_YEAR)
    ]

    usage_df["data_used_gb"] = pd.to_numeric(
        usage_df["data_used_gb"], errors="coerce"
    ).fillna(0)

    grouped = usage_df.groupby("subscription_id")["data_used_gb"].sum()

    return grouped.to_dict()