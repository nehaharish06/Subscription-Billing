def calculate_bill(monthly_fee, usage, usage_limit, status):

    if status == "CANCELLED":
        return 0, 0

    if status == "SUSPENDED":
        return monthly_fee, 0

    if usage <= usage_limit:
        return monthly_fee, 0

    overage_gb = usage - usage_limit
    overage_charge = overage_gb * 10
    total_bill = monthly_fee + overage_charge

    return total_bill, overage_gb