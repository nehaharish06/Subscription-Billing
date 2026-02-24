from flask import Flask, render_template, request, send_file
import os
import pandas as pd
import logging

from src.usage_aggregator import aggregate_usage
from src.billing_engine import calculate_bill
from src.status_engine import evaluate_status
from src.reporter import generate_summary

app = Flask(__name__)

UPLOAD_FOLDER = "data"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    filename="logs/billing.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/process", methods=["POST"])
def process():

    subscriptions_file = request.files["subscriptions"]
    usage_file = request.files["usage"]

    sub_path = os.path.join(UPLOAD_FOLDER, "subscriptions.csv")
    usage_path = os.path.join(UPLOAD_FOLDER, "usage.csv")

    subscriptions_file.save(sub_path)
    usage_file.save(usage_path)

    subscriptions = pd.read_csv(sub_path)
    usage = pd.read_csv(usage_path)

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

    output_df.to_csv("billing_output.csv", index=False)
    generate_summary(output_df, "billing_summary.json")

    # SUMMARY LOGIC

    active_count = len(output_df[output_df["final_status"] == "ACTIVE"])
    suspended_count = len(output_df[output_df["final_status"] == "SUSPENDED"])
    cancelled_count = len(output_df[output_df["final_status"] == "CANCELLED"])
    over_limit_count = len(output_df[output_df["overage_gb"] > 0])
    within_limit_count = len(output_df[output_df["overage_gb"] == 0])
    
    summary = {
        "total_subscriptions": len(output_df),
        "total_revenue": round(output_df["total_bill"].sum(), 2),
        "active_count": active_count,
        "suspended_count": suspended_count,
        "cancelled_count": cancelled_count,
        "over_limit_count": over_limit_count,
        "within_limit_count": within_limit_count
    }

    return render_template("results.html",
                           tables=output_df.to_dict(orient="records"),
                           summary=summary)

@app.route("/download/csv")
def download_csv():
    return send_file(
        "billing_output.csv",
        as_attachment=True
    )


@app.route("/download/excel")
def download_excel():
    output_df = pd.read_csv("billing_output.csv")
    excel_path = "billing_output.xlsx"
    output_df.to_excel(excel_path, index=False)
    return send_file(
        excel_path,
        as_attachment=True
    )


@app.route("/download-summary")
def download_summary():
    return send_file("billing_summary.json", as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)