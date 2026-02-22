import os
import logging
import pandas as pd

from loader import load_csv
from usage_aggregator import aggregate_usage
from billing_engine import calculate_bill
from status_engine import evaluate_status
from reporter import generate_summary

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_DIR = os.path.join(BASE_DIR, "data")
LOG_DIR = os.path.join(BASE_DIR, "logs")

os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    filename=os.path.join(LOG_DIR, "billing.log"),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def run():

    subscriptions = load_csv(os.path.join(DATA_DIR, "subscriptions.csv"))
    usage = load_csv(os.path.join(DATA_DIR, "usage.csv"))

    usage_map = aggregate_usage(usage)

    results = []

    for _, row in subscriptions.iterrows():

        subscription_id = row["subscription_id"]
        status = row["status"]

        total_usage = usage_map.get(subscription_id, 0)

        monthly_fee = float(row["monthly_fee"])
        usage_limit = float(row["usage_limit_gb"])

        total_bill, overage = calculate_bill(
            monthly_fee,
            total_usage,
            usage_limit,
            status
        )

        final_status = evaluate_status(
            status,
            total_usage,
            usage_limit
        )

        results.append({
            "subscription_id": subscription_id,
            "customer_id": row["customer_id"],
            "plan": row["plan"],
            "total_usage_gb": total_usage,
            "overage_gb": overage,
            "total_bill": total_bill,
            "final_status": final_status
        })

    output_df = pd.DataFrame(results)

    output_df.to_csv(os.path.join(BASE_DIR, "billing_output.csv"), index=False)

    generate_summary(
        output_df,
        os.path.join(BASE_DIR, "billing_summary.json")
    )

    logging.info("Billing process completed successfully")

if __name__ == "__main__":
    run()