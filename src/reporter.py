import json
import logging

def generate_summary(output_df, path):

    summary = {
        "total_subscriptions": len(output_df),
        "active_subscriptions": int((output_df["final_status"] == "ACTIVE").sum()),
        "suspended_subscriptions": int((output_df["final_status"] == "SUSPENDED").sum()),
        "cancelled_subscriptions": int((output_df["final_status"] == "CANCELLED").sum()),
        "total_revenue": float(output_df["total_bill"].sum()),
        "average_bill": float(output_df["total_bill"].mean()) if len(output_df) > 0 else 0
    }

    try:
        with open(path, "w") as f:
            json.dump(summary, f, indent=4)
        logging.info("Billing summary generated")
    except Exception as e:
        logging.error(f"Error writing summary file: {e}")
        